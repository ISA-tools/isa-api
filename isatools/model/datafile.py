from isatools.model.comments import Commentable
from isatools.model.sample import Sample
from isatools.model.process_sequence import ProcessSequenceNode
from isatools.model.identifiable import Identifiable


class DataFile(Commentable, ProcessSequenceNode, Identifiable):
    """Represents a data file in an experimental graph.

    Attributes:
        filename : A name/reference for the data file.
        label: The data file type, as indicated by a label such as
            'Array Data File' or 'Raw Data File'
        generated_from: Reference to Sample(s) the DataFile is generated from
        comments: Comments associated with instances of this class.
    """

    def __init__(self, filename='', id_='', label='', generated_from=None, comments=None):
        # super().__init__(comments)
        Commentable.__init__(self, comments)
        ProcessSequenceNode.__init__(self)
        Identifiable.__init__(self)

        self.id = id_
        self.__filename = filename
        self.__label = label

        self.__generated_from = []
        if generated_from:
            self.__generated_from = generated_from

    @property
    def filename(self):
        """:obj:`str`: the filename of the data file"""
        return self.__filename

    @filename.setter
    def filename(self, val):
        if val is not None and not isinstance(val, str):
            raise AttributeError('{0}.name must be a str or None; got {1}:{2}'
                                 .format(type(self).__name__, val, type(val)))
        self.__filename = val

    @property
    def label(self):
        """:obj:`str`: the ISA-Tab file heading label of the data file"""
        return self.__label

    @label.setter
    def label(self, val):
        if val is not None and not isinstance(val, str):
            raise AttributeError(
                '{0}.label must be a str or None; got {1}:{2}'
                    .format(type(self).__name__, val, type(val)))
        else:
            self.__label = val

    @property
    def generated_from(self):
        """:obj:`list` of :obj:`Sample`: a list of references from this data
        file to samples that the file was generated from"""
        return self.__generated_from

    @generated_from.setter
    def generated_from(self, val):
        if val is not None and hasattr(val, '__iter__'):
            if val == [] or all(isinstance(x, Sample) for x in val):
                self.__generated_from = list(val)
        else:
            raise AttributeError('{0}.generated_from must be iterable containing Samples'.format(type(self).__name__))

    def __repr__(self):
        return "isatools.model.DataFile(filename='{data_file.filename}', " \
               "label='{data_file.label}', " \
               "generated_from={data_file.generated_from}, " \
               "comments={data_file.comments})" \
            .format(data_file=self)

    def __str__(self):
        return ("DataFile(\n\t"
                "filename={data_file.filename}\n\t"
                "label={data_file.label}\n\t"
                "generated_from={num_generated_from} Sample objects\n\t"
                "comments={num_comments} Comment objects\n)"
                ).format(data_file=self, num_generated_from=len(self.generated_from), num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, DataFile) \
               and self.filename == other.filename \
               and self.label == other.label \
               and self.generated_from == other.generated_from \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other

    def to_dict(self, ld=False):
        data_file = {
            "@id": self.id,
            "name": self.filename,
            "type": self.label,
            "comments": [comment.to_dict(ld=ld) for comment in self.comments]
        }
        return self.update_isa_object(data_file, ld)

    def from_dict(self, data_file):
        self.id = data_file.get('@id', '')
        self.filename = data_file.get('name', '')
        self.label = data_file.get('type', '')
        self.load_comments(data_file.get('comments', []))

        # TODO : missing generated_from property in dump/load methods


class RawDataFile(DataFile):
    """Represents a raw data file in an experimental graph."""

    def __init__(self, filename='', id_='',
                 generated_from=None, comments=None):
        super().__init__(filename=filename, id_=id_,
                         generated_from=generated_from, comments=comments)

        self.label = 'Raw Data File'

    def __repr__(self):
        return "isatools.model.RawDataFile(filename='{data_file.filename}', " \
               "generated_from={data_file.generated_from}, " \
               "comments={data_file.comments})".format(data_file=self)

    def __str__(self):
        return """RawDataFile(
    filename={data_file.filename}
    generated_from={num_generated_from} Sample objects
    comments={num_comments} Comment objects
)""".format(data_file=self, num_generated_from=len(self.generated_from),
            num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, RawDataFile) \
               and self.filename == other.filename \
               and self.generated_from == other.generated_from \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other


class DerivedDataFile(DataFile):
    """Represents a derived data file in an experimental graph."""

    def __init__(self, filename='', id_='',
                 generated_from=None, comments=None):
        super().__init__(filename=filename, id_=id_,
                         generated_from=generated_from, comments=comments)

        self.label = 'Derived Data File'

    def __repr__(self):
        return "isatools.model.DerivedDataFile(" \
               "filename='{data_file.filename}', " \
               "generated_from={data_file.generated_from}, " \
               "comments={data_file.comments})".format(data_file=self)

    def __str__(self):
        return """DerivedDataFile(
    filename={data_file.filename}
    generated_from={num_generated_from} Sample objects
    comments={num_comments} Comment objects
)""".format(data_file=self, num_generated_from=len(self.generated_from),
            num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, DerivedDataFile) \
               and self.filename == other.filename \
               and self.generated_from == other.generated_from \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other


