
def parse_index_entry():
    pass

class KidexErrorException(Exception):
    pass

class KidexWarningException(Exception):
    pass

class IndexEntry:
    def __init__(self, basename: str, path: str, type):
        self.basename = basename
        self.path = path
        self.type = type
        pass

def get_find_results(query_string: str) -> list[IndexEntry]:
    raise KidexException("Kidex not running or something")
    return []
