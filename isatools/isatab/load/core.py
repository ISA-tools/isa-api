from __future__ import annotations
from typing import TextIO
from io import StringIO

from abc import ABCMeta, abstractmethod

from os import path
from glob import glob
from re import compile

from pandas import merge, read_csv, DataFrame, Series
from numpy import nan

from isatools.utils import utf8_text_file_open
from isatools.isatab.load.read import read_tfile, read_investigation_file
from isatools.isatab.load.ProcessSequenceFactory import ProcessSequenceFactory
from isatools.isatab.defaults import _RX_COMMENT, log
from isatools.isatab.utils import strip_comments
from isatools.model import (
    OntologyAnnotation,
    Publication,
    Person,
    Comment,
    Investigation,
    OntologySource,
    Study,
    StudyFactor,
    Protocol,
    Process,
    ProtocolParameter,
    Assay
)
from .mapping import investigation_sections_mapping, get_investigation_base_output, study_sections_mapping


class ISATabReader:
    """ A class to read an ISA-Tab investigation file into a dictionary of DataFrames

    :param fp: A file-like buffer object of the investigation file
    """

    def __init__(self, fp: TextIO) -> None:
        """ Constructor for the ISATabReader class """
        self.memory_file: TextIO = fp
        self.dataframe_dict: dict[str, DataFrame | str, list[DataFrame]] = {}

    def __del__(self) -> None:
        """ Destructor hook for the ISATabReader class. Called by the garbage collector. Makes sure the file-like
        buffer object is closed even if the program crashes.
        """
        self.memory_file.close()

    @property
    def memory_file(self) -> TextIO:
        """ Getter for the in memory file-like buffer object

        :return: A file-like buffer object
        """
        return self.__memory_file

    @memory_file.setter
    def memory_file(self, fp: TextIO) -> None:
        """ Setter for the memory_file property. Reads the input file into memory, stripping out comments and
        sets the memory_file property

        :param fp: A file-like buffer object
        """
        memory_file: StringIO = StringIO()
        line: bool | str = True
        while line:
            line = fp.readline()
            if not line.lstrip().startswith('#'):
                memory_file.write(line)
        memory_file.seek(0)
        self.__memory_file = memory_file

    def __peek(self) -> str:
        """Peek at the next line without moving to the next line. This function get the position of the next line,
        reads the next line, then resets the file pointer to the original position

        :return: The next line past the current line
        """
        position: int = self.memory_file.tell()
        line: str = self.memory_file.readline()
        self.memory_file.seek(position)
        return line

    def __read_tab_section(self, sec_key: str, next_sec_key: str) -> StringIO:
        """Slices a file by section delimited by section keys

        :param sec_key: Delimiter key of beginning of section
        :param next_sec_key: Delimiter key of end of section
        :return: A memory file of the section slice, as a string buffer object
        """
        fileline: str = self.memory_file.readline()
        normed_line: str = fileline.rstrip().strip('"')
        memory_file: StringIO = StringIO()

        if normed_line != sec_key:
            raise IOError(f"Expected: {sec_key} section, but got: {normed_line}")
        while self.__peek().rstrip() != next_sec_key:
            fileline = self.memory_file.readline()
            if not fileline:
                break
            memory_file.write(fileline.rstrip() + '\n')
        memory_file.seek(0)
        return memory_file

    def __build_section_df(self, current_section_key: str, next_section_key: str) -> DataFrame:
        """Reads a file section into a DataFrame

        :param current_section_key: Name of the current section
        :param next_section_key: Name of the next section
        :return: A DataFrame corresponding to the file section
        """
        file_handler: StringIO = self.__read_tab_section(sec_key=current_section_key, next_sec_key=next_section_key)
        df: DataFrame = read_csv(
            filepath_or_buffer=file_handler,
            names=range(0, 128),
            sep='\t',
            engine='python',
            encoding='utf-8'
        ).dropna(axis=1, how='all').T
        df.replace(nan, '', regex=True, inplace=True)  # Strip out the nan entries
        df.reset_index(inplace=True)  # Reset study_index so it is accessible as column
        df.columns = df.iloc[0]  # If all was OK, promote this row to the column headers
        return df.reindex(df.index.drop(0))  # Return the re-indexed DataFrame

    def run(self) -> dict[str, DataFrame | str, list[DataFrame]]:
        """ Main method to run the ISATabReader and return the dictionary of DataFrames

        :return: A dictionary holding a set of DataFrames for each section of the investigation file
        """
        # Make a copy of the base output to avoid modifying the original
        output: dict[str, DataFrame | str, list] = {**get_investigation_base_output()}
        for section, section_keys in investigation_sections_mapping.items():
            output[section] = self.__build_section_df(**section_keys)
        while self.__peek():
            for section, section_keys in study_sections_mapping.items():
                output[section].append(self.__build_section_df(**section_keys))
        return output


