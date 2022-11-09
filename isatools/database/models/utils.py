def make_get_table_method(target: type) -> callable:
    @staticmethod
    def get_table():
        return target
    return get_table
