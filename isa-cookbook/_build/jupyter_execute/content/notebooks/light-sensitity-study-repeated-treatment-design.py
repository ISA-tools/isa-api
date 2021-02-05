# Light Sensitivity Experiment: 

## Reporting a repeated treatment design with `ISA create mode`

This example creates `ISA study descriptor` for study with sequential treatments organized in an arm. This shows how to use objects from the `isatools.create` component in a granular fashion. It creates each `Element` of the Study `Arm` at a time.
Finally, the `study design plan` is shown by serializing the `ISA Study Design Model` content as an  `ISA_design` JSON document, which can be rendered in various ways (tables, figures).

## Study metadata

import datetime
import isatools
from isatools.model import *
from isatools.isatab import dumps
import json
from isatools.isajson import ISAJSONEncoder

from isatools.create.model import * 

investigation = Investigation()
investigation1 = Investigation() # to be used with the study create function
study = Study(filename="s_study_xover.txt")
study.identifier = "elifesprint2019-1"
study.title = "elifesprint2019-1: light sensitivity"
study.description = "a study about light sensitivity difference between a control population (n=10) and a genotype A population (n=10)."
study.submission_date = str(datetime.datetime.today())
study.public_release_date = str(datetime.datetime.today())
study.sources = [Source(name="source1")]
study.samples = [Sample(name="sample1")]
study.protocols = [Protocol(name="sample collection")]
study.process_sequence = [Process(executes_protocol=study.protocols[-1], inputs=[study.sources[-1]], outputs=[study.samples[-1]])]
investigation.studies = [study]


# Let's see the object :
investigation

# print(dumps(investigation))

# print(json.dumps(investigation, cls=ISAJSONEncoder, sort_keys=True, indent=4, separators=(',', ': ')))

### 1. Creation of the first `ISA Study Design Element` and setting *both* `element_type` AND `duration_unit` attributes

# IMPORTANT: note how duration_unit value is supplied as an OntologyAnnotation object
nte1 = NonTreatment(element_type='screen', duration_unit=OntologyAnnotation(term="days"))
print(nte1)

### 2. Creation of another `ISA Study Design Element`, of type `Treatment`

te1 = Treatment()
te1.type='radiological intervention'
print(te1)

### 2.1 defining the first treatment as a vector of ISA factor values:

Under "ISA Study Design Create mode", a `Study Design Element` of type `Treatment` needs to be defined by a vector of `Factors` and their respective associated `Factor Values`. This is done as follows:


f1 = StudyFactor(name='light', factor_type=OntologyAnnotation(term="electromagnetic energy"))
f1v = FactorValue(factor_name=f1, value="visible light at 3000K produced by LED array")
f2 = StudyFactor(name='dose', factor_type=OntologyAnnotation(term="quantity"))

# IMPORTANT: note how *FactorValue value* is supplied as an *numeral*
f2v = FactorValue(factor_name=f2, value=250, unit=OntologyAnnotation(term='lux'))
f3 = StudyFactor(name='duration', factor_type=OntologyAnnotation(term="time"))
f3v = FactorValue(factor_name=f3, value=1, unit=OntologyAnnotation(term='hr'))

print(f1v,f2v)


#assigning the factor values declared above to the ISA treatment element
te1.factor_values = [f1v,f2v,f3v]
print(te1)


### 3. Creation of a second  `ISA Study Design Element`, of type `Treatment`, following the same pattern.

te3 = Treatment()
te3.type = 'radiological intervention'
rays = StudyFactor(name='light', factor_type=OntologyAnnotation(term="electromagnetic energy"))

raysv = FactorValue(factor_name=rays, value='visible light at 3000K produced by LED array')
rays_intensity = StudyFactor(name='dose', factor_type=OntologyAnnotation(term="quantity"))
rays_intensityv= FactorValue(factor_name=rays_intensity, value = 250, unit=OntologyAnnotation(term='lux'))
rays_duration =  StudyFactor(name = 'duration', factor_type=OntologyAnnotation(term="time"))
rays_durationv = FactorValue(factor_name=rays_duration, value=1, unit=OntologyAnnotation(term='hour'))

te3.factor_values = [raysv,rays_intensityv,rays_durationv]
print(te3)
                

### 4. Creation of 'wash out' period as an `ISA Study Design Element`.

# Creation of another ISA element, which is not a Treatment element, which is of type `screen` by default
# nte2 = NonTreatment()
# nte2.type = 'washout'
# net2.duration_unit=OntologyAnnotation(term="days")

nte2 = NonTreatment(element_type='washout', duration_unit=OntologyAnnotation(term="days"))
print(nte2)

# setting the factor values associated with 'default' DURATION Factor associated with such elements
nte2.duration.value=2
nte2.duration.unit=OntologyAnnotation(term="weeks")

### 5. Creation of 'follow-up' period as an `ISA Study Design Element`.

nte3 = NonTreatment(element_type=FOLLOW_UP, duration_value=1, duration_unit=OntologyAnnotation(term="month"))
#print(nte3)

