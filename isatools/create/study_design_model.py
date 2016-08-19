__author__ = 'prs'

import uuid
import json
import xml


factors = {"factor_name":[]}

treatments={"uuid":[],"id":[],"fvcombo":{},"order":int}

study_design = {"balance": ["balanced design","unbalanced design"],
                "factorial":["full factorial design","fractional factorial design"],
                "treatment_applied": ["single treatment","repeated treatment"],
                "geometry": ["parallel design","crossover design"]}

study_groups = {"uuid":[],"id":[],"size":int,"treatment": treatments }

study = {"uuid": "", "study design":study_design, "study groups":study_groups, "treatments":treatments, "factors":factors, "study mode":["in-vitro","in-vivo"]}




#creating ISA records:

for group in study_groups:  #how many study groups
    for i in range(group["size"]): #how many subjects in each of the study group
        source_id = uuid.uuid4()
        source_name = group + "_subject-" + i
        source_Names[source_id]=source_name
        for j in range(sampletype):
            for k in nb_collection_events:
                sample_uuid = uuid.uuid4()
                sample_name = source_name + "_specimen-" + j + "_event-" + k
                sample_Names[sample_uuid] = sample_name