"""Factur-X exchanged document.

Common elements for all Factur-X documents.
"""
from typing import Optional
from pydantic_xml import BaseXmlModel, attr, element

from ._nsmaps import UDT, RAM

from .code_lists import UntDid2379, UntDid4451


class String(
    BaseXmlModel,
    tag="String",
    ns_attrs=True,
    ns="ram",
    nsmap=RAM,
):
    """ram:String"""

    value: str


class BoolIndicator(
    BaseXmlModel,
    tag="BoolIndicator",
    ns_attrs=True,
    ns="ram",
    nsmap=RAM,
):
    """ram:BoolIndicator"""

    indicator: bool = element(
        tag="Indicator",
        ns="udt",
        nsmap=UDT,
        example="false",
    )


class DateTimeString(
    BaseXmlModel,
    tag="DateTimeString",
    ns="udt",
    nsmap=UDT,
):
    """udt:DateTimeString

    Profiles:
        - Factur-X: minimum
        - Order-X: basic
    """

    text: str
    format: UntDid2379 = attr(
        name="format",
        example="102",
        description="Code to specify if it is a date or date time UNTDID 2379",
        usage="only 102 for invoices, 102 or 203 for orders",
    )


class DateString(
    BaseXmlModel,
    tag="DateString",
    ns="udt",
    nsmap=UDT,
):
    """udt:DateString

    Profiles:
        - Factur-X: minimum
        - Order-X: basic
    """

    text: str
    format: UntDid2379 = attr(
        name="format",
        example="102",
        description="Code to specify if it is a date or date time UNTDID 2379",
        usage="Value = 102",
    )


class DateTime(
    BaseXmlModel,
    ns_attrs=True,
    ns="ram",
    nsmap=RAM,
):
    """ram:DateTime"""

    date_time_string: DateTimeString = element(
        tag="DateTimeString",
        ns="udt",
        # nsmap=UDT,
        example="20220131",
        description="""date.""",
    )


class IncludedNote(
    BaseXmlModel,
    tag="IncludedNote",
    ns_attrs=True,
    ns="ram",
    nsmap=RAM,
):
    """ram:IncludedNote

    Profiles:
        - Factur-X: basic_wl
        - Order-X: basic
    """

    content_code: Optional[UntDid4451] = element(
        tag="ContentCode",
        ns="ram",
        # nsmap=RAM,
        example="1",
        profiles={"factur-x": "extended", "order-x": "extended"},
        description="a code to classify the content of the document",
        usage="""To be chosen from the entries in UNTDID 4451 [6], 
        and must be the same as BT-21""",
    )
    content: str = element(
        tag="Content",
        ns="ram",
        # nsmap=RAM,
        example="This is a note",
        profiles={"factur-x": "basic_wl", "order-x": "basic"},
        description="""A textual note that gives unstructured information that is relevant 
        to the Document as a whole.""",
        usage="""Such as the reason for any correction or assignment note in case 
        the invoice has been factored""",
    )
    subject_code: Optional[UntDid4451] = element(
        tag="SubjectCode",
        ns="ram",
        # nsmap=RAM,
        example="This is a note",
        profiles={"factur-x": "basic_wl", "order-x": "basic"},
        description="""The subject of the textual note in BT-22.""",
        usage="""To be chosen from the entries in UNTDID 4451 [6].""",
    )


class GlobalID(
    BaseXmlModel,
    tag="GlobalID",
    ns="udt",
    nsmap=UDT,
):
    """udt:GlobalID

    Profiles:
        - Factur-X: basic
        - Order-X: basic
    """

    id: str
    scheme_id: str = attr(
        name="schemeID",
        example="0160",
        description="Code to specify if it is a date or date time UNTDID 2379",
        usage="only 102 for invoices, 102 or 203 for orders",
    )


class ValueMeasure(
    BaseXmlModel,
    tag="ValueMeasure",
    ns="ram",
    nsmap=RAM,
):
    """ram:ValueMeasure"""

    value: float
    unit_code: str = attr(
        name="unitCode",
        example="meter",
        usage="To be chosen from the entries in UNTDID xxx",
    )


class Quantity(
    BaseXmlModel,
    tag="Quantity",
    ns="ram",
    nsmap=RAM,
):
    """ram:Quantity

    Generic class for quantities measurements
    """

    value: float
    unit_code: str = attr(
        name="unitCode",
        example="meter",
        usage="To be chosen from the entries in UNTDID xxx",
    )


class Amount(
    BaseXmlModel,
    tag="ValueMeasure",
    ns="ram",
    nsmap=RAM,
):
    """ram:ValueMeasure"""

    value: float
    currency: Optional[str] = attr(
        name="currencyID",
        example="EUR",
        usage="ID of the currency",
    )
