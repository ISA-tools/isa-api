# Create a repeated treatment design with ISA descriptor

This example creates `ISA study descriptor` for study with sequential treatments organized in an arm. 
This shows how to use objects from the `isatools.create` component in a granular fashion.
It creates each `Element` of the Study `Arm` at a time.

Finally, the `study design plan` is shown by serializing the `ISA Study Design Model` content as an  `ISA_design` JSON document, which can be rendered in various ways (tables, figures).

## Let's load the tools

import datetime
from isatools.model import *

from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Range1d, BoxAnnotation, Label, Legend, LegendItem, LabelSet
from bokeh.models.tools import HoverTool

import pandas as pd
import datetime as dt

import holoviews as hv
from holoviews import opts, dim
hv.extension('bokeh')


## Start by creating basic ISA Study metadata

investigation = Investigation()
study = Study(filename="s_study_xover.txt")
study.identifier = 'S-Xover-1'
study.title = 'My Simple ISA Study'
study.description = "We could alternataly use the class constructor's parameters to set some default " \
          "values at the time of creation, however we want to demonstrate how to use the " \
          "object's instance variables to set values."
study.submission_date = str(datetime.datetime.today())
study.public_release_date = str(datetime.datetime.today())
# study.sources = [Source(name="source1")]
# study.samples = [Sample(name="sample1")]
# study.protocols = [Protocol(name="sample collection")]
# study.process_sequence = [Process(executes_protocol=study.protocols[-1], inputs=[study.sources[-1]], outputs=[study.samples[-1]])]
investigation.studies = [study]
# investigation

# from isatools.isatab import dumps
# print(dumps(investigation))

import json
from isatools.isajson import ISAJSONEncoder
# print(json.dumps(investigation, cls=ISAJSONEncoder, sort_keys=True, indent=4, separators=(',', ': ')))

### Let's load the new ISA create module

from isatools.create.model import * 


### 1. Creation of the first `ISA Study Design Element` and setting its type

nte1 = NonTreatment(element_type='screen', duration_unit=OntologyAnnotation(term="days"))
print(nte1)

### 2. Creation of another `ISA Study Design Element`, of type `Treatment`

te1 = Treatment()
te1.type='biological intervention'
print(te1)

#### 2.1 defining the first treatment as a vector of ISA factor values:

Under "ISA Study Design Create mode", a `Study Design Element` of type `Treatment` needs to be defined by a vector of `Factors` and their respective associated `Factor Values`. This is done as follows:

f1 = StudyFactor(name='virus', factor_type=OntologyAnnotation(term="organism"))
f1v = FactorValue(factor_name=f1, value="hsv1")
f2 = StudyFactor(name='dose', factor_type=OntologyAnnotation(term="quantity"))
f2v = FactorValue(factor_name=f2, value='high dose')
f3 = StudyFactor(name='time post infection', factor_type=OntologyAnnotation(term="time"))
f3v = FactorValue(factor_name=f3, value=2, unit=OntologyAnnotation(term='hr'))


#assigning the factor values declared above to the ISA treatment element
te1.factor_values = [f1v,f2v,f3v]
print(te1)


### 3. Creation of a second  `ISA Study Design Element`, of type `Treatment`, following the same pattern.

te2 = Treatment()
te2.type = 'chemical intervention'
antivir = StudyFactor(name='antiviral', factor_type=OntologyAnnotation(term="chemical entity"))
antivirv = FactorValue(factor_name=antivir, value='hsvflumab')
intensity = StudyFactor(name='dose', factor_type=OntologyAnnotation(term="quantity"))
intensityv= FactorValue(factor_name=intensity, value = 10, unit=OntologyAnnotation(term='mg/kg/day'))
duration =  StudyFactor(name = 'treatment duration', factor_type=OntologyAnnotation(term="time"))
durationv = FactorValue(factor_name=duration, value=2, unit=OntologyAnnotation(term='weeks'))
te2.factor_values = [antivirv,intensityv,durationv]
print(te2)
                        
                        

