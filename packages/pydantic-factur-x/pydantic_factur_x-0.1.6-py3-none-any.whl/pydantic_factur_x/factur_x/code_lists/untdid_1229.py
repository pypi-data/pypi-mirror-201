"""UntDid1229 Status Code

https://service.unece.org/trade/untdid/d16b/tred/tred1229.htm
"""
from enum import Enum


class UntDid1229(str, Enum):
    """Enum for all possible values for UNTDID 1229.

    Line Item Status Code
    """

    ADDED = "1"
    CHANGED = "3"
    ACCEPTED_WITHOUT_AMENDMENT = "5"
    ACCEPTED_WITH_AMENDMENT = "6"
    NOT_ACCEPTED = "7"
    ALREADY_DELIVERED = "42"
    # ... to be completed