class ISATabLoaderMixin(metaclass=ABCMeta):
    """ A mixin to provide modeling for the ISATab loaders. Provides shared methods, attributes and implementations

    - Properties:
        - ontology_source_map: A dictionary of OntologySource objects references
        - skip_load_tables: A boolean to skip loading the studies and assays table files
        - filepath: The filepath of the investigation file

    - Methods:
        - get_contacts: Get a list of Person objects from the relevant investigation file section
        - get_comments: Get Comments from a section DataFrame
        - get_comments_row: Get Comments in a given DataFrame row
        - get_ontology_annotation: Gets an OntologyAnnotation for a given value, accession and term source REF
        - get_ontology_annotations: Gets a list of OntologyAnnotations from semicolon delimited lists
        - get_publications: Get a list of Publication objects from the relevant investigation file section

    - Abstract Methods:
        - load: Load the investigation file into the Investigation object
    """

    ontology_source_map: dict
    skip_load_tables: bool = False
    filepath: str

    def __get_ontology_source(self, term_source_ref) -> OntologySource | None:
        """ Small wrapper to return an ontology source from the map or None if not found

        :param term_source_ref: The term source reference
        :return: An OntologySource object or None
        """
        return None if term_source_ref not in self.ontology_source_map else self.ontology_source_map[term_source_ref]

    def get_contacts(self, contact_dataframe: DataFrame) -> list[Person]:
        """Get a list of Person objects from the relevant investigation file
        section

        :param contact_dataframe: A CONTACTS section DataFrame
        :return: A list of Person objects
        """
        contacts: list[Person] = []
        prefix: str

        if 'Investigation Person Last Name' in contact_dataframe.columns:
            prefix = 'Investigation '
        elif 'Study Person Last Name' in contact_dataframe.columns:
            prefix = 'Study '
        else:
            raise KeyError

        for current_row in contact_dataframe.to_dict(orient='records'):
            person: Person = Person(
                last_name=current_row[prefix + 'Person Last Name'],
                first_name=current_row[prefix + 'Person First Name'],
                mid_initials=current_row[prefix + 'Person Mid Initials'],
                email=current_row[prefix + 'Person Email'],
                phone=current_row[prefix + 'Person Phone'],
                fax=current_row[prefix + 'Person Fax'],
                address=current_row[prefix + 'Person Address'],
                affiliation=current_row[prefix + 'Person Affiliation']
            )
            person.roles = self.get_ontology_annotations(
                vals=current_row[prefix + 'Person Roles'],
                accessions=current_row[prefix + 'Person Roles Term Accession Number'],
                ts_refs=current_row[prefix + 'Person Roles Term Source REF']
            )
            person.comments = self.get_comments_row(contact_dataframe.columns, current_row)
            contacts.append(person)

        return contacts

    @staticmethod
    def get_comments(section_df: DataFrame) -> list[Comment]:
        """Get Comments from a section DataFrame

        :param section_df: A section DataFrame
        :return: A list of Comment objects as found in the section
        """
        comments: list[Comment] = []
        for col in [x for x in section_df.columns if _RX_COMMENT.match(str(x))]:
            for _, current_row in section_df.iterrows():
                comments.append(Comment(name=next(iter(_RX_COMMENT.findall(col))), value=current_row[col]))
        return comments

    @staticmethod
    def get_comments_row(cols, row) -> list[Comment]:
        """Get Comments in a given DataFrame row

        :param cols: List of DataFrame columns
        :param row: DataFrame row as a Series object
        :return: A list of Comment objects
        """
        comments: list[Comment] = []
        for col in [x for x in cols if _RX_COMMENT.match(str(x))]:
            comments.append(Comment(name=next(iter(_RX_COMMENT.findall(col))), value=row[col]))
        return comments

    def get_ontology_annotation(self, val, accession, ts_ref) -> OntologyAnnotation | None:
        """Gets an OntologyAnnotation for a given value, accession and term source REF

        :param val: Value of the OntologyAnnotation
        :param accession: Term Accession Number of the OntologyAnnotation
        :param ts_ref: Term Source REF of the OntologyAnnotation
        :return: An OntologyAnnotation object
        """
        if val == '' and accession == '':
            return None
        return OntologyAnnotation(val, self.__get_ontology_source(ts_ref), accession)

    def get_ontology_annotations(self, vals, accessions, ts_refs) -> list[OntologyAnnotation]:
        """ Gets a list of OntologyAnnotations from semicolon delimited lists

        :param vals: A list of values, separated by semi-colons
        :param accessions: A list of accessions, separated by semicolons
        :param ts_refs: A list of term source REFs, separated by semicolons
        :return: A list of OntologyAnnotation objects
        """
        ontology_annotations: list[OntologyAnnotation] = []
        accession_split: list[str] = accessions.split(';')
        ts_refs_split: list[str] = ts_refs.split(';')

        # if no acc or ts_refs
        if accession_split == [''] and ts_refs_split == ['']:
            for val in vals.split(';'):
                ontology_annotations.append(OntologyAnnotation(term=val))
        else:
            for index, val in enumerate(vals.split(';')):
                ontology_annotation: OntologyAnnotation | None = self.get_ontology_annotation(
                    val=val, accession=accessions.split(';')[index], ts_ref=ts_refs.split(';')[index]
                )
                if ontology_annotation:
                    ontology_annotations.append(ontology_annotation)
        return ontology_annotations

    def get_publications(self, section_df) -> list[Publication]:
        publications: list[Publication] = []
        prefix: str

        if 'Investigation PubMed ID' in section_df.columns:
            prefix = 'Investigation '
        elif 'Study PubMed ID' in section_df.columns:
            prefix = 'Study '
        else:
            raise KeyError

        for _, current_row in section_df.iterrows():
            publication: Publication = Publication(
                pubmed_id=current_row[prefix + 'PubMed ID'],
                doi=current_row[prefix + 'Publication DOI'],
                author_list=current_row[prefix + 'Publication Author List'],
                title=current_row[prefix + 'Publication Title']
            )
            publication.status = self.get_ontology_annotation(
                current_row[prefix + 'Publication Status'],
                current_row[prefix + 'Publication Status Term Accession Number'],
                current_row[prefix + 'Publication Status Term Source REF'])
            publication.comments = self.get_comments_row(section_df.columns, current_row)
            publications.append(publication)
        return publications

    @abstractmethod
    def load(self, **kwargs):
        raise NotImplementedError


