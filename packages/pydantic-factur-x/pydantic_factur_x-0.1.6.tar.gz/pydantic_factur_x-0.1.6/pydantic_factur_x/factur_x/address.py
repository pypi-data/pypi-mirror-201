"""Factur-X exchanged document.

Common address elements for all Factur-X documents.
"""
from typing import Optional
from pydantic_xml import BaseXmlModel, element

from ._nsmaps import RAM


class Address(
    BaseXmlModel,
    tag="Address",
    ns_attrs=True,
    ns="ram",
    nsmap=RAM,
):
    """ram:Address

    !!!! nsmap for elements are not generated in xml output, but it should.
         ex: nsmap for Address is generated, why post code is not?
    !!!!

    """

    postcode_code: Optional[str] = element(
        tag="PostcodeCode",
        ns="ram",
        example="12345",
        description="""The identifier for an addressable group of properties according
        to the relevant postal service.""",
        usage="Such as a ZIP code or a post code.",
    )
    line_one: Optional[str] = element(
        tag="LineOne",
        ns="ram",
        # nsmap=RAM,
        example="Line One",
        description="The main address line in an address.",
        usage="""Usually the street name and number or post office box.""",
    )
    line_two: Optional[str] = element(
        tag="LineTwo",
        ns="ram",
        # nsmap=RAM,
        example="Line two",
        description="""An additional address line in an address that can be used to
        give further details supplementing the main line.""",
    )
    line_three: Optional[str] = element(
        tag="LineThree",
        ns="ram",
        # nsmap=RAM,
        example="Line Three",
        description="""An additional address line in an address that can be used to
        give further details supplementing the main line.""",
    )
    city_name: Optional[str] = element(
        tag="CityName",
        ns="ram",
        # nsmap=RAM,
        example="City Name",
        description="""The common name of the city, town or village, where the
        Seller's address is located.""",
    )
    country_id: str = element(
        tag="CountryID",
        ns="ram",
        # nsmap=RAM,
        example="DE",
        description="""A code that identifies the country.""",
        usage="""The lists of valid countries are registered with the EN ISO 3166-1
        Maintenance agency, 
        “Codes for the representation of names of countries and their subdivisions”.""",
    )
    country_sub_division_name: Optional[str] = element(
        tag="CountrySubDivisionName",
        ns="ram",
        # nsmap=RAM,
        example="Country Sub Division Name",
        description="""The subdivision of a country.""",
        usage="""Such as a region, a county, a state, a province, etc.""",
    )