te3 = Treatment()
te3.type = 'radiological intervention'
rays = StudyFactor(name='radiation', factor_type=OntologyAnnotation(term="physical entity"))
raysv = FactorValue(factor_name=rays, value='neutron beam')
rays_intensity = StudyFactor(name='dose', factor_type=OntologyAnnotation(term="quantity"))
rays_intensityv= FactorValue(factor_name=rays_intensity, value = '10', unit=OntologyAnnotation(term='mSev'))
rays_duration =  StudyFactor(name = 'treatment duration', factor_type=OntologyAnnotation(term="time"))
rays_durationv = FactorValue(factor_name=rays_duration, value='30', unit=OntologyAnnotation(term='minutes'))
te3.factor_values = [raysv,rays_intensityv,rays_durationv]
print(te3)
                

### 4. Creation of 'wash out' period as an `ISA Study Design Element`.

# Creation of another ISA element, which is not a Treatment element, which is of type `screen` by default
nte2 = NonTreatment(duration_unit=OntologyAnnotation(term="days"))
print(nte2.type)

# let's change it by setting its type by relying on the keys defined for the object
nte2.type=RUN_IN
print(nte2.type)

#let's change it again by direct use of the allowed strings (note: the string should match exactly the predefined values)
nte2.type = 'washout'
print(nte2.type)

# setting the factor values associated with 'default' DURATION Factor associated with such elements
nte2.duration.value=2
nte2.duration.unit=OntologyAnnotation(term="weeks")

### 5. Creation of 'follow-up' period as an `ISA Study Design Element`.

nte3 = NonTreatment(element_type=FOLLOW_UP, duration_value=4, duration_unit=OntologyAnnotation(term="month"))
# nte3.duration.value = 2
# nte3.duration.unit = 'months'
print(nte3)

### 6. Creation of the associated container, known as an ISA `Cell` for each ISA `Element`.
In this example, a single `Element` is hosted by a `Cell`, which must be named. In more complex designs (e.g. study designs with assymetric arms), a `Cell` may contain more than one `Element`, hence the list attribute.

st_cl1= StudyCell(name="st_cl1", elements=[nte1])
st_cl2= StudyCell(name="st_cl2", elements=[te1])
st_cl3= StudyCell(name="st_cl3", elements=[nte2])
st_cl4= StudyCell(name="st_cl4", elements=[te2])
st_cl6= StudyCell(name="st_cl6", elements=[nte2])
st_cl7= StudyCell(name="st_cl7", elements=[te3])
st_cl5= StudyCell(name="st_cl5", elements=[nte3])

### 7. Creation of an ISA `Study Arm` and setting the number of subjects associated to that unique sequence of ISA `Cell`s.

arm1 = StudyArm(name='Arm 1', group_size=20, )
print(arm1)

genotype_cat = OntologyAnnotation(term="genotype")
genotype_value1 = OntologyAnnotation(term="control - normal")
genotype_value2 = OntologyAnnotation(term="mutant")

arm1 = StudyArm(name='Arm 1', 
                group_size=2, 
                source_type=Characteristic(category=genotype_cat,
                                           value=genotype_value1)
                                          )
print(arm1)

### 8. Declaring an ISA `Sample Assay Plan`, defining which `Sample` are to be collected and which `Assay`s to be used

input_material1=ProductNode(id_="MAT1", name="liver", node_type=SAMPLE,size=1,characteristics=[Characteristic(category=OntologyAnnotation(term='organism part'), value=OntologyAnnotation(term='liver'))])
input_material2=ProductNode(id_="MAT2", name="blood", node_type=SAMPLE,size=1,characteristics=[Characteristic(category=OntologyAnnotation(term='organism part'), value=OntologyAnnotation(term='blood'))])
input_material3=ProductNode(id_="MAT3", name="urine", node_type=SAMPLE,size=3,characteristics=[Characteristic(category=OntologyAnnotation(term='organism part'), value=OntologyAnnotation(term='urine'))])


### 9. Loading an isa assay definition in the form of an ordered dictionary. 

- It corresponds to an ISA configuration assay table but expressed in JSON.

- In this NMR assay there is a sample extraction step, which produces "supernatant" and "pellet" extracts (1 of each per input sample).

- IMPORTANT: Note how ISA `OntologyAnnotation` elements are used in this data structure