class ISATabLoaderStudyAssayMixin(metaclass=ABCMeta):
    """ A mixin for the Study and Assay loaders. Provides shared abstract methods to prevent code duplication

    - Properties:
        - unknown_protocol_description: A description for an unknown protocol
        - protocol_map: A dictionary of Protocol objects references

    - Methods:
        - update_protocols: Update the protocols in the process with the protocol map
        - set_misc: Bind misc data to the target object (Study or Assay)

    - Abstract Methods:
        - load_tables: Load the study or assay table file
    """

    unknown_protocol_description: str = "This protocol was auto-generated where a protocol could not be determined."
    protocol_map: dict[str, Protocol] = {}

    def update_protocols(self, process: Process, study: Study, protocol_map) -> None:
        """ Update the protocols in the process with the protocol map and binds it to the study in case of an
        unknown protocol

        :param process: The process to update
        :param study: The study to bind the protocol to
        :param protocol_map: A dictionary of Protocol objects references
        """
        if process.executes_protocol in protocol_map:
            protocol_name: str | Protocol = process.executes_protocol
            process.executes_protocol = protocol_map[protocol_name]
            return
        if 'unknown' in protocol_map:
            process.executes_protocol = protocol_map['unknown']
            return
        protocol: Protocol = Protocol(name="unknown protocol", description=self.unknown_protocol_description)
        protocol_map['unknown'] = protocol
        process.executes_protocol = protocol
        study.protocols.append(protocol)
        process.executes_protocol = protocol

    @staticmethod
    def set_misc(
            target: Study | Assay,
            samples: dict,
            processes: dict,
            characteristic_categories: dict,
            unit_categories: dict
    ) -> Study | Assay:
        """ Bind misc data to the target object (Study or Assay). The data to be loaded includes:
            - samples
            - process_sequence
            - characteristic_categories
            - units

        :param target: The study or assay to update
        :param samples: A dictionary of Sample objects
        :param processes: A dictionary of Process objects
        :param characteristic_categories: A dictionary of characteristic categories
        :param unit_categories: A dictionary of unit categories
        :return: The updated study or assay
        """
        target.samples = sorted(list(samples.values()), key=lambda x: x.name)
        target.process_sequence = list(processes.values())
        target.characteristic_categories = sorted(list(characteristic_categories.values()), key=lambda x: x.term)
        target.units = sorted(list(unit_categories.values()), key=lambda x: x.term)
        return target

    @abstractmethod
    def load_tables(self, **kwargs):
        raise NotImplementedError


