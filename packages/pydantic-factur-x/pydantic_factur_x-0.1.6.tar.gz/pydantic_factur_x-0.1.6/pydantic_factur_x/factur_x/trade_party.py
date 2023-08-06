"""Factur-X exchanged document.

Common trade party objects for all Factur-X documents.
"""
from enum import Enum
from typing import Optional, List
from pydantic_xml import BaseXmlModel, attr, element

from ._nsmaps import RSM, UDT, QTD, RAM, XSI
from .code_lists import UntDid1229
from .common import BoolIndicator, IncludedNote, GlobalID, ValueMeasure, Quantity
from .address import Address
from .contact import Email, Contact


class SpecifiedLegalOrganization(
    BaseXmlModel,
    tag="SpecifiedLegalOrganization",
    ns_attrs=True,
    ns="ram",
    nsmap=RAM,
):
    """ram:SpecifiedLegalOrganization"""

    id: Optional[GlobalID] = element(
        tag="ID",
        ns="ram",
        # nsmap=RAM,
        profiles={"factur-x": "basic_wl", "order-x": "basic"},
        description="""An identifier issued by an official registrar that identifies the
        Party as a legal entity or person.
        The identification scheme identifier of the party legal
        registration identifier.""",
        usage="""If no identification scheme is specified, 
        it should be known by the parties, e.g. the identifier that is 
        exclusively used in the applicable legal environment.
        If used, the identification scheme shall be chosen from the entries of 
        the list published by the ISO/IEC 6523 maintenance agency.""",
    )
    trading_business_name: Optional[str] = element(
        tag="TradingBusinessName",
        ns="ram",
        # nsmap=RAM,
    )


class SpecifiedTaxRegistration(
    BaseXmlModel,
    tag="SpecifiedTaxRegistration",
    ns_attrs=True,
    ns="ram",
    nsmap=RAM,
):
    """ram:SpecifiedTaxRegistration"""

    id: GlobalID = element(
        tag="ID",
        ns="ram",
        # nsmap=RAM,
        profiles={"factur-x": "basic_wl", "order-x": "basic"},
        description="""The local identification (defined by the Party's address) of
        the Party for tax purposes or a reference that enables
        the other Party to state his registered tax status.""",
    )


class TradeParty(
    BaseXmlModel,
    tag="SellerTradeParty",
    ns_attrs=True,
    ns="ram",
    nsmap=RAM,
):
    """ram:SellerTradeParty

    level: 2

    Profiles:
        - Factur-X: minimum
        - Order-X: basic
    """

    id: Optional[str] = element(
        tag="ID",
        ns="ram",
        # nsmap=RAM,
        profiles={"factur-x": "basic_wl", "order-x": "basic"},
        description="""An identification of the Seller.
        The identification scheme identifier of the Seller identifier.""",
        usage="""For many systems, the Seller identifier is a key piece of information.
        Multiple Seller identifiers may be assigned or specified.
        They may be differentiated by using various identification schemes.
        If no scheme is specified, it should be known by Buyer and Seller,
        e.g. a previously exchanged Buyer assigned identifier of the Seller.
        If used, the identification scheme identifier shall be chosen from the entries
        of the list published by the ISO/IEC 6523 maintenance agency.""",
    )
    global_id: Optional[GlobalID] = element(
        tag="GlobalID",
        ns="ram",
        # nsmap=RAM,
        profiles={"factur-x": "basic_wl", "order-x": "basic"},
        description="""An item identifier based on a registered scheme.
        The identification scheme identifier of the Item standard identifier.""",
        usage="""The identification scheme shall be identified from the entries of the
        list published by the ISO/IEC 6523 maintenance agency.""",
    )
    name: str = element(
        tag="Name",
        ns="ram",
        # nsmap=RAM,
        profiles={"factur-x": "minimum", "order-x": "basic"},
        description="""trade party name""",
        usage="""The full formal name by which the Seller is registered in the national
        registry of legal entities or as a Taxable person or otherwise trades
        as a person or persons.""",
    )
    description: Optional[str] = element(
        tag="Description",
        ns="ram",
        # nsmap=RAM,
        profiles={"factur-x": "comfort", "order-x": "comfort"},
        description="""Additional legal information relevant for the Seller.""",
    )
    specified_legal_organization: Optional[SpecifiedLegalOrganization] = element(
        tag="SpecifiedLegalOrganization",
        ns="ram",
        # nsmap=RAM,
    )
    legal_postal_trade_address: Optional[Address] = element(
        tag="PostalTradeAddress",
        ns="ram",
        # nsmap=RAM,
    )
    defined_trade_contacts: Optional[List[Contact]] = element(
        tag="DefinedTradeContact",
        ns="ram",
        # nsmap=RAM,
    )
    postal_trade_address: Address = element(
        tag="PostalTradeAddress",
        ns="ram",
        # nsmap=RAM,
    )
    electronic_address: Optional[Email] = element(
        tag="URIUniversalCommunication",
        ns="ram",
        # nsmap=RAM,
    )
    vat_registrations: Optional[List[SpecifiedTaxRegistration]] = element(
        tag="SpecifiedTaxRegistration",
        ns="ram",
        # nsmap=RAM,
    )
    tax_registrations: Optional[List[SpecifiedTaxRegistration]] = element(
        tag="SpecifiedTaxRegistration",
        ns="ram",
        # nsmap=RAM,
    )
