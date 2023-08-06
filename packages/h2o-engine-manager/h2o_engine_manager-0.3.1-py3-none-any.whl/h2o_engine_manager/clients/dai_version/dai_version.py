import pprint
from typing import Dict, List


class DAIVersion:
    """Class represents Driverless AI version."""

    def __init__(
        self,
        version: str,
        aliases: List[str],
        annotations: Dict[str, str],
    ) -> None:
        self.version = version
        self.aliases = aliases
        self.annotations = annotations

    def __repr__(self) -> str:
        return pprint.pformat(self.__dict__)
