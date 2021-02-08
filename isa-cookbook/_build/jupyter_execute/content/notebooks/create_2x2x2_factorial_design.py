# Create an ISA Study representing a 2x2x2 factorial design with single measurements

## Abstract:

In this notebook, we'll show how a study design defines a series of interventions with two distinct radiological agents, at two distinct dose levels and 2 distinct timepoints of observation post-exposure.

|Factor Name|Factor Type|Factor Value|Unit| Factor Value|Unit|Number of factor levels|
|:---|:---|:---|:---:|:---|:---:|---:|
|radionucleide|radiological agent|Cs 137| |Fe 56|| 2 |
|dose|intensity | 2.5 | cGy | 10 | cGy | 2 |
|time post exposure| time| 1 | hr | 72 | hr | 2 |

In this experiment, *muscle* samples are collected once from each study subject (n=10 per group) and `metabolite profiling` using `1D 13C NMR` is performed on the `supernatant` and `pellet` of the extracted fraction.
Subjects were also `phenotyped using a custom hyperspectral imaging`.


### Let's get the toolkit

# If executing the notebooks on `Google Colab`,uncomment the following command 
# and run it to install the required python libraries. Also, make the test datasets available.

# !pip install -r requirements.txt

import pandas as pd
import datetime as dt
import json

from isatools.model import (Investigation, Study,StudyFactor,FactorValue, Assay, Person, Material,
                            DataFile, plink,
                            OntologySource, OntologyAnnotation, Sample,
                            Source, Characteristic, Protocol,ProtocolParameter, Process)

from isatools.create.model import (Treatment,StudyCell,StudyArm,ProductNode,OrderedDict,ProductNode,ProtocolNode)

from isatools.isajson import ISAJSONEncoder


### Creating the ISA Study core metadata

investigation = Investigation()
study = Study(filename="s_study_2by2by2.txt")
study.identifier = "2x2x2"
study.title = "2x2x2 factorial design study"
study.description = "a simple full factorial design study 2x2x2"
study.submission_date = "2021-04-21" # Note the ISO8601 format for dates
study.public_release_date = "2021-05-30"  # Note the ISO8601 format for dates
study.protocols = [Protocol(name="sample collection")]
investigation.studies = [study]
print(investigation)


print(json.dumps(investigation, cls=ISAJSONEncoder, sort_keys=True, indent=4, separators=(',', ': ')))

### Let's build the ISA Study Design Object

#### Declaring the 3 independent variables (ISA Factors) of the Study

f1 = StudyFactor(name='radionucleide', factor_type=OntologyAnnotation(term="radiological agent"))
f2 = StudyFactor(name='dose', factor_type=OntologyAnnotation(term="intensity"))
f3 = StudyFactor(name='time post exposure', factor_type=OntologyAnnotation(term="time"))

#### Declaring the treatment groups

te1 = Treatment()
te1.type='radiological intervention'

f1v1 = FactorValue(factor_name=f1, value=OntologyAnnotation(term="Cs 137"))
f2v1 = FactorValue(factor_name=f2, value=2.5, unit=OntologyAnnotation(term='cGy'))
f3v1 = FactorValue(factor_name=f3, value=1, unit=OntologyAnnotation(term='hr'))

te1.factor_values = (f1v1,f2v1,f3v1)
# te1.factor_values.add(f1v1)

te6 = Treatment()
te6.type='radiological intervention'

f1v1 = FactorValue(factor_name=f1, value=OntologyAnnotation(term="Cs 137"))
f2v1 = FactorValue(factor_name=f2, value=2.5,unit=OntologyAnnotation(term='cGy'))
f3v2 = FactorValue(factor_name=f3, value=72, unit=OntologyAnnotation(term='hr'))

te6.factor_values = (f1v1,f2v1,f3v2)

te2 = Treatment()
te2.type='radiological intervention'

f1v1 = FactorValue(factor_name=f1, value=OntologyAnnotation(term="Cs 137"))
f2v2 = FactorValue(factor_name=f2, value=10,unit=OntologyAnnotation(term='cGy'))
f3v2 = FactorValue(factor_name=f3, value=72, unit=OntologyAnnotation(term='hr'))

te2.factor_values = (f1v1,f2v2,f3v2)

te7 = Treatment()
te7.type='radiological intervention'

