import os
import subprocess
import json

def parse_index_entry():
    pass

class KidexErrorException(Exception):
    pass

class KidexWarningException(Exception):
    pass

class IndexEntry:
    def __init__(self, path: str, type):
        self.basename = os.path.basename(path)
        self.path = path
        self.type = type
        pass

def get_find_results(query_string: str, limit: int = 100) -> list[IndexEntry]:
    results = []
    try:
        process_result = subprocess.check_output(["kidex-client", "find", query_string])
        result: list[dict[str,str]] = json.loads(process_result)
        i = 0
        for entry in reversed(result):
            i += 1
            if i >= limit:
                break
            results.append(IndexEntry(
                entry['path'],
                "dir" if entry['directory'] else "file"
            ))
    except subprocess.CalledProcessError:
        raise KidexErrorException("Kidex not running or something")

    return results
