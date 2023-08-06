"""Factur-X document context.

Insert specific Factur-X elements here.
"""
from enum import Enum
from typing import Optional
from pydantic_xml import BaseXmlModel, attr, element

from ._nsmaps import RSM, UDT, QTD, RAM, XSI


from .common import BoolIndicator


class BusinessProcessSpecifiedDocumentContextParameter(
    BaseXmlModel,
    tag="BusinessProcessSpecifiedDocumentContextParameter",
    ns_attrs=True,
    ns="ram",
    nsmap=RAM,
):
    """ram:BusinessProcessSpecifiedDocumentContextParameter

    Profiles:
        - Factur-X: minimum
        - Order-X: basic
    """

    id: Optional[str] = element(tag="ID", ns="ram", example="A1")


class GuidelineSpecifiedDocumentContextParameterEnum(str, Enum):
    """Enum for all possible values for GuidelineSpecifiedDocumentContextParameter."""

    FACTUR_X_MINIMUM = "urn:factur-x.eu:1p0:minimum"
    FACTUR_X_BASIC_WL = "urn:factur-x.eu:1p0:basicwl"
    FACTUR_X_BASIC = "urn:cen.eu:en16931:2017#compliant#urn:factur-x.eu:1p0:basic"
    FACTUR_X_COMFORT = "urn:cen.eu:en16931:2017"
    # FACTUR_X_EN_16931 = "urn:cen.eu:en16931:2017"
    FACTUR_X_EXTENDED = (
        "urn:cen.eu:en16931:2017#conformant#urn:factur-x.eu:1p0:extended"
    )
    ORDER_X_BASIC = "urn:order-x.eu:1p0:basic"
    ORDER_X_COMFORT = "urn:order-x.eu:1p0:comfort"
    ORDER_X_EXTENDED = "urn:order-x.eu:1p0:extended"


class GuidelineSpecifiedDocumentContextParameter(
    BaseXmlModel,
    tag="GuidelineSpecifiedDocumentContextParameter",
    ns_attrs=True,
    ns="ram",
    nsmap=RAM,
):
    """ram:GuidelineSpecifiedDocumentContextParameter

    Profiles:
        - Factur-X: minimum
        - Order-X: basic
    """

    id: Optional[GuidelineSpecifiedDocumentContextParameterEnum] = element(
        tag="ID",
        ns="ram",
        # nsmap=RAM,
        example="urn:factur-x.eu:1p0:basicwl",
        profiles={"factur-x": "minimum", "order-x": "basic"},
        description="""An identification of the specification containing the total
        set of rules regarding semantic content, cardinalities and business rules
        to which the data contained in the instance document conforms.""",
        usage="""This identifies compliance or conformance to this document.
        Compliant invoices specify: urn:cen.eu:en16931:2017.
        Invoices, compliant to a user specification may identify that use
        specification here.
        No identification scheme is to be used.""",
    )


class ExchangedDocumentContext(
    BaseXmlModel,
    tag="ExchangedDocumentContext",
    ns_attrs=True,
    ns="rsm",
    nsmap=RSM,
):
    """rsm:ExchangedDocumentContext

    Profiles:
        - Factur-X: minimum
        - Order-X: basic
    """

    test_indicator: Optional[BoolIndicator] = element(
        tag="TestIndicator",
        ns="ram",
        # nsmap=RAM,
        profiles={"factur-x": "minimum", "order-x": "basic"},
    )
    business_process_specified_document_context_parameter: Optional[
        BusinessProcessSpecifiedDocumentContextParameter
    ] = element(
        ns="ram",
        profiles={"factur-x": "extended", "order-x": "basic"},
    )
    guideline_specified_document_context_parameter: GuidelineSpecifiedDocumentContextParameter = element(
        ns="ram",
        profiles={"factur-x": "minimum", "order-x": "basic"},
    )