f1v2 = FactorValue(factor_name=f1, value=OntologyAnnotation(term="Cs 137"))
f2v1 = FactorValue(factor_name=f2, value=10,unit=OntologyAnnotation(term='cGy'))
f3v2 = FactorValue(factor_name=f3, value=72, unit=OntologyAnnotation(term='hr'))

te7.factor_values = (f1v2,f2v1,f3v2)

te3 = Treatment()
te3.type='radiological intervention'

f1v2 = FactorValue(factor_name=f1, value=OntologyAnnotation(term="Fe 56"))
f2v1 = FactorValue(factor_name=f2, value=2.5,unit=OntologyAnnotation(term='cGy'))
f3v1 = FactorValue(factor_name=f3, value=1, unit=OntologyAnnotation(term='hr'))

te3.factor_values = (f1v2,f2v1,f3v1)

te5 = Treatment()
te5.type='radiological intervention'

f1v2 = FactorValue(factor_name=f1, value=OntologyAnnotation(term="Fe 56"))
f2v1 = FactorValue(factor_name=f2, value=2.5,unit=OntologyAnnotation(term='cGy'))
f3v2 = FactorValue(factor_name=f3, value=72, unit=OntologyAnnotation(term='hr'))

te5.factor_values = (f1v2,f2v1,f3v2)

te8 = Treatment()
te8.type='radiological intervention'

f1v2 = FactorValue(factor_name=f1, value=OntologyAnnotation(term="Fe 56"))
f2v2 = FactorValue(factor_name=f2, value=10,unit=OntologyAnnotation(term='cGy'))
f3v1 = FactorValue(factor_name=f3, value=1, unit=OntologyAnnotation(term='hr'))

te8.factor_values = (f1v2,f2v2,f3v1)

te4 = Treatment()
te4.type='radiological intervention'

f1v2 = FactorValue(factor_name=f1, value=OntologyAnnotation(term="Fe 56"))
f2v2 = FactorValue(factor_name=f2, value=10,unit=OntologyAnnotation(term='cGy'))
f3v2 = FactorValue(factor_name=f3, value=72, unit=OntologyAnnotation(term='hr'))

te4.factor_values = (f1v2,f2v2,f3v2)

#### Now building the Study Arms

st_cl1= StudyCell(name="st_cl1", elements=[te1])
st_cl2= StudyCell(name="st_cl2", elements=[te2])
st_cl3= StudyCell(name="st_cl3", elements=[te3])
st_cl4= StudyCell(name="st_cl4", elements=[te4])
st_cl5= StudyCell(name="st_cl5", elements=[te5])
st_cl6= StudyCell(name="st_cl6", elements=[te6])
st_cl7= StudyCell(name="st_cl7", elements=[te7])
st_cl8= StudyCell(name="st_cl8", elements=[te8])


arm1 = StudyArm(name='Group 1', group_size=10, source_type=Characteristic(category=OntologyAnnotation(term="Study Subject"),value=OntologyAnnotation(term="Mus musculus")))
arm2 = StudyArm(name='Group 2', group_size=10)
arm3 = StudyArm(name='Group 3', group_size=10)
arm4 = StudyArm(name='Group 4', group_size=10)
arm5 = StudyArm(name='Group 5', group_size=10)
arm6 = StudyArm(name='Group 6', group_size=10)
arm7 = StudyArm(name='Group 7', group_size=10)
arm8 = StudyArm(name='Group 8', group_size=10)

input_material1=ProductNode(id_="MAT1", name="muscle tissue", node_type=SAMPLE,size=1,characteristics=[Characteristic(category=OntologyAnnotation(term='organism part'), value=OntologyAnnotation(term='muscle'))])
#input_material2=ProductNode(id_="MAT2", name="blood", node_type=SAMPLE,size=1,characteristics=[Characteristic(category='organism part', value='blood')])

#### A new data structure for defining an assay workflow

The following cells show 2 distinct assay workflows, which are consumed by the `ISAcreate module` of the ISA-API to drive to creation of ISA objects. In this notebook, we show how the data structure can be used to pass workflow settings.  Each `Protocol Node` can be used to specify the number of technical replicates and parameter settings for each data acquisition to be executed. Note how these values are `OntologyAnnotation` and therefore can be marked up with URI.

