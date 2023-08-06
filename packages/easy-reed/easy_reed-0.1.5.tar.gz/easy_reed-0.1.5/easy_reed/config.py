# Standard Library Imports
from typing import Self, Any, Dict


class Config():
    """
    
    
    """

    def __init__(self) -> Self:
        self._config = []

    def __get__(self, arg: str, ) -> Any:
        """ fetches
        
        """
        if arg not in self._config:
            raise KeyError("f{arg} is missing from the config")
        return self._config[arg]

    def __set__(self, key: str, value: Any) -> NameError:
        raise NameError("The easy_reed config object does not allow developers to add config fields directly in code.  This must be done from a configuration file.")

    def register(self, filename: str, *, typemap: Dict[str, Any] = None):
        pass