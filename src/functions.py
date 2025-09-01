import os
import subprocess
import json
import logging
import gi
from ulauncher.utils.Path import Path

gi.require_version('Gtk', '3.0')
from gi.repository import Gio, Gtk # type: ignore
logger = logging.getLogger(__name__)

icon_theme = Gtk.IconTheme.get_default()
def lookup_icon(icon_name, size):
    filename = ""
    icon_file = icon_theme.lookup_icon(icon_name , size , 0)
    if icon_file != None:
        filename = icon_file.get_filename()
    else: 
        logger.debug(f'Icon "{icon_name}" not found')
    return filename

def get_file_icon(path: Path, size):
    if path.exists():
        file = Gio.File.new_for_path(path.get_abs_path())
        info = file.query_info('standard::icon' , 0 , Gio.Cancellable())
        icon = info.get_icon().get_names()[0]
        return lookup_icon(icon, size) 


class ExtensionException(Exception):
    def __init__(self, name, desc=""):
        self.name = name
        self.desc = desc
        super().__init__(name, desc)

class KidexErrorException(ExtensionException):
    pass

class KidexWarningException(ExtensionException):
    pass

class IndexEntry:
    def __init__(self, path: str, _type):
        self.path = Path(path)
        self.parent_dir = os.path.dirname(self.path.get_abs_path())
        self.basename = self.path.get_basename()
        self.type = _type

    def is_dir(self) -> bool:
        return self.path.is_dir()

    def get_icon(self) -> str | None:
        if self.is_dir():
            return lookup_icon("folder", 64)
        else:
            return get_file_icon(self.path, 64)


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

