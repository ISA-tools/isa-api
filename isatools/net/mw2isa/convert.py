import logging
from json import loads as json_loads
import requests

from bs4 import BeautifulSoup

from isatools.net.mw2isa.utils import is_mw_id
from isatools.net.mw2isa.const import STUDY_ANALYSIS_BASE_URL, STUDY_BASE_URL


log = logging.getLogger('isatools')


class MW2ISA:

    def __init__(self, mw_id: str) -> None:
        self.mw_id = mw_id
        self.study_analysis_url = '%s/%s/analysis' % (STUDY_ANALYSIS_BASE_URL, mw_id)
        self.analysis_type = None

    @property
    def mw_id(self) -> str:
        return self.__mw_id

    @mw_id.setter
    def mw_id(self, mw_id: str) -> None:
        if not is_mw_id(mw_id):
            raise ValueError("Invalid MetaboLights ID: %s" % mw_id)
        self.__mw_id = mw_id

    def get_analysis_type(self) -> str:
        if self.analysis_type:
            return self.analysis_type
        try:
            response = requests.get(self.study_analysis_url)
            analyses = json_loads(response.text)
        except Exception as e:
            raise Exception('There was a problem when trying to download the analysis for %s: %s' % (self.mw_id, e))

        if "1" in analyses.keys():
            log.warning('Several analysis types found, using the last one')
            analyse_type = analyses[list(analyses.keys())[-1]]['analysis_type']
        else:
            analyse_type = analyses['analysis_type']
        log.info('Using technology type %s' % analyse_type)
        self.analysis_type = analyse_type
        return analyse_type

    def get_html_table(self) -> list:
        analysis_type = self.get_analysis_type()
        page_url = '%s%sData&StudyID=%s&StudyType=%s&ResultType=1#DataTabs' % (
            STUDY_BASE_URL, analysis_type, self.mw_id, analysis_type
        )
        response = requests.get(page_url)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.findAll("table", {'class': "datatable2"})