### 6. Creation of the associated container, known as an ISA `Cell` for each ISA `Element`.
In this example, a single `Element` is hosted by a `Cell`, which must be named. In more complex designs (e.g. study designs with assymetric arms), a `Cell` may contain more than one `Element`, hence the list attribute.

st_cl1= StudyCell(name="st_cl1", elements=[nte1])
st_cl2= StudyCell(name="st_cl2", elements=[te1])
st_cl3= StudyCell(name="st_cl3", elements=[nte2])
st_cl4= StudyCell(name="st_cl4", elements=[te3])
st_cl5= StudyCell(name="st_cl5", elements=[nte3])

### 7. Creation of an ISA `Study Arm` and setting the number of subjects associated to that unique sequence of ISA `Cell`s.

genotype_cat = OntologyAnnotation(term="genotype")
genotype_value1 = OntologyAnnotation(term="control - normal")
genotype_value2 = OntologyAnnotation(term="mutant")

arm1 = StudyArm(name='Arm 1', 
                group_size=2)

arm1.source_type=Characteristic(category=genotype_cat,
                                           value=genotype_value1)

print(arm1)

### 8. Declaring an ISA `Sample Assay Plan`, defining which `Sample` are to be collected and which `Assay`s to be used

whole_patient=ProductNode(id_="MAT1",
                          name="subject",
                          node_type=SAMPLE, size=1,
                          characteristics=[Characteristic(
                                category=OntologyAnnotation(term='organism part'), 
                                value=OntologyAnnotation(term='whole organism'))])

saliva=ProductNode(id_="MAT2", name="saliva", node_type=SAMPLE, size=1, characteristics=[
    Characteristic(category=OntologyAnnotation(term='organism part'),
                   value=OntologyAnnotation(term='saliva'))])



Here we load an isa assay definition in the form of an ordered dictionary. It corresponds to an ISA configuration assay table but expressed in JSON.

We now show how to create an new AssayGraph structure from scratch, as if we were defining a completely new assay type.

light_sensitivity_phenotyping_1 = OrderedDict([
    ('measurement_type', OntologyAnnotation(term='melatonine concentration')),
    ('technology_type', OntologyAnnotation(term='radioimmunoprecipitation assay')),
     ('extraction', {}),
            ('extract', [
                {
                    'node_type': EXTRACT,
                    'characteristics_category': OntologyAnnotation(term='extract type'),
                    'characteristics_value': OntologyAnnotation(term='extract'),
                    'size': 1,
                    'technical_replicates': None,
                    'is_input_to_next_protocols': True
                }]),
                
    ('radioimmunoprecipitation', {
                OntologyAnnotation(term='instrument'): [OntologyAnnotation(term='Beckon Dickison XYZ')],
                OntologyAnnotation(term='antibody'): [OntologyAnnotation(term='AbCam antiMelatonine ')],
                OntologyAnnotation(term='time point'): [OntologyAnnotation(term='1 hr'),
                                                        OntologyAnnotation(term='2 hr')]
            }),
            ('raw_data_file', [
                {
                    'node_type': DATA_FILE,
                    'size': 1,
                    'technical_replicates': 1,
                    'is_input_to_next_protocols': False
                }
            ])
])


light_sensitivity_phenotyping_2 = OrderedDict([
        ('measurement_type', OntologyAnnotation(term='light sensitivity')),
        ('technology_type', OntologyAnnotation(term='electroencephalography')),
            ('data_collection', {
                OntologyAnnotation(term='instrument'): [OntologyAnnotation(term='Somnotouch')],
                OntologyAnnotation(term='sampling_rate'): [OntologyAnnotation(term='200 Hz')],
                OntologyAnnotation(term='time point'): [OntologyAnnotation(term='1 hr'),
                                                        OntologyAnnotation(term='2 hr')]
            }),
            ('raw_data_file', [
                {
                    'node_type': DATA_FILE,
                    'size': 1,
                    'technical_replicates': 1,
                    'is_input_to_next_protocols': False
                }
            ])
])

light_sensitivity_phenotyping_3 = OrderedDict([
        ('measurement_type', OntologyAnnotation(term='light sensitivity phenotyping')),
        ('technology_type', OntologyAnnotation(term='direct measurement')),
            ('data_collection', {
                OntologyAnnotation(term='variables'): [OntologyAnnotation(term='sleepiness'),
                                                       OntologyAnnotation(term='heart rate'),
                                                       OntologyAnnotation(term='pupilla size')],
                OntologyAnnotation(term='time point'): [OntologyAnnotation(term='1 hr'),
                                                        OntologyAnnotation(term='2 hr')]
            }),
            ('raw_data_file', [
                {
                    'node_type': DATA_FILE,
                    'size': 1,
                    'technical_replicates': 1,
                    'is_input_to_next_protocols': False
                }
            ])
])


alterness_assay_graph = AssayGraph.generate_assay_plan_from_dict(light_sensitivity_phenotyping_1)
melatonine_assay_graph = AssayGraph.generate_assay_plan_from_dict(light_sensitivity_phenotyping_2)
general_phenotyping_assay_graph = AssayGraph.generate_assay_plan_from_dict(light_sensitivity_phenotyping_3)


