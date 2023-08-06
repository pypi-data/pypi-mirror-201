from dataclasses import dataclass
from typing import List
from core.bp_metadata_utils.policy import Policy, Validation


@dataclass
class BlueprintMetaData:
    """
    Class to represent blueprint metadata
    """
    name: str
    desc: str
    author: str
    validations: List[Validation]
