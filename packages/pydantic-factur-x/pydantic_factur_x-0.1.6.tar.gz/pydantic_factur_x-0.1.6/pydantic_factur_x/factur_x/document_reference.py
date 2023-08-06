"""Factur-X exchanged document.

Common address elements for all Factur-X documents.
"""
from typing import Optional
from pydantic_xml import BaseXmlModel, element

from ._nsmaps import RAM

from .common import DateTime


class DocumentReference(
    BaseXmlModel,
    tag="DocumentReference",
    ns_attrs=True,
    ns="ram",
    nsmap=RAM,
):
    """ram:DocumentReference"""

    document_id: str = element(
        tag="IssuerAssignedID",
        ns="ram",
        # nsmap=RAM,
    )
    reference_date: Optional[DateTime] = element(
        tag="FormattedIssueDateTime",
        ns="ram",
        # nsmap=RAM,
    )