class RawSpectralDataFile(DataFile):
    """Represents a raw spectral data file in an experimental graph."""

    def __init__(self, filename='', id_='',
                 generated_from=None, comments=None):
        super().__init__(filename=filename, id_=id_,
                         generated_from=generated_from, comments=comments)

        self.label = 'Raw Spectral Data File'

    def __repr__(self):
        return "isatools.model.RawSpectralDataFile(filename='{0.filename}', " \
               "generated_from={0.generated_from}, comments={0.comments})" \
            .format(self)

    def __str__(self):
        return """RawSpectralDataFile(
    filename={data_file.filename}
    generated_from={num_generated_from} Sample objects
    comments={num_comments} Comment objects
)""".format(data_file=self, num_generated_from=len(self.generated_from),
            num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, RawSpectralDataFile) \
               and self.filename == other.filename \
               and self.generated_from == other.generated_from \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other


class DerivedArrayDataFile(DataFile):
    """Represents a derived array data file in an experimental graph."""

    def __init__(self, filename='', id_='',
                 generated_from=None, comments=None):
        super().__init__(filename=filename, id_=id_,
                         generated_from=generated_from, comments=comments)

        self.label = 'Derived Array Data File'

    def __repr__(self):
        return "isatools.model.DerivedArrayDataFile(" \
               "filename='{data_file.filename}', " \
               "generated_from={data_file.generated_from}, " \
               "comments={data_file.comments})".format(data_file=self)

    def __str__(self):
        return """DerivedArrayDataFile(
    filename={data_file.filename}
    generated_from={num_generated_from} Sample objects
    comments={num_comments} Comment objects
)""".format(data_file=self, num_generated_from=len(self.generated_from),
            num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, DerivedArrayDataFile) \
               and self.filename == other.filename \
               and self.generated_from == other.generated_from \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other


class ArrayDataFile(DataFile):
    """Represents a array data file in an experimental graph."""

    def __init__(self, filename='', id_='',
                 generated_from=None, comments=None):
        super().__init__(filename=filename, id_=id_,
                         generated_from=generated_from, comments=comments)

        self.label = 'Array Data File'

    def __repr__(self):
        return "isatools.model.ArrayDataFile(" \
               "filename='{data_file.filename}', " \
               "generated_from={data_file.generated_from}, " \
               "comments={data_file.comments})".format(data_file=self)

    def __str__(self):
        return """ArrayDataFile(
    filename={data_file.filename}
    generated_from={num_generated_from} Sample objects
    comments={num_comments} Comment objects
)""".format(data_file=self, num_generated_from=len(self.generated_from),
            num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, ArrayDataFile) \
               and self.filename == other.filename \
               and self.generated_from == other.generated_from \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other


class DerivedSpectralDataFile(DataFile):
    """Represents a derived spectral data file in an experimental graph."""

    def __init__(self, filename='', id_='',
                 generated_from=None, comments=None):
        super().__init__(filename=filename, id_=id_,
                         generated_from=generated_from, comments=comments)

        self.label = 'Derived Spectral Data File'

    def __repr__(self):
        return "isatools.model.DerivedSpectralDataFile(" \
               "filename='{data_file.filename}', " \
               "generated_from={data_file.generated_from}, " \
               "comments={data_file.comments})".format(data_file=self)

    def __str__(self):
        return """DerivedSpectralDataFile(
    filename={data_file.filename}
    generated_from={num_generated_from} Sample objects
    comments={num_comments} Comment objects
)""".format(data_file=self, num_generated_from=len(self.generated_from),
            num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, DerivedSpectralDataFile) \
               and self.filename == other.filename \
               and self.generated_from == other.generated_from \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other


class ProteinAssignmentFile(DataFile):
    """Represents a protein assignment file in an experimental graph."""

    def __init__(self, filename='', id_='',
                 generated_from=None, comments=None):
        super().__init__(filename=filename, id_=id_,
                         generated_from=generated_from, comments=comments)

        self.label = 'Protein Assignment File'

    def __repr__(self):
        return "isatools.model.ProteinAssignmentFile(" \
               "filename='{data_file.filename}', " \
               "generated_from={data_file.generated_from}, " \
               "comments={data_file.comments})".format(data_file=self)

    def __str__(self):
        return """ProteinAssignmentFile(
    filename={data_file.filename}
    generated_from={num_generated_from} Sample objects
    comments={num_comments} Comment objects
)""".format(data_file=self, num_generated_from=len(self.generated_from),
            num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, ProteinAssignmentFile) \
               and self.filename == other.filename \
               and self.generated_from == other.generated_from \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other


