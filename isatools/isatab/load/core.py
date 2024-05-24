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
from isatools.isatab.load.ProcessSequenceFactory import ProcessSequenceFactory
from isatools.isatab.defaults import _RX_COMMENT, log
from isatools.isatab.utils import strip_comments, IsaTabDataFrame
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
        for key in row.keys():
            if _RX_COMMENT.match(str(key)) and row[key]:
                source_name = next(iter(_RX_COMMENT.findall(str(key))))
                ontology_source.comments.append(Comment(name=source_name, value=row[key]))
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


def load(isatab_path_or_ifile: TextIO, skip_load_tables: bool = False) -> Investigation:
    """Load an ISA-Tab into ISA Data Model objects

    :param isatab_path_or_ifile: Full path to an ISA-Tab directory or file-like
    buffer object pointing to an investigation file
    :param skip_load_tables: Whether to skip loading the table files
    :return: Investigation objects
    """
    investigation_loader: ISATabInvestigationLoader = ISATabInvestigationLoader(
        file=isatab_path_or_ifile, skip_load_table=skip_load_tables
    )
    return investigation_loader.investigation


def merge_study_with_assay_tables(study_file_path: str, assay_file_path: str, target_file_path: str):
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
    study_dataframe = read_tfile(study_file_path)
    log.info("Reading assay file %s into DataFrame", assay_file_path)
    assay_dataframe = read_tfile(assay_file_path)
    log.info("Merging DataFrames...")
    merged_dataframe = merge(study_dataframe, assay_dataframe, on='Sample Name')
    log.info("Writing merged DataFrame to file %s", target_file_path)
    headers = study_dataframe.isatab_header + assay_dataframe.isatab_header[1:]
    with open(target_file_path, 'w', encoding='utf-8') as fp:
        merged_dataframe.to_csv(fp, sep='\t', index=False, header=headers)


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


def read_tfile(tfile_path: str, index_col=None, factor_filter=None) -> IsaTabDataFrame:
    """Read a table file into a DataFrame

    :param tfile_path: Path to a table file to load
    :param index_col: The column to use as study_index
    :param factor_filter: Factor filter tuple, e.g. ('Gender', 'Male') will
    filter on FactorValue[Gender] == Male
    :return: A table file DataFrame
    """
    with utf8_text_file_open(tfile_path) as tfile_fp:
        tfile_fp.seek(0)
        tfile_fp = strip_comments(tfile_fp)
        csv = read_csv(tfile_fp, dtype=str, sep='\t', index_col=index_col, encoding='utf-8').fillna('')
        tfile_df = IsaTabDataFrame(csv)
    if factor_filter:
        log.debug("Filtering DataFrame contents on Factor Value %s", factor_filter)
        return tfile_df[tfile_df['Factor Value[{}]'.format(factor_filter[0])] == factor_filter[1]]
    return tfile_df


def read_investigation_file(fp):
    """Reads an investigation file into a dictionary of DataFrames, each
    DataFrame being each section of the investigation file. e.g. One DataFrame
    for the INVESTIGATION PUBLICATIONS section

    :param fp: A file-like buffer object of the investigation file
    :return: A dictionary holding a set of DataFrames for each section of the
    investigation file. See below implementation for detail
    """
    return ISATabReader(fp).run()