class ISATabInvestigationLoader(ISATabLoaderMixin):
    """ A class to load an ISA-Tab investigation file into an Investigation object

    :param file: A file-like buffer object or a string representing a file path / directory containing the ISA-Tab
    :param run: Whether to run the load method in the constructor
    :param skip_load_table: Whether to skip loading the table files
    """

    def __init__(self, file: TextIO | str, run: bool = True, skip_load_table: bool = False) -> None:
        """ Constructor for the ISATabInvestigationLoader class

        """
        ISATabLoaderMixin.skip_load_tables = skip_load_table
        self.__investigation: Investigation
        self.__df_dict: dict = {}
        self.file: TextIO = file
        if run:
            self.load()

    def __del__(self, **kwargs) -> None:
        """ Destructor hook for the ISATabInvestigationLoader class. Called by the garbage collector. Makes sure
        the file-like buffer object is closed even if the program crashes.
        """
        self.file.close()

    @property
    def investigation(self) -> Investigation:
        """ Getter for the ISA Investigation object. Setter is not allowed

        :return: An Investigation object
        """
        return self.__investigation

    @property
    def file(self) -> TextIO:
        """ Getter for the in memory file-like buffer object

        :return: A file-like buffer object
        """
        return self.__file

    @file.setter
    def file(self, file: str | TextIO) -> None:
        """ Setter for the file property. Also sets the __df_dict property

        :param file: A file-like buffer object or a string representing a file path / directory containing the ISA-Tab
        """
        file_content: TextIO | None = None
        if isinstance(file, str):
            if path.isdir(file):
                fnames: list = glob(path.join(file, "i_*.txt"))
                assert len(fnames) == 1
                file_content = utf8_text_file_open(fnames[0])
        elif hasattr(file, 'read'):
            file_content = file
        else:
            raise IOError("Cannot resolve input file")
        self.__file = file_content
        isatab_reader: ISATabReader = ISATabReader(file_content)
        self.__df_dict = isatab_reader.run()
        ISATabLoaderMixin.filepath = self.file.name

    def __set_ontology_source(self, row: Series) -> None:
        """Sets the ontology source from the given row at the top of the investigation file in the investigation object

        :param row: A row from the investigation file
        """
        ontology_source: OntologySource = OntologySource(
            name=row['Term Source Name'],
            file=row['Term Source File'],
            version=row['Term Source Version'],
            description=row['Term Source Description'])
        ontology_source.comments = self.get_comments(self.__df_dict['ontology_sources'])
        self.__investigation.ontology_source_references.append(ontology_source)

    def __create_investigation(self) -> None:
        """ Loads all data regarding the investigation into the Investigation object. Studies and assays are
        loaded in a separate private method.
        """
        self.__investigation = Investigation()
        self.__df_dict['ontology_sources'].apply(lambda r: self.__set_ontology_source(r), axis=1)
        ISATabLoaderMixin.ontology_source_map = dict(
            map(lambda x: (x.name, x), self.__investigation.ontology_source_references)
        )

        if not self.__df_dict['investigation'].empty:
            row = self.__df_dict['investigation'].iloc[0]
            self.__investigation.identifier = str(row['Investigation Identifier'])
            self.__investigation.title = row['Investigation Title']
            self.__investigation.description = row['Investigation Description']
            self.__investigation.submission_date = row['Investigation Submission Date']
            self.__investigation.public_release_date = row['Investigation Public Release Date']
        self.__investigation.publications = self.get_publications(self.__df_dict['i_publications'])
        self.__investigation.contacts = self.get_contacts(self.__df_dict['i_contacts'])
        self.__investigation.comments = self.get_comments(self.__df_dict['investigation'])

    def __create_studies(self) -> None:
        """ Loads all the studies inside the investigation object """
        for i, row in enumerate(self.__df_dict['studies']):
            row = row.iloc[0]
            study_loader: ISATabStudyLoader = ISATabStudyLoader(row, self.__df_dict, i)
            study_loader.load()
            self.__investigation.studies.append(study_loader.study)

    def load(self):
        """ Public wrapper to load the investigation file into the Investigation object. """
        self.__create_investigation()
        self.__create_studies()


class ISATabStudyLoader(ISATabLoaderMixin, ISATabLoaderStudyAssayMixin):
    """ A class to load an ISA-Tab study file into a Study object

    :param row: A row from the study file
    :param df_dict: A dictionary of DataFrames containing the data extracted from the investigation file
    :param index: The study index of this study in this investigation
    """

    def __init__(self, row: DataFrame, df_dict: dict, index: int) -> None:
        """ Constructor for the ISATabStudyLoader class """
        ISATabLoaderStudyAssayMixin.protocol_map = {}

        self.__study_index: int = index
        self.__row: DataFrame = row
        self.__publications: list[DataFrame] = df_dict['s_publications']
        self.__contacts: list[DataFrame] = df_dict['s_contacts']
        self.__comments: DataFrame = df_dict['studies']
        self.__design_descriptors: list[DataFrame] = df_dict['s_design_descriptors']
        self.__factors: list[DataFrame] = df_dict['s_factors']
        self.__protocols: list[DataFrame] = df_dict['s_protocols']
        self.__assays: list[DataFrame] = df_dict['s_assays']
        self.study: Study | None = None

    def __get_design_descriptors(self) -> list[OntologyAnnotation]:
        """ Load the design descriptors from the study file into the Study object

        :return: A list of OntologyAnnotation describing design descriptors
        """
        design_descriptors: list[OntologyAnnotation] = []
        for _, row in self.__design_descriptors[self.__study_index].iterrows():
            design_descriptor = self.get_ontology_annotation(
                row['Study Design Type'],
                row['Study Design Type Term Accession Number'],
                row['Study Design Type Term Source REF'])
            design_descriptor.comments = self.get_comments_row(
                self.__design_descriptors[self.__study_index].columns, row
            )
            design_descriptors.append(design_descriptor)
        return design_descriptors

    def __get_factors(self) -> list[StudyFactor]:
        """ Load the factors from the study file into the Study object

        :return: A list of StudyFactor
        """
        factors: list[StudyFactor] = []
        for _, row in self.__factors[self.__study_index].iterrows():
            factor = StudyFactor(name=row['Study Factor Name'])
            factor.factor_type = self.get_ontology_annotation(
                row['Study Factor Type'],
                row['Study Factor Type Term Accession Number'],
                row['Study Factor Type Term Source REF'])
            factor.comments = self.get_comments_row(self.__factors[self.__study_index].columns, row)
            factors.append(factor)
        return factors

    def __get_protocols(self) -> list[Protocol]:
        """ Load the protocols from the study file into the Study object

        :return: A list of Protocol
        """
        protocols: list[Protocol] = []
        for _, row in self.__protocols[self.__study_index].iterrows():
            protocol = Protocol()
            protocol.name = row['Study Protocol Name']
            protocol.description = row['Study Protocol Description']
            protocol.uri = row['Study Protocol URI']
            protocol.version = row['Study Protocol Version']
            protocol.protocol_type = self.get_ontology_annotation(
                row['Study Protocol Type'],
                row['Study Protocol Type Term Accession Number'],
                row['Study Protocol Type Term Source REF'])
            params = self.get_ontology_annotations(
                row['Study Protocol Parameters Name'],
                row['Study Protocol Parameters Name Term Accession Number'],
                row['Study Protocol Parameters Name Term Source REF'])
            for param in params:
                protocol_param = ProtocolParameter(parameter_name=param)
                protocol.parameters.append(protocol_param)
            protocol.comments = self.get_comments_row(self.__protocols[self.__study_index].columns, row)
            protocols.append(protocol)
            ISATabLoaderStudyAssayMixin.protocol_map[protocol.name] = protocol
        return protocols

    def __create_assays(self):
        """ Create the assays and bind them to the study object """
        for _, row in self.__assays[self.__study_index].iterrows():
            assay_loader: ISATabAssayLoader = ISATabAssayLoader(
                row, self.__assays[self.__study_index].columns, self.study
            )
            assay_loader.load()
            self.study.assays.append(assay_loader.assay)

    def __create_study(self) -> None:
        """ Create the Study object from the dataframes """
        self.study = Study(
            identifier=str(self.__row['Study Identifier']),
            title=self.__row['Study Title'],
            description=self.__row['Study Description'],
            submission_date=self.__row['Study Submission Date'],
            public_release_date=self.__row['Study Public Release Date'],
            filename=self.__row['Study File Name'],
            publications=self.get_publications(self.__publications[self.__study_index]),
            contacts=self.get_contacts(self.__contacts[self.__study_index]),
            comments=self.get_comments(self.__comments[self.__study_index])
        )
        self.study.design_descriptors = self.__get_design_descriptors()
        self.study.factors = self.__get_factors()
        self.study.protocols = self.__get_protocols()

        if not self.skip_load_tables:
            self.load_tables(filename=self.study.filename)

    def load(self):
        """ Public wrapper to load the study file into the Study object """
        self.__create_study()
        self.__create_assays()

    def load_tables(self, filename: str) -> None:
        """ Load the study table file into the Study object.

        :param filename: The filename of the study file
        """
        process_sequence_factory: ProcessSequenceFactory = ProcessSequenceFactory(
            ontology_sources=self.ontology_source_map.values(),
            study_protocols=self.study.protocols,
            study_factors=self.study.factors
        )
        sources, samples, _, __, processes, characteristic_categories, unit_categories = \
            process_sequence_factory.create_from_df(read_tfile(path.join(path.dirname(self.filepath), filename)))
        self.study.sources = sorted(list(sources.values()), key=lambda x: x.name)
        self.study = self.set_misc(self.study, samples, processes, characteristic_categories, unit_categories)

        for process in self.study.process_sequence:
            self.update_protocols(process, self.study, self.protocol_map)


