"""Factur-X exchanged document.

Common contact elements for all Factur-X documents.
"""
from typing import Optional
from pydantic_xml import BaseXmlModel, element

from ._nsmaps import RAM


class Telephone(
    BaseXmlModel,
    tag="Telephone",
    ns_attrs=True,
    ns="ram",
    nsmap=RAM,
):
    """ram:Telephone"""

    complete_number: str = element(
        tag="CompleteNumber",
        ns="ram",
        # nsmap=RAM,
        description="""The complete telephone number.""",
    )


class Email(
    BaseXmlModel,
    tag="Email",
    ns_attrs=True,
    ns="ram",
    nsmap=RAM,
):
    """ram:Email"""

    email: str = element(
        tag="URIID",
        ns="ram",
        # nsmap=RAM,
        description="""An e-mail address for the contact point.""",
    )


class Contact(
    BaseXmlModel,
    tag="Contact",
    ns_attrs=True,
    ns="ram",
    nsmap=RAM,
):
    """ram:Contact"""

    person_name: Optional[str] = element(
        tag="PersonName",
        ns="ram",
        # nsmap=RAM,
        description="""A contact point for a legal entity or person.""",
        usage="""Such as person name, contact identification, department or
        office identification : Person Name""",
    )
    department_name: Optional[str] = element(
        tag="DepartmentName",
        ns="ram",
        # nsmap=RAM,
        description="""A contact point for a legal entity or person.""",
        usage="""Such as person name, contact identification, department or office
        identification : Department Name""",
    )
    type_code: Optional[str] = element(
        tag="TypeCode",
        ns="ram",
        # nsmap=RAM,
        description="""The code specifying the type of trade contact.""",
        usage="""To be chosen from the entries in UNTDID 3139.""",
    )
    telephone_universal_communication: Optional[Telephone] = element(
        tag="TelephoneUniversalCommunication",
        ns="ram",
        # nsmap=RAM,
    )
    fax_universal_communication: Optional[Telephone] = element(
        tag="FaxUniversalCommunication",
        ns="ram",
        # nsmap=RAM,
    )
    email_uri_universal_communication: Optional[Email] = element(
        tag="EmailURIUniversalCommunication",
        ns="ram",
        # nsmap=RAM,
    )
