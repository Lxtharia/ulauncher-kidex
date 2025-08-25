import os
import subprocess
import json


def parse_index_entry():
    pass

class ExtensionException(Exception):
    def __init__(self, name, desc = ""):
        self.name = name
        self.desc = desc
        super().__init__(name, desc)

class KidexErrorException(ExtensionException):
    pass


class KidexWarningException(ExtensionException):
    pass


class IndexEntry:
    def __init__(self, path: str, type):
        self.basename = os.path.basename(path)
        self.path = path
        self.type = type
        pass


def get_find_results(query_string: str,
                     command: str = "kidex-client",
                     limit: int = 100) -> list[IndexEntry]:
    results = []
    try:
        process_result = subprocess.check_output([command, "find", query_string])
        result: list[dict[str,str]] = json.loads(process_result)
        i = 0
        for entry in reversed(result):
            results.append(IndexEntry(
                entry['path'],
                "dir" if entry['directory'] else "file"
            ))
            i += 1
            if i >= limit:
                break
    except subprocess.CalledProcessError:
        raise KidexErrorException("Kidex is not running", "Go start it!")
    except Exception as e:
        raise KidexErrorException("Unknown Error occured", e)
    return results