class ISATabAssayLoader(ISATabLoaderMixin, ISATabLoaderStudyAssayMixin):
    """ A class to load an ISA-Tab assay file into an Assay object

    :param row: A row from the assay file
    :param study: The Study object to which this assay belongs (required to add protocols to the study)
    """

    def __init__(self, row: Series, columns: list[str], study: Study) -> None:
        """ Constructor for the ISATabAssayLoader class """
        self.__row: Series = row
        self.__columns: list[str] = columns
        self.__study: Study = study
        self.assay: Assay | None = None

    def load(self):
        """ Create the assay object from the dataframes """
        self.assay = Assay(**{
            "filename": self.__row['Study Assay File Name'],
            "measurement_type": self.get_ontology_annotation(
                self.__row['Study Assay Measurement Type'],
                self.__row['Study Assay Measurement Type Term Accession Number'],
                self.__row['Study Assay Measurement Type Term Source REF']
            ),
            "technology_type": self.get_ontology_annotation(
                self.__row['Study Assay Technology Type'],
                self.__row['Study Assay Technology Type Term Accession Number'],
                self.__row['Study Assay Technology Type Term Source REF']
            ),
            "technology_platform": self.__row['Study Assay Technology Platform'],
            "comments": self.get_comments_row(self.__columns, self.__row)
        })
        if not self.skip_load_tables:
            self.load_tables()

    def load_tables(self):
        """ Load the assay table file into the Assay object """
        assay_table_file = read_tfile(path.join(path.dirname(self.filepath), self.assay.filename))
        _, samples, other, data, processes, characteristic_categories, unit_categories = ProcessSequenceFactory(
            ontology_sources=self.ontology_source_map.values(),
            study_samples=self.__study.samples,
            study_protocols=self.__study.protocols,
            study_factors=self.__study.factors
        ).create_from_df(assay_table_file)
        self.assay.other_material = sorted(list(other.values()), key=lambda x: x.name)
        self.assay.data_files = sorted(list(data.values()), key=lambda x: x.filename)
        self.assay = self.set_misc(self.assay, samples, processes, characteristic_categories, unit_categories)
        for process in self.assay.process_sequence:
            self.update_protocols(process, self.__study, self.protocol_map)


