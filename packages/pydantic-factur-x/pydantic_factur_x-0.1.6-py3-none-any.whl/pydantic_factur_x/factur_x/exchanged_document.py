"""Factur-X exchanged document.

Insert specific Factur-X elements here.
"""
from enum import Enum
from typing import Optional, List
from pydantic_xml import BaseXmlModel, attr, element

from ._nsmaps import RSM, UDT, QTD, RAM, XSI

from .code_lists import UntDid1001, UntDid1373, UntDid4451
from .common import DateTime, IncludedNote


class CopyIndicator(
    BaseXmlModel,
    tag="CopyIndicator",
    ns_attrs=True,
    ns="ram",
    nsmap=RAM,
):
    """ram:CopyIndicator

    Profiles:
        - Factur-X: extended
        - Order-X: basic
    """

    indicator: bool = element(
        tag="Indicator",
        default="false",
        ns="udt",
        nsmap=UDT,
        example="false",
        profiles={"factur-x": "extended", "order-x": "basic"},
        description="Indicates if the document is a copy.",
    )


class PurposeCodeEnum(str, Enum):
    """Enum for all possible values for PurposeCode.

    Order-x only
    """

    DUPLICATE = "7"
    ORIGINAL = "9"
    RETRANSMISSION = "35"


class RequestedResponseTypeCodeEnum(str, Enum):
    """Enum for all possible values for RequestedResponseTypeCode.

    Order-x only
    """

    ORDER_RESPONSE = "AC"


class EffectiveSpecifiedPeriod(
    BaseXmlModel,
    tag="EffectiveSpecifiedPeriod",
    ns_attrs=True,
    ns="ram",
    nsmap=RAM,
):
    """ram:EffectiveSpecifiedPeriod

    Profiles:
        - Factur-X: extended
        - Order-X: comfort
    """

    start_date_time: Optional[DateTime] = element(
        tag="StartDateTime",
        ns="ram",
        # nsmap=RAM,
        profiles={"factur-x": None, "order-x": "comfort"},
        usage="For Order-x",
    )
    end_date_time: Optional[DateTime] = element(
        tag="EndDateTime",
        ns="ram",
        # nsmap=RAM,
        profiles={"factur-x": None, "order-x": "comfort"},
        usage="for order-x",
    )
    # TODO: add a pydantic custom validator to make this mandatory
    #       when profile is factur-x:
    complete_date_time: Optional[DateTime] = element(
        tag="EndDateTime",
        ns="ram",
        # nsmap=RAM,
        profiles={"factur-x": "extended", "order-x": None},
        usage="""for factur-X, mandatory in factur-X if the
        EffectiveSpecifiedPeriod is used""",
    )


class ExchangedDocument(
    BaseXmlModel,
    tag="ExchangedDocument",
    ns_attrs=True,
    ns="rsm",
    nsmap=RSM,
):
    """rsm:ExchangedDocument

    Profiles:
        - Factur-X: minimum
        - Order-X: basic
    """

    id: str = element(
        tag="ID",
        ns="ram",
        nsmap=RAM,
        example="FACT-00001",
        profiles={"factur-x": "minimum", "order-x": "basic"},
        description="A unique identification of the Invoice.",
        usage="""The sequential number required in Article 226(2) of the
        directive 2006/112/EC [2], to uniquely identify the Invoice within the business
        context, time-frame, operating systems and records of the Seller. 
        It may be based on one or more series of numbers, which may include alphanumeric
        characters. No identification scheme is to be used.""",
    )
    name: Optional[str] = element(
        tag="Name",
        ns="ram",
        nsmap=RAM,
        example="FACT-00001",
        profiles={"factur-x": "extended", "order-x": "basic"},
        description="A freetext name of the invoice document.",
    )
    type_code: UntDid1001 = element(
        tag="TypeCode",
        ns="ram",
        nsmap=RAM,
        example="380",
        profiles={"factur-x": "minimum", "order-x": "basic"},
        description="A code specifying the functional type of the Invoice or the Order.",
        usage="""Commercial invoices and credit notes are defined according
        the entries in UNTDID 1001 [6].
        Other entries of UNTDID 1001 [6] with specific invoices or
        credit notes may be used if applicable.""",
    )
    status_code: Optional[UntDid1373] = element(
        tag="StatusCode",
        ns="ram",
        nsmap=RAM,
        example="1",
        profiles={"factur-x": None, "order-x": "basic"},
        description="The code specifying the status of this exchanged document.",
        usage="""To be chosen from the entries in UNTDID 1373. Order-x usage only.""",
    )
    issue_date_time: DateTime = element(
        tag="IssueDateTime",
        ns="ram",
        # nsmap=RAM,
    )
    copy_indicator: Optional[CopyIndicator] = element(
        tag="CopyIndicator",
        ns="ram",
        # nsmap=RAM,
        profiles={"factur-x": "extended", "order-x": "basic"},
    )
    language_ids: Optional[List[str]] = element(  # TODO: filter by ISO 639-1
        tag="LanguageID",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": "extended", "order-x": "extended"},
        description="A unique identifier for a language used in this exchanged document.",
        usage="""To be chosen from the entries in UNTDID 3453 / ISO 639-1.""",
    )
    purpose_code: Optional[PurposeCodeEnum] = element(
        tag="PurposeCode",
        ns="ram",
        nsmap=RAM,
        profiles={"factur-x": None, "order-x": "basic"},
        description="""The purpose, expressed as text, of this exchanged document.
        Order-x only.""",
        usage="""Potential values:
        7 : Duplicate
        9 : Original
        35 : Retransmission""",
    )
    requested_response_type_code: Optional[RequestedResponseTypeCodeEnum] = element(
        tag="RequestedResponseTypeCode",
        ns="ram",
        # nsmap=RAM,
        profiles={"factur-x": None, "order-x": "basic"},
        description="""A code specifying a type of response requested for this exchanged
        document.
        Order-x only.""",
        usage="""Value = AC to request an Order_Response""",
    )
    included_notes: Optional[List[IncludedNote]] = element(
        tag="IncludedNote",
        ns="ram",
        # nsmap=RAM,
        profiles={"factur-x": "basic_wl", "order-x": "basic"},
        description="""A group of business terms providing textual notes that are relevant
        for the document, together with an indication of the note subject.""",
    )
    effective_specified_period: Optional[EffectiveSpecifiedPeriod] = element(
        tag="EffectiveSpecifiedPeriod",
        ns="ram",
        # nsmap=RAM,
        profiles={"factur-x": "extended", "order-x": "comfort"},
        description=""" The specified period within which this exchanged document
        is effective""",
    )