nmr_assay_dict = OrderedDict([
    ('measurement_type', OntologyAnnotation(term='metabolite profiling')),
    ('technology_type', OntologyAnnotation(term='nmr spectroscopy')),
            ('extraction', {}),
            ('extract', [
                {
                    'node_type': EXTRACT,
                    'characteristics_category':  OntologyAnnotation(term='extract type'),
                    'characteristics_value': OntologyAnnotation(term='supernatant'),
                    'size': 1,
                    'technical_replicates': None,
                    'is_input_to_next_protocols': True
                },
                {
                    'node_type': EXTRACT,
                    'characteristics_category':  OntologyAnnotation(term='extract type'),
                    'characteristics_value': OntologyAnnotation(term='pellet'),
                    'size': 1,
                    'technical_replicates': None,
                    'is_input_to_next_protocols': True
                }
            ]),
            ('nmr_spectroscopy', {
                OntologyAnnotation(term='instrument'): [OntologyAnnotation(term='Bruker AvanceII 1 GHz')],
                OntologyAnnotation(term='acquisition_mode'): [OntologyAnnotation(term='1D 13C NMR')],
                OntologyAnnotation(term='pulse_sequence'): [OntologyAnnotation(term='CPMG')]
            }),
            ('raw_spectral_data_file', [
                {
                    'node_type': DATA_FILE,
                    'size': 1,
                    'technical_replicates': 2,
                    'is_input_to_next_protocols': False
                }
            ])
        ])

custom_nasa_lab_dict = OrderedDict([
        ('measurement_type', OntologyAnnotation(term='phenotyping')),
        ('technology_type', OntologyAnnotation(term='hyperspectral imaging')),
                ('hyperspectral imaging', {
                OntologyAnnotation(term='instrument'): [OntologyAnnotation(term='Hitachi ZBR-II')],
                OntologyAnnotation(term='acquisition_mode'): [OntologyAnnotation(term='multimodal')],
                OntologyAnnotation(term='wavelength'): [OntologyAnnotation(term='near-IR'),OntologyAnnotation(term='far-IR'),OntologyAnnotation(term='UV')]
            }),
            ('raw_spectral_data_file', [
                {
                    'node_type': DATA_FILE,
                    'size': 1,
                    'technical_replicates': 2,
                    'is_input_to_next_protocols': False
                }
            ])
])

nmr_assay_graph = AssayGraph.generate_assay_plan_from_dict(nmr_assay_dict)
interspersed_sample_node = ProductNode(node_type=SAMPLE, name="sample qc", 
                                       size=2,characteristics=(
                                           Characteristic(category='dilution', value=10, unit='ml'),
                                       ))
pre_run_sample_node = ProductNode(node_type=SAMPLE, 
                                  name="pre run qc",
                                  size=2,
                                  characteristics=(
                                      Characteristic(category='dilution', value=10, unit='ml'),
                                  ))

qc_object = QualityControl(interspersed_sample_type=[(interspersed_sample_node, 10)], 
                           pre_run_sample_type=pre_run_sample_node)


nmr_assay_graph.quality_control=qc_object

sap1 = SampleAndAssayPlan(name="sap1" , sample_plan=[input_material1],assay_plan=[nmr_assay_graph])
 
sample2assay_plan={input_material1: [nmr_assay_graph]}

sap1.sample_to_assay_map=sample2assay_plan

sorted(sap1.assay_plan)[0].quality_control

#### Associating each `study arm` with the `study cell` and its `sample to assay plan`

arm1.add_item_to_arm_map(st_cl1,sap1)
arm2.add_item_to_arm_map(st_cl2,sap1)
arm3.add_item_to_arm_map(st_cl3,sap1)
arm4.add_item_to_arm_map(st_cl4,sap1)
arm5.add_item_to_arm_map(st_cl5,sap1)
arm6.add_item_to_arm_map(st_cl6,sap1)
arm7.add_item_to_arm_map(st_cl7,sap1)
arm8.add_item_to_arm_map(st_cl8,sap1)

#### Adding all the `study arm` to the `study design` object

study_design= StudyDesign(name='parallel group design 2x2x2 #1')
study_design.add_study_arm(arm1)
study_design.add_study_arm(arm2)
study_design.add_study_arm(arm3)
study_design.add_study_arm(arm4)
study_design.add_study_arm(arm5)
study_design.add_study_arm(arm6)
study_design.add_study_arm(arm7)
study_design.add_study_arm(arm8)

