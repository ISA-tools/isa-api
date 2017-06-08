import itertools

__author__ = 'massi'


class StudyDesigner(object):
    pass


class InterventionStudyDesign(StudyDesigner):

    def __init__(self, treatments_count):
        super().__init__()
        self._treatments_count = 0


    @property
    def treatments_count(self):
        return self._treatments_count

    @treatments_count.setter
    def treatments_count(self, treatments_count):
        self._treatments_count = treatments_count


class Treatment(object):

    def __init__(self):
        self._agent_values = []
        self._intensity_values = []
        self._duration_values = []

        self._factorial_design = set()

    @property
    def agent_values(self):
        return self._agent_values

    @property
    def intensity_values(self):
        return self._intensity_values

    @property
    def duration_values(self):
        return self._duration_values

    @agent_values.setter
    def agent_values(self, value):
        if isinstance(value, list):
            self._agent_values = value
        else:
            self._agent_values = [value]

    @intensity_values.setter
    def intensity_values(self, value):
        if isinstance(value, list):
            self._intensity_values = value
        else:
            self._agent_values = [value]

    @duration_values.setter
    def duration_values(self, value):
        if isinstance(value, list):
            self._duration_values = value
        else:
            self._duration_values = [value]

    def compute_full_factorial_design(self):
        if self._agent_values and self._intensity_values and self.duration_values:
            return itertools.product(self.agent_values, self.intensity_values, self.duration_values)
        else:
            return []

