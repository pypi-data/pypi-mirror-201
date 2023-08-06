from dataclasses import dataclass
from enum import Enum
from typing import Union, List



class PolicyProvider(Enum):
    AZURE_POLICY = 1
    AWS_CONFIG_POLICY = 2
    KUBE_BENCH = 3
    OTHER = 4


class SourceProvider(Enum):
    AWS = 1
    AZURE = 2
    KUBERNETES = 3
    GCP = 4
    NIST = 5
    CSA = 6
    CIS = 7
    OTHER = 8


@dataclass
class Policy:
    """Class to represent a Policy and reference metadata"""
    name: str
    description: str
    provider: Union[PolicyProvider, SourceProvider]
    url: str


@dataclass()
class Validation:
    """Class to represent Validation metadata."""
    name: str
    description: str
    implements: List[Policy]
    references: List[Policy]
    coverage: str

