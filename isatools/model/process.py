from logging import getLogger

from isatools.model.comments import Commentable
from isatools.model.process_sequence import ProcessSequenceNode
from isatools.model.protocol import Protocol
from isatools.model.material import Material
from isatools.model.source import Source
from isatools.model.sample import Sample
from isatools.model.datafile import DataFile
from isatools.model.parameter_value import ParameterValue
from isatools.model.identifiable import Identifiable
from isatools.model.ontology_annotation import OntologyAnnotation
from isatools.model.loader_indexes import loader_states as indexes

log = getLogger('isatools')


class Process(Commentable, ProcessSequenceNode, Identifiable):
    """Process nodes represent the application of a protocol to some input
    material (e.g. a Source) to produce some output (e.g.a Sample).

    Attributes:
        name : If relevant, a unique name for the process to disambiguate it
            from other processes.
        executes_protocol: A reference to the Protocol that this process
            executes.
        date_: A date formatted as an ISO8601 string corresponding to when the
            process event occurred.
        performer: The name of the person or organisation that carried out the
            process.
        parameter_values: A list of ParameterValues relevant to the executing
            protocol.
        inputs: A list of input materials, possibly Sources, Samples,
            Materials, DataFiles
        outputs: A list of output materials, possibly Samples, Materials,
            DataFiles
        comments: Comments associated with instances of this class.
    """

    # TODO: replace with above but need to debug where behaviour starts varying

    def __init__(self, id_='', name=None, executes_protocol=None, date_=None,
                 performer=None, parameter_values=None, inputs=None,
                 outputs=None, comments=None):
        Commentable.__init__(self, comments)
        ProcessSequenceNode.__init__(self)
        Identifiable.__init__(self)

        self.id = id_
        self.name = ''
        if name:
            self.__name = name

        if executes_protocol is None:
            self.__executes_protocol = Protocol()
        else:
            self.__executes_protocol = executes_protocol

        self.__date = date_
        self.__performer = performer

        if parameter_values is None:
            self.__parameter_values = []
        else:
            self.__parameter_values = parameter_values

        if inputs is None:
            self.__inputs = []
        else:
            self.__inputs = inputs

        if outputs is None:
            self.__outputs = []
        else:
            self.__outputs = outputs

        self.__prev_process = None
        self.__next_process = None

    @property
    def name(self):
        """:obj:`str`: disambiguation name for the process"""
        return self.__name

    @name.setter
    def name(self, val):
        if val is not None and isinstance(val, str):
            self.__name = val
        else:
            raise AttributeError('Process.name must be a string')

    @property
    def executes_protocol(self):
        """:obj:`Protocol`: a references to the study protocol the process has
        applied"""
        return self.__executes_protocol

    @executes_protocol.setter
    def executes_protocol(self, val):
        if val is not None and not isinstance(val, Protocol):
            raise AttributeError('Process.executes_protocol must be a Protocol or None; got {0}:{1}'
                                 .format(val, type(val)))
        self.__executes_protocol = val

    @property
    def date(self):
        """:obj:`str`: date the process event occurred"""
        return self.__date

    @date.setter
    def date(self, val):
        if val is not None and isinstance(val, str):
            self.__date = val
        else:
            raise AttributeError('Process.date must be a string')

    @property
    def performer(self):
        """:obj:`str`: name of the performer responsible for the process"""
        return self.__performer

    @performer.setter
    def performer(self, val):
        if val is not None and isinstance(val, str):
            self.__performer = val
        else:
            raise AttributeError('Process.performer must be a string')

    @property
    def parameter_values(self):
        """:obj:`list` of :obj:`ParameterValue`: Container for
        process parameter values"""
        return self.__parameter_values

    @parameter_values.setter
    def parameter_values(self, val):
        if val is not None and hasattr(val, '__iter__'):
            if val == [] or all(isinstance(x, ParameterValue) for x in val):
                self.__parameter_values = list(val)
        else:
            raise AttributeError('Process.parameter_values must be iterable containing ParameterValues')

    @property
    def inputs(self):
        """:obj:`list` of :obj:`Material` or :obj:`DataFile`: Container for
        process inputs"""
        return self.__inputs

    @inputs.setter
    def inputs(self, val):
        if val is not None and hasattr(val, '__iter__'):
            if val == [] or all(isinstance(x, (Material, Source, Sample, DataFile)) for x in val):
                self.__inputs = list(val)
        else:
            raise AttributeError('Process.inputs must be iterable containing objects of types '
                                 '(Material, Source, Sample, DataFile)')

    @property
    def outputs(self):
        """:obj:`list` of :obj:`Material` or :obj:`DataFile`: Container for
        process outputs"""
        return self.__outputs

    @outputs.setter
    def outputs(self, val):
        if val is not None and hasattr(val, '__iter__'):
            if val == [] or all(isinstance(x, (Material, Source, Sample, DataFile)) for x in val):
                self.__outputs = list(val)
        else:
            raise AttributeError(
                'Process.outputs must be iterable containing objects of types '
                '(Material, Source, Sample, DataFile)')

    @property
    def prev_process(self):
        """:obj:`Process`: a reference to another process, previous in the
        process sequence to the current process"""
        return self.__prev_process

    @prev_process.setter
    def prev_process(self, val):
        if val is not None and not isinstance(val, Process):
            raise AttributeError(
                'Process.prev_process must be a Process '
                'or None; got {0}:{1}'.format(val, type(val)))
        else:
            self.__prev_process = val

    @property
    def next_process(self):
        """:obj:`Process`: a reference to another process, next in the process
        sequence to the current process"""
        return self.__next_process

    @next_process.setter
    def next_process(self, val):
        if val is not None and not isinstance(val, Process):
            raise AttributeError(
                'Process.next_process must be a Process '
                'or None; got {0}:{1}'.format(val, type(val))
            )
        else:
            self.__next_process = val

    def __repr__(self):
        return ('{0}.{1}(id="{2.id}". name="{2.name}", executes_protocol={2.executes_protocol}, '
                'date="{2.date}", performer="{2.performer}", inputs={2.inputs}, outputs={2.outputs}'
                ')').format(self.__class__.__module__, self.__class__.__name__, self)

    def __str__(self):
        return """{0}(name={1.name})""".format(self.__class__.__name__, self)

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, Process) \
               and self.id == other.id \
               and self.name == other.name \
               and self.executes_protocol == other.executes_protocol \
               and self.date == other.date \
               and self.performer == other.performer \
               and self.inputs == other.inputs \
               and self.outputs == other.outputs

    def __ne__(self, other):
        return not self == other

    def to_dict(self, ld=False):
        parameter_values = []
        for param in self.parameter_values:
            value = ''
            if param.value:
                value = param.value.to_dict(ld=ld) if isinstance(param.value, OntologyAnnotation) else param.value
            parameter_value = {
                "category": {"@id": param.category.id} if param.category else '',
                "value": value
            }
            if param.unit:
                parameter_value["unit"] = {"@id": param.unit.id}
            parameter_values.append(parameter_value)
        serialized = {
            "@id": self.id,
            "name": self.name if self.name is not None else '',
            "performer": self.performer if self.performer is not None else '',
            "date": self.date if self.date is not None else '',
            "executesProtocol": {"@id": self.executes_protocol.id},
            "parameterValues": parameter_values,
            "inputs": [{'@id': x.id} for x in self.inputs],
            "outputs": [{'@id': x.id} for x in self.outputs],
            "comments": [comment.to_dict(ld=ld) for comment in self.comments]
        }
        if self.prev_process:
            serialized['previousProcess'] = {'@id': self.prev_process.id}
        if self.next_process:
            serialized['nextProcess'] = {'@id': self.next_process.id}
        return self.update_isa_object(serialized, ld)

    def from_dict(self, process):
        self.id = process.get('@id', '')
        self.executes_protocol = indexes.get_protocol(process['executesProtocol']['@id'])
        self.load_comments(process.get('comments', []))
        self.name = process.get('name', '')
        self.performer = process.get('performer', '')
        self.date = process.get('date', '')

        # parameter values
        for parameter_value_data in process.get('parameterValues', []):
            parameter_value = ParameterValue()
            parameter_value.from_dict(parameter_value_data)
            self.parameter_values.append(parameter_value)

        # Inputs
        for input_data in process.get('inputs', []):
            input_ = None
            try:
                input_ = indexes.get_source(input_data["@id"])
            except KeyError:
                pass
            finally:
                try:
                    input_ = indexes.get_sample(input_data["@id"])
                except KeyError:
                    pass
            if input_ is None:
                raise IOError("Could not find input node in sources or samples dicts: " + input_data["@id"])
            self.inputs.append(input_)

        # Outputs
        for output_data in process.get('outputs', []):
            output = None
            try:
                output = indexes.get_source(output_data["@id"])
            except KeyError:
                pass
            finally:
                try:
                    output = indexes.get_sample(output_data["@id"])
                except KeyError:
                    pass
            if output is None:
                raise IOError("Could not find output node in sources or samples dicts: " + output_data["@id"])
            self.outputs.append(output)

    def from_assay_dict(self, process, technology_type):
        self.id = process.get('@id', '')
        self.executes_protocol = indexes.get_protocol(process['executesProtocol']['@id'])
        self.load_comments(process.get('comments', []))
        # TODO: move to constants.py
        allowed_protocol_type_terms = [
            "nucleic acid sequencing",
            "nmr spectroscopy",
            "mass spectrometry",
            "nucleic acid hybridization",
            "data transformation",
            "data normalization"
        ]
        if self.executes_protocol.protocol_type.term in allowed_protocol_type_terms or (
                self.executes_protocol.protocol_type.term == 'data collection'
                and technology_type.term == 'DNA microarray'):
            self.name = process['name']

        # Inputs / Outputs
        for io_data_target in ['inputs', 'outputs']:
            for io_data in process.get(io_data_target, []):
                io_value = None
                try:
                    io_value = indexes.get_sample(io_data["@id"])
                except KeyError:
                    pass
                finally:
                    try:
                        io_value = indexes.get_other_material(io_data["@id"])
                    except KeyError:
                        pass
                    finally:
                        try:
                            io_value = indexes.get_data_file(io_data["@id"])
                        except KeyError:
                            pass
                if io_value is None:
                    error_msg = "Could not find %s node in samples or materials or data " \
                                "dicts: %s" % (io_data_target.replace('s', ''), io_data["@id"])
                    raise IOError(error_msg)
                getattr(self, io_data_target).append(io_value)

        # Parameter values
        for parameter_value_data in process.get('parameterValues', []):
            if "category" not in parameter_value_data.keys():
                log.warning("warning: parameter category not found for instance %s" % parameter_value_data)
            else:
                if parameter_value_data["category"]["@id"] == "#parameter/Array_Design_REF":  # Special case
                    self.array_design_ref = parameter_value_data["value"]
                elif isinstance(parameter_value_data["value"], int) or isinstance(parameter_value_data["value"], float):
                    parameter_value = ParameterValue(
                        category=indexes.get_parameter(parameter_value_data["category"]["@id"]),
                        value=parameter_value_data["value"]
                    )
                    parameter_value.load_comments(parameter_value_data.get('comments', []))
                    if 'unit' in parameter_value_data.keys():
                        parameter_value.unit = indexes.get_unit(parameter_value_data['unit']['@id'])
                    self.parameter_values.append(parameter_value)
                else:
                    parameter_value = ParameterValue()
                    parameter_value.from_dict(parameter_value_data)
                    self.parameter_values.append(parameter_value)