#### Let's now serialize the ISA Study Design Object as a JSON document.

import json
from isatools.isajson import ISAJSONEncoder
from isatools.create.model import StudyDesignEncoder

f=json.dumps(study_design, cls=StudyDesignEncoder, sort_keys=True, indent=4, separators=(',', ': '))

#### Let's produce a graphical representation of the study groups and their size using python bokeh library

from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Range1d, BoxAnnotation, Label, Legend, LegendItem, LabelSet
from bokeh.models.tools import HoverTool
import holoviews as hv
from holoviews import opts, dim
hv.extension('bokeh')

def get_treatment_factors(some_element):
    treat = ""
    for j in range(len(some_element['factorValues'])):
        if j < len(some_element['factorValues']) - 1:
            if 'unit' in some_element['factorValues'][j].keys():
                treat = treat + some_element['factorValues'][j]['factor']['name'].lower() + ": " \
                        + str(some_element['factorValues'][j]['value']) + " " \
                        + str(some_element['factorValues'][j]['unit']['term'].lower()) + ", "
            else:
                treat = treat + some_element['factorValues'][j]['factor']['name'].lower() + ": " \
                        + str(some_element['factorValues'][j]['value']) + ","
        else:
            if 'unit' in some_element['factorValues'][j].keys():
                treat = treat + some_element['factorValues'][j]['factor']['name'].lower() + ": " \
                        + str(some_element['factorValues'][j]['value']) + " " \
                        + str(some_element['factorValues'][j]['unit']['term'].lower())
            else:
                treat = treat + some_element['factorValues'][j]['factor']['name'].lower() + ": " \
                        + str(some_element['factorValues'][j]['value'])

    return treat

design = json.loads(json.dumps(study_design, cls=StudyDesignEncoder, sort_keys=True, indent=4, separators=(',', ': ')))
frames = []
Items = []

# defining a color pallet for the different element types:
element_colors = {"biological intervention": "rgb(253,232,37)",
                  "radiological intervention": "rgb(53, 155, 8)",
                  "dietary intervention": "rgb(53, 155, 8)",
                  "chemical intervention": "rgb(69, 13, 83)",
                  "washout": "rgb(45, 62, 120)",
                  "screen": "rgb(33, 144, 140)",
                  "run in": "rgb(43, 144, 180)",
                  "follow-up": "rgb(88, 189, 94)",
                  "concomitant treatment": "rgb(255, 255, 0)"}

# processing the study design arms and treatment plans:
for key in design["studyArms"].keys():
    DF = pd.DataFrame(columns=['Arm', 'Cell', 'Type', 'Start_date', 'End_date', 'Treatment', 'Color'])
    arm_name = key
    # print("arm: ", arm_name)
    size = design["studyArms"][key]["groupSize"]
    size_annotation = "n=" + str(size)

    cells_per_arm = design["studyArms"][key]["cells"]
    cell_counter = 0
    for cell in cells_per_arm:
        cell_name = cell['name']
        elements_per_cell = cell['elements']

        for element in elements_per_cell:
            treat = ""
            element_counter = 0                      
            if 'concomitantTreatments' in element.keys():
                element_counter = element_counter + 1
                treatments = []
                for item in element['concomitantTreatments']:
                    treatment = get_treatment_factors(item)
                    treatments.append(treatment)
                    
                concomitant = ','.join(treatments[0:-1])
                concomitant = concomitant + ' and ' + treatments[-1]
                array = [arm_name, cell_name, arm_name + ": [" + concomitant + "]_concomitant_" + str(cell_counter),
                     dt.datetime(cell_counter + 2000, 1, 1), dt.datetime(cell_counter + 2000 + 1, 1, 1),
                     str(element['factorValues']),
                     concomitant,
                     element_colors["concomitant treatment"]]
                Items.append(array)

            elif 'type' in element.keys():
                treatment = get_treatment_factors(element)
                element_counter = element_counter + 1
                array = [arm_name, cell_name, arm_name + ": [" + str(element['type']) + "]_" + str(cell_counter),
                         dt.datetime((cell_counter + 2000), 1, 1), dt.datetime((cell_counter + 2000 + 1), 1, 1),
                         # str(element['factorValues']),
                         str(treatment),
                         element_colors[element['type']]]
                Items.append(array)

            cell_counter = cell_counter + 1