sap1 = SampleAndAssayPlan(name='sap1', sample_plan=[whole_patient,saliva],assay_plan=[alterness_assay_graph,melatonine_assay_graph,general_phenotyping_assay_graph])

sap1.add_element_to_map(sample_node=saliva, assay_graph=melatonine_assay_graph)
sap1.add_element_to_map(sample_node=whole_patient, assay_graph=alterness_assay_graph)
sap1.add_element_to_map(sample_node=whole_patient,assay_graph=general_phenotyping_assay_graph)


sap1.sample_to_assay_map

### 9. Declaration of an ISA assay and linking specimen type and data acquisition plan for this assay

### 10. Build an ISA `Study Design Arm` by adding the first set of ISA `Cells` and setting the `Sample Assay Plan`

arm1.add_item_to_arm_map(st_cl1, sap1)
# print(arm1)

### 11 Now expanding the `Arm` by adding a new `Cell`, which uses the same `Sample Assay Plan` as the one used in Cell #1.
Of course, the `Sample Assay Plan` for this new `Cell` could be different. It would have to be to built as shown before.

arm1.add_item_to_arm_map(st_cl2, sap1)

# Adding the last section of the Arm, with a cell which also uses the same sample assay plan.
arm1.add_item_to_arm_map(st_cl3, sap1)
arm1.add_item_to_arm_map(st_cl4, sap1)
arm1.add_item_to_arm_map(st_cl5, sap1)

### 12. Creation of additional ISA Study Arms and setting the number of subjects associated to that unique sequence of ISA Cells.

arm2 = StudyArm(name='Arm 2')
arm2.group_size=2
arm2.source_type=Characteristic(category=genotype_cat,
                                value=genotype_value2)

# st_cl6= StudyCell(name="st_cl6", elements=[nte1])
# st_cl7= StudyCell(name="st_cl7", elements=[te1])
# st_cl8= StudyCell(name="st_cl8", elements=[nte2])
# st_cl9= StudyCell(name="st_cl9", elements=[te3])
# st_cl10= StudyCell(name="st_cl10", elements=[nte3])



arm2.source_type.category
arm2.add_item_to_arm_map(st_cl1,sap1)
arm2.add_item_to_arm_map(st_cl4,sap1)
arm2.add_item_to_arm_map(st_cl3,sap1)
arm2.add_item_to_arm_map(st_cl2,sap1)
arm2.add_item_to_arm_map(st_cl5,sap1)

arm3 = StudyArm(name='Arm 3')
arm3.group_size=2
arm3.source_type=Characteristic(category=genotype_cat,
                                value=genotype_value1
                               )
arm3.add_item_to_arm_map(st_cl1,sap1)
arm3.add_item_to_arm_map(st_cl2,sap1)
arm3.add_item_to_arm_map(st_cl3,sap1)
arm3.add_item_to_arm_map(st_cl4,sap1)
arm3.add_item_to_arm_map(st_cl5,sap1)

arm4 = StudyArm(name='Arm 4')
arm4.group_size=2
arm4.source_type=Characteristic(category=genotype_cat,
                                value=genotype_value2)

arm4.add_item_to_arm_map(st_cl1,sap1)
arm4.add_item_to_arm_map(st_cl4,None)
arm4.add_item_to_arm_map(st_cl3,sap1)
arm4.add_item_to_arm_map(st_cl2,None)
arm4.add_item_to_arm_map(st_cl5,sap1)

### 14. We can now create the ISA `Study Design` object, which will receive the `Arms` defined by the user.

study_design_final= StudyDesign(name='trial design #1')
# print(sd)

# Adding a study arm to the study design object.
study_design_final.add_study_arm(arm1)
study_design_final.add_study_arm(arm2)
study_design_final.add_study_arm(arm3)
study_design_final.add_study_arm(arm4)

study_finale = study_design_final.generate_isa_study()
investigation1.studies.append(study_finale)
# print(investigation1.studies[0].name)

# Let's now serialize the ISA study design to JSON
import json
from isatools.isajson import ISAJSONEncoder
from isatools.create.model import StudyDesignEncoder

f=json.dumps(study_design_final, cls=StudyDesignEncoder, sort_keys=True, indent=4, separators=(',', ': '))

final_dir = os.path.abspath(os.path.join('notebook-output', 'isa-study-custom-assay-light-sensitivity'))

with open(os.path.join(final_dir,'./light-sensitivity-study_design_final.json'), 'w') as isa_sdf_jf:
    json.dump(json.loads(f), isa_sdf_jf)

# print(json.dumps(investigation, cls=ISAJSONEncoder, sort_keys=True, indent=4, separators=(',', ': ')))
from isatools import isatab
isatab.dump(investigation1, final_dir)

from isatools.isatab import dump_tables_to_dataframes as dumpdf
dataframes = dumpdf(investigation)

## About this notebook

- authors: philippe.rocca-serra@oerc.ox.ac.uk, massimiliano.izzo@oerc.ox.ac.uk
- license: CC-BY 4.0
- support: isatools@googlegroups.com
- issue tracker: https://github.com/ISA-tools/isa-api/issues