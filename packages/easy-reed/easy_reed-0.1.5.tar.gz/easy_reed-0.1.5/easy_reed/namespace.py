# Standard Library Imports
from typing import Self, Any, Dict
from configparser import ConfigParser

class NameSpace():

    def __init__(self, name: str, filename: str, *, typemap: Dict[str, type] = None) -> Any:
        self._config = ConfigParser()
        self._name = name