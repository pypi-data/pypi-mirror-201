"""UntDid2379 Status Code
"""
from enum import Enum


class UntDid2379(str, Enum):
    """Enum for all possible values for UNTDID 2379.

    Specify date or datetime types
    """

    DATE = "102"  # CCYYMMDD
    DATE_TIME = "203"  # CCYYMMDDHHMM
