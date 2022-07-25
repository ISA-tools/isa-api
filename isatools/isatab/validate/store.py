class Validator:

    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []

    def reset_store(self):
        self.errors = []
        self.warnings = []
        self.info = []

    def add_error(self, code: int, message: str = '', supplemental: str = '') -> None:
        self.errors.append({"message": message, "supplemental": supplemental, "code": code})

    def add_warning(self, code: int, message: str = '', supplemental: str = '') -> None:
        self.warnings.append({"message": message, "supplemental": supplemental, "code": code})

    def add_info(self, code: int, message: str = '', supplemental: str = '') -> None:
        self.info.append({"message": message, "supplemental": supplemental, "code": code})

    def __dict__(self):
        return {'errors': self.errors, 'warnings': self.warnings, 'info': self.info}

    def __str__(self):
        return str(self.__dict__())


validator = Validator()
