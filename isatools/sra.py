import lxml
import logging
from isatools.model.v1 import *

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def dump(isa_obj, output_path):

    def _get_comment(comments, name):
        matches = [i for i in comments if i.name == name]
        if len(matches) == 1:
            return matches[0].value
        else:
            if len(matches) == 0:
                return None
            else:
                raise AttributeError("Could not find comment with name '{}'".format(name))

    def _get_study_type(assays):
        measurement_types = [a.measurement_type.name for a in assays]
        logger.info(measurement_types)
        if 'transcription profiling' in measurement_types:
            return 'Transcriptome Analysis'
        elif 'environmental gene survey' in measurement_types:
            return 'Metagenomics'
        elif 'DNA-protein binding site identification' in measurement_types \
                or 'transcription factor binding site identification' in measurement_types:
            return 'Gene Regulation Study'
        elif 'DNA methylation profiling' in measurement_types:
            return 'Epigenetics'
        elif 'genome sequencing' in measurement_types:
            return 'Whole Genome Sequencing'
        elif 'chromosome rearrangement' in measurement_types:
            return 'Population Genomics'
        else:
            return 'Other'

    def _write_study_xml(s):
        s_comments = s.comments

        # build STUDY DESCRIPTOR
        sra_center_name = _get_comment(s_comments, 'SRA Center Name')
        sra_center_project_name = _get_comment(s_comments, 'SRA Center Project Name')
        study_title = s.title
        study_abstract = s.description
        study_description = s.description
        study_type = _get_study_type(s.assays)
        study_xml = """
            <DESCRIPTOR>
                <CENTER_NAME>{sra_center_name}</CENTER_NAME>
                <CENTER_PROJECT_NAME>{sra_center_project_name}</CENTER_PROJECT_NAME>
                <STUDY_TITLE>{study_title}</STUDY_TITLE>
                <STUDY_ABSTRACT>{study_description}</STUDY_ABSTRACT>
                <STUDY_DESCRIPTION>{study_description}</STUDY_DESCRIPTION>
            <STUDY_TYPE existing_study_type="{study_type}"/>
        """.format(sra_center_name=sra_center_name,
                   sra_center_project_name=sra_center_project_name,
                   study_title=study_title,
                   study_abstract=study_abstract,
                   study_description=study_description,
                   study_type=study_type)
        logger.info(study_xml)

        # build STUDY LINKS


    def _write_experiment_set_xml():
        pass

    def _write_run_set_xml():
        pass

    def _write_sample_set_xml():
        pass


    def _write_submission_xml():
        pass

    for study in isa_obj.studies:
        _write_study_xml(study)