nmr_assay_dict = OrderedDict([
    ('measurement_type', OntologyAnnotation(term='metabolite profiling')),
    ('technology_type', OntologyAnnotation(term='nmr spectroscopy')),
            ('extraction', {}),
            ('extract', [
                {
                    'node_type': EXTRACT,
                    'characteristics_category': OntologyAnnotation(term='extract type'),
                    'characteristics_value': 'supernatant',
                    'size': 1,
                    'technical_replicates': None,
                    'is_input_to_next_protocols': True
                },
                {
                    'node_type': EXTRACT,
                    'characteristics_category': OntologyAnnotation(term='extract type'),
                    'characteristics_value': 'pellet',
                    'size': 1,
                    'technical_replicates': None,
                    'is_input_to_next_protocols': True
                }
            ]),
            ('nmr_spectroscopy', {
                OntologyAnnotation(term='instrument'): ['Bruker AvanceII 1 GHz'],
                OntologyAnnotation(term='acquisition_mode'): ['1D 13C NMR','1D 1H NMR','2D 13C-13C NMR'],
                OntologyAnnotation(term='pulse_sequence'): ['CPMG','TOCSY','HOESY','watergate']
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

### 10. We now show how to create an new AssayGraph structure from scratch, as if we were defining a completely new assay type.

new_assay_graph1=AssayGraph(id_="WB", measurement_type=OntologyAnnotation(term="protein profiling"), technology_type=OntologyAnnotation(term="Western blot"))



### 11. We procede by assembling the Process graph:


protocol_node_protein = ProtocolNode(id_="P",name='Protein extraction')
protocol_node_data_acq = ProtocolNode(id_="DA",name='WB imaging', parameter_values=[ParameterValue(category=ProtocolParameter(parameter_name=OntologyAnnotation(term="channel")),value=OntologyAnnotation(term="360 nm")),ParameterValue(category=ProtocolParameter(parameter_name=OntologyAnnotation(term='channel')),value=OntologyAnnotation(term="550 nm"))])

protein_char = Characteristic(category=OntologyAnnotation(term='material type'), value='protein extract')
protein_sample_node = ProductNode(id_="SP", node_type=SAMPLE, size=1, characteristics=[protein_char])
wb_data_node = ProductNode(id_="WBD", node_type=DATA_FILE, size=1)

nodes = [protein_sample_node, wb_data_node, protocol_node_protein, protocol_node_data_acq]
links = [(protocol_node_protein,protein_sample_node),(protein_sample_node,protocol_node_data_acq),(protocol_node_data_acq,wb_data_node)]

new_assay_graph1.add_nodes(nodes)
new_assay_graph1.add_links(links)

new_assay_graph1

The following step does 3 things:

- generate an assay plan from the assay declaration data strucure
- create a `Sample and Assay Plan` object holding a list of samples and the list of assay workflows which have been declared
- create a `Sample to Assay` object, which details which sample will be input to a specific assay.

nmr_assay_graph = AssayGraph.generate_assay_plan_from_dict(nmr_assay_dict)

sap1 = SampleAndAssayPlan(name='sap1', sample_plan=[input_material1,input_material2,input_material3],assay_plan=[new_assay_graph1,nmr_assay_graph])

sample2assay_plan={input_material3: [new_assay_graph1, nmr_assay_graph], input_material2: [nmr_assay_graph], input_material1: [nmr_assay_graph]}

sap1.sample_to_assay_map=sample2assay_plan

sap1.sample_to_assay_map

# specifying which sample type (sometimes referred to as specimen)
# sap1.add_sample_type('liver')

# specifying how many times each specimen is supposed to be collected
# sap1.add_sample_plan_record('liver',3)

#### 9. Declaration of an ISA assay and linking specimen type and data acquisition plan for this assay
# # declare the type of `Assay` which will be performed
# assay_type1 = Assay(measurement_type='metabolite profiling', technology_type='mass spectrometry')
# # associate this assay type to the `SampleAssayPlan`
# sap1.add_assay_type(assay_type1)
# # specify which `sample type` will be used as input to the declare `Assay`
# sap1.add_assay_plan_record('liver',assay_type1)

### 11. Build an ISA `Study Design Arm` by adding the first set of ISA `Cells` and setting the `Sample Assay Plan`

arm1.add_item_to_arm_map(st_cl1,sap1)
print(arm1)

### 12 Now expanding the `Arm` by adding a new `Cell`, which uses the same `Sample Assay Plan` as the one used in Cell #1.
Of course, the `Sample Assay Plan` for this new `Cell` could be different. It would have to be to built as shown before.

arm1.add_item_to_arm_map(st_cl2,sap1)

# Adding the last section of the Arm, with a cell which also uses the same sample assay plan.
arm1.add_item_to_arm_map(st_cl3,sap1)
arm1.add_item_to_arm_map(st_cl4,sap1)
arm1.add_item_to_arm_map(st_cl6,sap1)
arm1.add_item_to_arm_map(st_cl7,sap1)
arm1.add_item_to_arm_map(st_cl5,sap1)

### 13. Creation of additional ISA Study Arms and setting the number of subjects associated to that unique sequence of ISA Cells.

arm2 = StudyArm(name='Arm 2')
arm2.group_size=40
arm2.add_item_to_arm_map(st_cl1,sap1)
arm2.add_item_to_arm_map(st_cl4,sap1)
arm2.add_item_to_arm_map(st_cl3,sap1)
arm2.add_item_to_arm_map(st_cl2,sap1)
arm2.add_item_to_arm_map(st_cl6,sap1)
arm2.add_item_to_arm_map(st_cl7,sap1)
arm2.add_item_to_arm_map(st_cl5,sap1)

arm3 = StudyArm(name='Arm 3')
arm3.group_size=10
arm3.add_item_to_arm_map(st_cl1,sap1)
arm3.add_item_to_arm_map(st_cl7,sap1)
arm3.add_item_to_arm_map(st_cl3,sap1)
arm3.add_item_to_arm_map(st_cl4,sap1)
arm3.add_item_to_arm_map(st_cl6,sap1)
arm3.add_item_to_arm_map(st_cl2,sap1)
arm3.add_item_to_arm_map(st_cl5,sap1)

### 14. We can now create the ISA `Study Design` object, which will receive the `Arms` defined by the user.

study_design= StudyDesign(name='trial design #1')
# print(sd)

# Adding a study arm to the study design object.
study_design.add_study_arm(arm1)
study_design.add_study_arm(arm2)
study_design.add_study_arm(arm3)
# print(sd)

# Let's now serialize the ISA study design to JSON
import json
from isatools.isajson import ISAJSONEncoder
from isatools.create.model import StudyDesignEncoder

f=json.dumps(study_design, cls=StudyDesignEncoder, sort_keys=True, indent=4, separators=(',', ': '))


### 15. let's produce a graphical overview of the study design arms and the associated sample assay plans

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
                 text='repeated measure group design layout - isa-api 0.12', render_mode='css',
                 border_line_color='gray', border_line_alpha=0.4,
                 background_fill_color='white', background_fill_alpha=1.0)

fig.add_layout(citation)

show(fig)

study = study_design.generate_isa_study()

len(study.assays)

investigation.studies=[study]

# print(investigation.studies[0].assays[1])
print(investigation.studies[0].assays[0])

# WRITING ISA-JSON document
print(json.dumps(investigation, cls=ISAJSONEncoder, sort_keys=True, indent=4, separators=(',', ': ')))

from isatools import isatab
isatab.dump(investigation, './notebook-output/isa-repeated-measure-crossover-design')

from isatools.isatab import dump_tables_to_dataframes as dumpdf
dataframes = dumpdf(investigation)
dataframes.keys()

len(dataframes.keys())

dataframes[list(dataframes.keys())[1]]

[x for x in study.assays[0].graph.nodes() if isinstance(x, Sample)]

len([x for x in study.assays[0].graph.nodes() if isinstance(x, Sample)])

[getattr(x, 'name', None) for x in study.assays[0].graph.nodes()]

## About this notebook

- authors: philippe.rocca-serra@oerc.ox.ac.uk, massimiliano.izzo@oerc.ox.ac.uk
- license: CC-BY 4.0
- support: isatools@googlegroups.com
- issue tracker: https://github.com/ISA-tools/isa-api/issues