def load(isatab_path_or_ifile: object, skip_load_tables: object = False) -> object:
    """Load an ISA-Tab into ISA Data Model objects

    :rtype: object
    :param isatab_path_or_ifile: Full path to an ISA-Tab directory or file-like
    buffer object pointing to an investigation file
    :param skip_load_tables: Whether or not to skip loading the table files
    :return: Investigation objects
    """

    # from DF of investigation file

    def get_ontology_source(term_source_ref):
        try:
            current_onto_source = ontology_source_map[term_source_ref]
        except KeyError:
            current_onto_source = None
        return current_onto_source

    def get_oa(val, accession, ts_ref):
        """Gets a OntologyAnnotation for a give value, accession and
        term source REF

        :param val: Value of the OA
        :param accession: Term Accession Number of the OA
        :param ts_ref: Term Source REF of the OA
        :return: An OntologyAnnotation object
        """
        if val == '' and accession == '':
            return None
        else:
            return OntologyAnnotation(
                term=val,
                term_accession=accession,
                term_source=get_ontology_source(ts_ref)
            )

    def get_oa_list_from_semi_c_list(vals, accessions, ts_refs):
        """Gets a list of OntologyAnnotations from semi-colon delimited lists

        :param vals: A list of values, separated by semi-colons
        :param accessions: A list of accessions, separated by semi-colons
        :param ts_refs: A list of term source REFs, separated by semi-colons
        :return: A list of OntologyAnnotation objects
        """
        oa_list = []
        accession_split = accessions.split(';')
        ts_refs_split = ts_refs.split(';')
        # if no acc or ts_refs
        if accession_split == [''] and ts_refs_split == ['']:
            for val in vals.split(';'):
                oa_list.append(OntologyAnnotation(term=val, ))
        else:  # try parse all three sections
            for _, val in enumerate(vals.split(';')):
                oa = get_oa(val, accessions.split(';')[_], ts_refs.split(';')[_])
                if oa is not None:
                    oa_list.append(oa)
        return oa_list

    def get_publications(section_df):
        """Get a list of Publications from the relevant investigation file
        section

        :param section_df: A PUBLICATIONS section DataFrame
        :return: A list of Publication objects
        """
        if 'Investigation PubMed ID' in section_df.columns:
            prefix = 'Investigation '
        elif 'Study PubMed ID' in section_df.columns:
            prefix = 'Study '
        else:
            raise KeyError

        publications = []

        for _, current_row in section_df.iterrows():
            publication = Publication(pubmed_id=current_row[prefix + 'PubMed ID'],
                                      doi=current_row[prefix + 'Publication DOI'],
                                      author_list=current_row[
                                          prefix + 'Publication Author List'],
                                      title=current_row[prefix + 'Publication Title'])

            publication.status = get_oa(
                current_row[prefix + 'Publication Status'],
                current_row[prefix + 'Publication Status Term Accession Number'],
                current_row[prefix + 'Publication Status Term Source REF'])
            publication.comments = get_comments_row(section_df.columns, current_row)
            publications.append(publication)

        return publications

    def get_contacts(section_df):
        """Get a list of Person objects from the relevant investigation file
        section

        :param section_df: A CONTACTS section DataFrame
        :return: A list of Person objects
        """
        if 'Investigation Person Last Name' in section_df.columns:
            prefix = 'Investigation '
        elif 'Study Person Last Name' in section_df.columns:
            prefix = 'Study '
        else:
            raise KeyError

        contacts = []

        for _, current_row in section_df.iterrows():
            person = Person(last_name=current_row[prefix + 'Person Last Name'],
                            first_name=current_row[prefix + 'Person First Name'],
                            mid_initials=current_row[prefix + 'Person Mid Initials'],
                            email=current_row[prefix + 'Person Email'],
                            phone=current_row[prefix + 'Person Phone'],
                            fax=current_row[prefix + 'Person Fax'],
                            address=current_row[prefix + 'Person Address'],
                            affiliation=current_row[prefix + 'Person Affiliation'])

            person.roles = get_oa_list_from_semi_c_list(
                current_row[prefix + 'Person Roles'],
                current_row[prefix + 'Person Roles Term Accession Number'],
                current_row[prefix + 'Person Roles Term Source REF'])
            person.comments = get_comments_row(section_df.columns, current_row)
            contacts.append(person)

        return contacts

    def get_comments(section_df):
        """Get Comments from a section DataFrame

        :param section_df: A section DataFrame
        :return: A list of Comment objects as found in the section
        """
        comments = []
        for col in [x for x in section_df.columns if _RX_COMMENT.match(str(x))]:
            for _, current_row in section_df.iterrows():
                comment = Comment(
                    name=next(iter(_RX_COMMENT.findall(col))), value=current_row[col])
                comments.append(comment)
        return comments

    def get_comments_row(cols, row):
        """Get Comments in a given DataFrame row

        :param cols: List of DataFrame columns
        :param row: DataFrame row as a Series object
        :return: A list of Comment objects
        """
        comments = []
        for col in [x for x in cols if _RX_COMMENT.match(str(x))]:
            comment = Comment(
                name=next(iter(_RX_COMMENT.findall(col))), value=row[col])
            comments.append(comment)
        return comments

    def get_ontology_sources(r):
        ontology_source = OntologySource(
            name=r['Term Source Name'],
            file=r['Term Source File'],
            version=r['Term Source Version'],
            description=r['Term Source Description'])
        ontology_source.comments = get_comments_row(df_dict['ontology_sources'].columns, r)
        investigation.ontology_source_references.append(ontology_source)

    FP = None

    if isinstance(isatab_path_or_ifile, str):
        if path.isdir(isatab_path_or_ifile):
            fnames = glob(path.join(isatab_path_or_ifile, "i_*.txt"))
            assert len(fnames) == 1
            FP = utf8_text_file_open(fnames[0])
    elif hasattr(isatab_path_or_ifile, 'read'):
        FP = isatab_path_or_ifile
    else:
        raise IOError("Cannot resolve input file")

    try:
        df_dict = read_investigation_file(FP)
        investigation = Investigation()

        df_dict['ontology_sources'].apply(lambda x: get_ontology_sources(x), axis=1)
        ontology_source_map = dict(map(lambda x: (x.name, x), investigation.ontology_source_references))

        if not df_dict['investigation'].empty:
            row = df_dict['investigation'].iloc[0]
            investigation.identifier = str(row['Investigation Identifier'])
            investigation.title = row['Investigation Title']
            investigation.description = row['Investigation Description']
            investigation.submission_date = row['Investigation Submission Date']
            investigation.public_release_date = row['Investigation Public Release Date']
        investigation.publications = get_publications(df_dict['i_publications'])
        investigation.contacts = get_contacts(df_dict['i_contacts'])
        investigation.comments = get_comments(df_dict['investigation'])

        for i in range(0, len(df_dict['studies'])):
            row = df_dict['studies'][i].iloc[0]
            study = Study()
            study.identifier = str(row['Study Identifier'])
            study.title = row['Study Title']
            study.description = row['Study Description']
            study.submission_date = row['Study Submission Date']
            study.public_release_date = row['Study Public Release Date']
            study.filename = row['Study File Name']

            study.publications = get_publications(df_dict['s_publications'][i])
            study.contacts = get_contacts(df_dict['s_contacts'][i])
            study.comments = get_comments(df_dict['studies'][i])

            for _, row in df_dict['s_design_descriptors'][i].iterrows():
                design_descriptor = get_oa(
                    row['Study Design Type'],
                    row['Study Design Type Term Accession Number'],
                    row['Study Design Type Term Source REF'])
                these_comments = get_comments_row(df_dict['s_design_descriptors'][i].columns, row)
                design_descriptor.comments = these_comments
                study.design_descriptors.append(design_descriptor)

            for _, row in df_dict['s_factors'][i].iterrows():
                factor = StudyFactor(name=row['Study Factor Name'])
                factor.factor_type = get_oa(
                    row['Study Factor Type'],
                    row['Study Factor Type Term Accession Number'],
                    row['Study Factor Type Term Source REF'])
                factor.comments = get_comments_row(df_dict['s_factors'][i].columns, row)
                study.factors.append(factor)

            protocol_map = {}
            for _, row in df_dict['s_protocols'][i].iterrows():
                protocol = Protocol()
                protocol.name = row['Study Protocol Name']
                protocol.description = row['Study Protocol Description']
                protocol.uri = row['Study Protocol URI']
                protocol.version = row['Study Protocol Version']
                protocol.protocol_type = get_oa(
                    row['Study Protocol Type'],
                    row['Study Protocol Type Term Accession Number'],
                    row['Study Protocol Type Term Source REF'])
                params = get_oa_list_from_semi_c_list(
                    row['Study Protocol Parameters Name'],
                    row['Study Protocol Parameters Name Term Accession Number'],
                    row['Study Protocol Parameters Name Term Source REF'])
                for param in params:
                    protocol_param = ProtocolParameter(parameter_name=param)
                    protocol.parameters.append(protocol_param)
                protocol.comments = get_comments_row(df_dict['s_protocols'][i].columns, row)
                study.protocols.append(protocol)
                protocol_map[protocol.name] = protocol
            study.protocols = list(protocol_map.values())
            if skip_load_tables:
                pass
            else:
                study_tfile_df = read_tfile(path.join(path.dirname(FP.name), study.filename))
                iosrs = investigation.ontology_source_references
                sources, samples, _, __, processes, characteristic_categories, unit_categories = \
                    ProcessSequenceFactory(
                        ontology_sources=iosrs,
                        study_protocols=study.protocols,
                        study_factors=study.factors
                    ).create_from_df(study_tfile_df)
                study.sources = sorted(list(sources.values()), key=lambda x: x.name, reverse=False)
                study.samples = sorted(list(samples.values()), key=lambda x: x.name, reverse=False)
                study.process_sequence = list(processes.values())
                study.characteristic_categories = sorted(
                    list(characteristic_categories.values()),
                    key=lambda x: x.term,
                    reverse=False)
                study.units = sorted(list(unit_categories.values()), key=lambda x: x.term, reverse=False)

                for process in study.process_sequence:
                    try:
                        process.executes_protocol = protocol_map[process.executes_protocol]
                    except KeyError:
                        try:
                            unknown_protocol = protocol_map['unknown']
                        except KeyError:
                            description = "This protocol was auto-generated where a protocol could not be determined."
                            protocol_map['unknown'] = Protocol(name="unknown protocol", description=description)
                            unknown_protocol = protocol_map['unknown']
                            study.protocols.append(unknown_protocol)
                        process.executes_protocol = unknown_protocol

            for _, row in df_dict['s_assays'][i].iterrows():
                assay_dict = {
                    "filename": row['Study Assay File Name'],
                    "measurement_type": get_oa(
                        row['Study Assay Measurement Type'],
                        row['Study Assay Measurement Type Term Accession Number'],
                        row['Study Assay Measurement Type Term Source REF']
                    ),
                    "technology_type": get_oa(
                        row['Study Assay Technology Type'],
                        row['Study Assay Technology Type Term Accession Number'],
                        row['Study Assay Technology Type Term Source REF']
                    ),
                    "technology_platform": row['Study Assay Technology Platform'],
                    "comments": get_comments_row(df_dict['s_assays'][i].columns, row)
                }
                assay = Assay(**assay_dict)

                if skip_load_tables:
                    pass
                else:
                    iosrs = investigation.ontology_source_references
                    assay_tfile_df = read_tfile(path.join(path.dirname(FP.name), assay.filename))
                    _, samples, other, data, processes, characteristic_categories, unit_categories = \
                        ProcessSequenceFactory(
                            ontology_sources=iosrs,
                            study_samples=study.samples,
                            study_protocols=study.protocols,
                            study_factors=study.factors).create_from_df(
                            assay_tfile_df)
                    assay.samples = sorted(
                        list(samples.values()), key=lambda x: x.name,
                        reverse=False)
                    assay.other_material = sorted(
                        list(other.values()), key=lambda x: x.name,
                        reverse=False)
                    assay.data_files = sorted(
                        list(data.values()), key=lambda x: x.filename,
                        reverse=False)
                    assay.process_sequence = list(processes.values())
                    assay.characteristic_categories = sorted(
                        list(characteristic_categories.values()),
                        key=lambda x: x.term, reverse=False)
                    assay.units = sorted(
                        list(unit_categories.values()), key=lambda x: x.term,
                        reverse=False)

                    for process in assay.process_sequence:
                        try:
                            process.executes_protocol = protocol_map[process.executes_protocol]
                        except KeyError:
                            try:
                                unknown_protocol = protocol_map['unknown']
                            except KeyError:
                                description = "This protocol was auto-generated where a protocol could not be determined."
                                protocol_map['unknown'] = Protocol(name="unknown protocol", description=description)
                                unknown_protocol = protocol_map['unknown']
                                study.protocols.append(unknown_protocol)
                            process.executes_protocol = unknown_protocol

                study.assays.append(assay)
            investigation.studies.append(study)
    finally:
        FP.close()
    return investigation