class PeptideAssignmentFile(DataFile):
    """Represents a peptide assignment file in an experimental graph."""

    def __init__(self, filename='', id_='',
                 generated_from=None, comments=None):
        super().__init__(filename=filename, id_=id_,
                         generated_from=generated_from, comments=comments)

        self.label = 'Peptide Assignment File'

    def __repr__(self):
        return "isatools.model.PeptideAssignmentFile(" \
               "filename='{data_file.filename}', " \
               "generated_from={data_file.generated_from}, " \
               "comments={data_file.comments})".format(data_file=self)

    def __str__(self):
        return """PeptideAssignmentFile(
    filename={data_file.filename}
    generated_from={num_generated_from} Sample objects
    comments={num_comments} Comment objects
)""".format(data_file=self, num_generated_from=len(self.generated_from),
            num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, PeptideAssignmentFile) \
               and self.filename == other.filename \
               and self.generated_from == other.generated_from \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other


class DerivedArrayDataMatrixFile(DataFile):
    """Represents a derived array data matrix file in an experimental graph."""

    def __init__(self, filename='', id_='',
                 generated_from=None, comments=None):
        super().__init__(filename=filename, id_=id_,
                         generated_from=generated_from, comments=comments)

        self.label = 'Derived Array Data Matrix File'

    def __repr__(self):
        return "isatools.model.DerivedArrayDataMatrixFile(" \
               "filename='{data_file.filename}', " \
               "generated_from={data_file.generated_from}, " \
               "comments={data_file.comments})".format(data_file=self)

    def __str__(self):
        return """DerivedArrayDataMatrixFile(
    filename={data_file.filename}
    generated_from={num_generated_from} Sample objects
    comments={num_comments} Comment objects
)""".format(data_file=self, num_generated_from=len(self.generated_from),
            num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, DerivedArrayDataMatrixFile) \
               and self.filename == other.filename \
               and self.generated_from == other.generated_from \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other


class PostTranslationalModificationAssignmentFile(DataFile):
    """Represents a post translational modification assignment file in an
    experimental graph."""

    def __init__(self, filename='', id_='',
                 generated_from=None, comments=None):
        super().__init__(filename=filename, id_=id_,
                         generated_from=generated_from, comments=comments)

        self.label = 'Post Translational Modification Assignment File'

    def __repr__(self):
        return "isatools.model.PostTranslationalModificationAssignmentFile(" \
               "filename='{data_file.filename}', " \
               "generated_from={data_file.generated_from}, " \
               "comments={data_file.comments})".format(data_file=self)

    def __str__(self):
        return """PostTranslationalModificationAssignmentFile(
    filename={data_file.filename}
    generated_from={num_generated_from} Sample objects
    comments={num_comments} Comment objects
)""".format(data_file=self, num_generated_from=len(self.generated_from),
            num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, PostTranslationalModificationAssignmentFile) \
               and self.filename == other.filename \
               and self.generated_from == other.generated_from \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other


class AcquisitionParameterDataFile(DataFile):
    """Represents a acquisition parameter data file in an experimental
    graph."""

    def __init__(self, filename='', id_='',
                 generated_from=None, comments=None):
        super().__init__(filename=filename, id_=id_,
                         generated_from=generated_from, comments=comments)

        self.label = 'Acquisition Parameter Data File'

    def __repr__(self):
        return "isatools.model.AcquisitionParameterDataFile(" \
               "filename='{data_file.filename}', " \
               "generated_from={data_file.generated_from}, " \
               "comments={data_file.comments})".format(data_file=self)

    def __str__(self):
        return """AcquisitionParameterDataFile(
    filename={data_file.filename}
    generated_from={num_generated_from} Sample objects
    comments={num_comments} Comment objects
)""".format(data_file=self, num_generated_from=len(self.generated_from),
            num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, AcquisitionParameterDataFile) \
               and self.filename == other.filename \
               and self.generated_from == other.generated_from \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other


class FreeInductionDecayDataFile(DataFile):
    """Represents a free induction decay data file in an experimental graph."""

    def __init__(self, filename='', id_='',
                 generated_from=None, comments=None):
        super().__init__(filename=filename, id_=id_,
                         generated_from=generated_from, comments=comments)

        self.label = 'Free Induction Decay Data File'

    def __repr__(self):
        return "isatools.model.FreeInductionDecayDataFile(" \
               "filename='{data_file.filename}', " \
               "generated_from={data_file.generated_from}, " \
               "comments={data_file.comments})".format(data_file=self)

    def __str__(self):
        return """FreeInductionDecayDataFile(
    filename={data_file.filename}
    generated_from={num_generated_from} Sample objects
    comments={num_comments} Comment objects
)""".format(data_file=self, num_generated_from=len(self.generated_from),
            num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, FreeInductionDecayDataFile) \
               and self.filename == other.filename \
               and self.generated_from == other.generated_from \
               and self.comments == other.comments

    def __ne__(self, other):
        return not self == other
