"""Pydantic XML models for Factur-X and Order-X schemas."""
from pydantic_xml import BaseXmlModel, element


from .document_context import ExchangedDocumentContext
from .exchanged_document import ExchangedDocument
from .supply_chain_trade_transaction import SupplyChainTradeTransaction
from ._nsmaps import RSM, UDT, QTD, RAM, XSI, DEFAULT_TO_ORDER_X, DEFAULT_TO_FACTUR_X


class SCRDMCCBDACIOMessageStructure(
    BaseXmlModel,
    tag="SCRDMCCBDACIOMessageStructure",
    ns_attrs=True,
    ns="rsm",
    nsmap=RSM | UDT | QTD | RAM | XSI,
    # nsmap={
    #     "rsm": "urn:un:unece:uncefact:data:SCRDMCCBDACIOMessageStructure:100",
    #     "udt": "urn:un:unece:uncefact:data:standard:UnqualifiedDataType:128",
    #     "qtd": "urn:un:unece:uncefact:data:standard:QualifiedDataType:128",
    #     "ram": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:128",
    #     "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    # },
):
    """Root Factur-X and Order-X element.

    nsmaps are fully definied here.
    """

    exchanged_document_context: ExchangedDocumentContext = element(
        ns="rsm",
        profiles={"factur-x": "minimum", "order-x": "basic"},
        description="""A group of business terms providing information on the business
        process and rules applicable to the Invoice document.""",
    )
    exchanged_document: ExchangedDocument = element(
        ns="rsm",
        profiles={"factur-x": "minimum", "order-x": "basic"},
    )
    supply_chain_trade_transaction: SupplyChainTradeTransaction = element(
        ns="rsm",
        profiles={"factur-x": "minimum", "order-x": "basic"},
    )


class CrossIndustryInvoice(
    BaseXmlModel,
    tag="CrossIndustryInvoice",
    ns_attrs=True,
    ns="rsm",
    nsmap=RSM | UDT | QTD | RAM | XSI,
    # nsmap={
    #     "rsm": "urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100",
    #     "udt": "urn:un:unece:uncefact:data:standard:UnqualifiedDataType:100",
    #     "qtd": "urn:un:unece:uncefact:data:standard:QualifiedDataType:100",
    #     "ram": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
    #     "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    # },
):
    """Root Factur-X and Order-X element.

    nsmaps are fully definied here.
    """

    exchanged_document_context: ExchangedDocumentContext = element(
        ns="rsm",
        profiles={"factur-x": "minimum", "order-x": "basic"},
        description="""A group of business terms providing information on the business
        process and rules applicable to the Invoice document.""",
    )
    exchanged_document: ExchangedDocument = element(
        ns="rsm",
        profiles={"factur-x": "minimum", "order-x": "basic"},
    )
    supply_chain_trade_transaction: SupplyChainTradeTransaction = element(
        ns="rsm",
        profiles={"factur-x": "minimum", "order-x": "basic"},
    )


# Alias for the root element
RootOrderX = SCRDMCCBDACIOMessageStructure
RootFacturX = CrossIndustryInvoice


def serialize(doc) -> bytes:
    """Serialize a document to XML."""
    bytes_xml = doc.to_xml(
        method="xml",
        pretty_print=True,
        encoding="utf-8",
        skip_empty=True,
        standalone=None,
        xml_declaration=True,
    )
    assert isinstance(bytes_xml, bytes)  # nosec  # for mypy
    xml = bytes_xml.decode("utf-8")
    if doc.__xml_tag__ == "SCRDMCCBDACIOMessageStructure":
        for key, value in DEFAULT_TO_ORDER_X.items():
            xml = xml.replace(key, value)
    elif doc.__xml_tag__ == "CrossIndustryInvoice":
        for key, value in DEFAULT_TO_FACTUR_X.items():
            xml = xml.replace(key, value)
    return xml.encode("utf-8")