def merge_study_with_assay_tables(study_file_path, assay_file_path, target_file_path):
    """
        Utility function to merge a study table file with an assay table
        file. The merge uses the Sample Name as the
        key, so samples in the assay file must match those in the study file.
        If there are no matches, the function
        will output the joined header and no additional rows.

        Usage:

        merge_study_with_assay_tables('/path/to/study.txt',
        '/path/to/assay.txt', '/path/to/merged.txt')
    """
    log.info("Reading study file %s into DataFrame", study_file_path)
    study_DF = read_tfile(study_file_path)
    log.info("Reading assay file %s into DataFrame", assay_file_path)
    assay_DF = read_tfile(assay_file_path)
    log.info("Merging DataFrames...")
    merged_DF = merge(study_DF, assay_DF, on='Sample Name')
    log.info("Writing merged DataFrame to file %s", target_file_path)
    with open(target_file_path, 'w', encoding='utf-8') as fp:
        merged_DF.to_csv(fp, sep='\t', index=False, header=study_DF.isatab_header + assay_DF.isatab_header[1:])


def load_table(fp):
    """Loads a ISA table file into a DataFrame

    :param fp: A file-like buffer object
    :return: DataFrame of the study or assay table
    """
    try:
        fp = strip_comments(fp)
        df = read_csv(fp, dtype=str, sep='\t', encoding='utf-8').replace(nan, '')
    except UnicodeDecodeError:
        log.warning("Could not load file with UTF-8, trying ISO-8859-1")
        fp = strip_comments(fp)
        df = read_csv(fp, dtype=str, sep='\t', encoding='latin1').replace(nan, '')
    labels = df.columns
    new_labels = []
    for label in labels:
        any_var_regex = compile(r'.*\[(.*?)\]')
        hits = any_var_regex.findall(label)
        if len(hits) > 0:
            val = hits[0].strip()
            new_label = ""
            if 'Comment' in label:
                new_label = 'Comment[{val}]'.format(val=val)
            elif 'Characteristics' in label:
                new_label = 'Characteristics[{val}]'.format(val=val)
            elif 'Parameter Value' in label:
                new_label = 'Parameter Value[{val}]'.format(val=val)
            elif 'Factor Value' in label:
                new_label = 'Factor Value[{val}]'.format(val=val)
            new_labels.append(new_label)
        elif label == "Material Type":
            new_label = 'Characteristics[Material Type]'
            new_labels.append(new_label)
        else:
            new_labels.append(label)
    df.columns = new_labels
    return df
