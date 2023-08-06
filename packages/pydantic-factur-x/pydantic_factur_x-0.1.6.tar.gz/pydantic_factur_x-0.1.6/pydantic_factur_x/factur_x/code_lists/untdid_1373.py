"""UntDid1373 Status Code
"""
from enum import Enum


class UntDid1373(str, Enum):
    """Enum for all possible values for UNTDID 1373."""

    ACCEPTED = "1"
    CONDITIONALLY_ACCEPTED = "3"
    REJECTED = "8"
    FINAL = "38"
    ON_HOLD = "39"
    VALIDITY_SUSPENDED = "40"
    VALIDITY_REVOKED = "41"