for i, Dat in enumerate(Items):
    DF.loc[i] = Dat
#     print("setting:", DF.loc[i])

# providing the canvas for the figure
# print("THESE ARE THE TYPES_: ", DF.Type.tolist())
fig = figure(title='Study Design Treatment Plan',
             width=800,
             height=400,
             y_range=DF.Type.tolist(),
             x_range=Range1d(DF.Start_date.min(), DF.End_date.max()),
             tools='save')

# adding a tool tip
hover = HoverTool(tooltips="Task: @Type<br>\
Start: @Start_date<br>\
Cell_Name: @Cell<br>\
Treatment: @Treatment")
fig.add_tools(hover)

DF['ID'] = DF.index+0.8
# print("ID: ", DF['ID'])
DF['ID1'] = DF.index+1.2
# print("ID1: ", DF['ID1'])
CDS = ColumnDataSource(DF)
# , legend=str(size_annotation)
r = fig.quad(left='Start_date', right='End_date', bottom='ID', top='ID1', source=CDS, color="Color")
fig.xaxis.axis_label = 'Time'
fig.yaxis.axis_label = 'study arms'

# working at providing a background color change for every arm in the study design
counts = DF['Arm'].value_counts().tolist()
# print("total number of study arms:", len(counts), "| number of phases per arm:", counts)
# box = []
# for i, this_element in enumerate(DF['Arm']):
#     if i==0:
#         box[i] = BoxAnnotation(bottom=0,
#                              top=DF['Arm'].value_counts().tolist()[0],
#                              fill_color="blue")
#     elif i % 2 == 0:
#         box[i] = BoxAnnotation(bottom=DF['Arm'].value_counts().tolist()[0],
#                              top=DF['Arm'].value_counts().tolist()[0],
#                              fill_color="silver")
#     else:
#         box[i] = BoxAnnotation(bottom=DF['Arm'].value_counts().tolist()[0],
#                              top=DF['Arm'].value_counts().tolist()[0] + DF['Arm'].value_counts().tolist()[1],
#                              fill_color="grey",
#                              fill_alpha=0.1)
# # adding the background color for each arm:
# for element in box:
#     fig.add_layout(element)
# # fig.add_layout(box2)
# # fig.add_layout(legend,'right')

caption1 = Legend(items=[(str(size_annotation), [r])])
fig.add_layout(caption1, 'right')

citation = Label(x=10, y=-80, x_units='screen', y_units='screen',
                 text='parallel group design layout - isa-api 0.12', render_mode='css',
                 border_line_color='gray', border_line_alpha=0.4,
                 background_fill_color='white', background_fill_alpha=1.0)

fig.add_layout(citation)

show(fig)

### Let's now generate the full `ISA Study object` from the `ISA Study Design object`

This is done by invoking the new `generate_isa_study` method on the ISA `study design` object

study = study_design.generate_isa_study()

#### We can now check the objects which have been generated

investigation.studies=[study]

print(investigation.studies[0].assays[0])

#### We can also simply write to file either as ISA-Tab or as ISA-JSON

# WRITING ISA-JSON document
print(json.dumps(investigation, cls=ISAJSONEncoder, sort_keys=True, indent=4, separators=(',', ': ')))

from isatools import isatab
isatab.dump(investigation, './notebook-output/isa-2x2x2-single-measure-design')

#### One can also check out the tables as dataframes

from isatools.isatab import dump_tables_to_dataframes as dumpdf
dataframes = dumpdf(investigation)

dataframes.keys()

len(dataframes.keys())

dataframes[list(dataframes.keys())[1]]

#### or use the graph structure to count objects

[x for x in study.assays[0].graph.nodes() if isinstance(x, Sample)]

len([x for x in study.assays[0].graph.nodes() if isinstance(x, Sample)])

[getattr(x, 'name', None) for x in study.assays[0].graph.nodes()]

## About this notebook

- authors: philippe.rocca-serra@oerc.ox.ac.uk, massimiliano.izzo@oerc.ox.ac.uk
- license: CC-BY 4.0
- support: isatools@googlegroups.com
- issue tracker: https://github.com/ISA-tools/isa-api/issues