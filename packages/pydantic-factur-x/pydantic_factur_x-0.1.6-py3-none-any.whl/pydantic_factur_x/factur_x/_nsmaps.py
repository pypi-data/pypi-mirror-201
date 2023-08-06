"""All Nsmaps used in documents.

namespace maps differs for order-x and factur-x.
"""

# default namespace map - indifferent for order-x and factur-x
RSM = {
    "rsm": "urn:rsm"
    # "rsm": "urn:un:unece:uncefact:data:SCRDMCCBDACIOMessageStructure:100",  # order-x
    # "rsm": "urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100",  # factur-x
}

UDT = {
    "udt": "urn:udt"
    # "udt": "urn:un:unece:uncefact:data:standard:UnqualifiedDataType:128",  # order-x
    # "udt": "urn:un:unece:uncefact:data:standard:UnqualifiedDataType:100",  # factur-x
}

QTD = {
    "qtd": "urn:qtd"
    # "qtd": "urn:un:unece:uncefact:data:standard:QualifiedDataType:128",  # order-x
    # "qtd": "urn:un:unece:uncefact:data:standard:QualifiedDataType:100",  # factur-x
}

RAM = {
    "ram": "urn:ram"
    # "ram": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:128",  # order-x
    # "ram": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",  # factur-x
}

XSI = {
    "xsi": "urn:xsi",
    # "xsi": "http://www.w3.org/2001/XMLSchema-instance",  # order-x
    # "xsi": "http://www.w3.org/2001/XMLSchema-instance"  # factur-x
}


DEFAULT_TO_ORDER_X = {
    'xmlns:rsm="urn:rsm"': 'xmlns:rsm="urn:un:unece:uncefact:data:SCRDMCCBDACIOMessageStructure:100"',
    'xmlns:udt="urn:udt"': 'xmlns:udt="urn:un:unece:uncefact:data:standard:UnqualifiedDataType:128"',
    'xmlns:qtd="urn:qtd"': 'xmlns:qtd="urn:un:unece:uncefact:data:standard:QualifiedDataType:128"',
    'xmlns:ram="urn:ram"': 'xmlns:ram="urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:128"',
    'xmlns:xsi="urn:xsi"': 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
}

DEFAULT_TO_FACTUR_X = {
    'xmlns:rsm="urn:rsm"': 'xmlns:rsm="urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100"',
    'xmlns:udt="urn:udt"': 'xmlns:udt="urn:un:unece:uncefact:data:standard:UnqualifiedDataType:100"',
    'xmlns:qtd="urn:qtd"': 'xmlns:qtd="urn:un:unece:uncefact:data:standard:QualifiedDataType:100"',
    'xmlns:ram="urn:ram"': 'xmlns:ram="urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100"',
    'xmlns:xsi="urn:xsi"': 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
}
