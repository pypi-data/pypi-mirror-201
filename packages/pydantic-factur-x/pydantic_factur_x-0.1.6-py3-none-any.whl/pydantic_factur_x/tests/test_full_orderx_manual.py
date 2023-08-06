# ruff: noqa: F403, F405
"""Test output for factur-X.
"""
import json
from pydantic_factur_x.factur_x import *


doc = RootOrderX(  # RootFacturX(  # RootOrderX(
    exchanged_document_context=ExchangedDocumentContext(
        test_indicator=BoolIndicator(indicator=True),
        business_process_specified_document_context_parameter=BusinessProcessSpecifiedDocumentContextParameter(
            id="testID"
        ),
        guideline_specified_document_context_parameter=GuidelineSpecifiedDocumentContextParameter(
            id="urn:cen.eu:en16931:2017#conformant#urn:factur-x.eu:1p0:extended"
        ),
    ),
    exchanged_document=ExchangedDocument(
        id="fact-000001",
        name="Facture",
        type_code="380",
        issue_date_time=DateTime(
            date_time_string=DateTimeString(text="20201201", format="102")
        ),
        copy_indicator=CopyIndicator(indicator=False),
        # language_ids=["fr", "de", "en"],
        language_ids=[
            "fr",
        ],
        purpose_code="9",
        requested_response_type_code="AC",
        included_notes=[
            IncludedNote(
                content_code="AAA",
                content="This is a test invoice.",
                subject_code="AAA",
            ),
            IncludedNote(
                content="FOURNISSEUR F SARL au capital de 50 000 EUR",
                subject_code="REG",
            ),
            IncludedNote(
                content="""Tout retard de paiement engendre une pénalité exigible à
                compter de la date d'échéance, calculée sur la base de trois fois le
                taux d'intérêt légal.""",
                subject_code="PMD",
            ),
        ],
        effective_specified_period=EffectiveSpecifiedPeriod(
            start_date_time=DateTime(
                date_time_string=DateTimeString(text="20201201", format="102")
            ),
            end_date_time=DateTime(
                date_time_string=DateTimeString(text="20201202", format="102")
            ),
        ),
    ),
    supply_chain_trade_transaction=SupplyChainTradeTransaction(
        included_supply_chain_trade_line_items=[
            IncludedSupplyChainTradeLineItem(
                associated_document_line_document=AssociatedDocumentLineDocument(
                    line_id="1",
                    included_notes=[
                        IncludedNote(
                            content="FOURNISSEUR F SARL au capital de 50 000 EUR",
                            subject_code="REG",
                        ),
                        IncludedNote(
                            content_code="AAA",
                            content="This is a test invoice.",
                            subject_code="AAA",
                        ),
                    ],
                ),
                specified_trade_product=SpecifiedTradeProduct(
                    id="1234567890123",
                    global_id=GlobalID(id="9876543210321", scheme_id="0160"),
                    seller_assigned_id="seller_id",
                    buyer_assigned_id="buyer_id",
                    industry_assigned_id="industry_id",
                    model_id="model_id",
                    name="Product name",
                    description="Product description",
                    batch_id="batch_id",
                    brand_name="brand_name",
                    model_name="model_name",
                    applicable_product_characteristics=[
                        ApplicableProductCharacteristic(
                            description="color", value="red"
                        ),
                    ],
                ),
                specified_line_trade_agreement=SpecifiedLineTradeAgreement(
                    minimum_product_orderable_quantity=Quantity(
                        value=1, unit_code="C62"
                    ),
                    gross_price_product_trade_price=GrossPriceProductTradePrice(
                        charge_amount="12.12",
                        basis_quantity=Quantity(value=1.0, unit_code="C62"),
                    ),
                    net_price_product_trade_price=NetPriceProductTradePrice(
                        charge_amount="12.12",
                        basis_quantity=Quantity(value=1.0, unit_code="C62"),
                    ),
                ),
                specified_line_trade_delivery=SpecifiedLineTradeDelivery(
                    partial_delivery_allowed_indicator=BoolIndicator(indicator=False),
                    requested_quantity=Quantity(value=100.0, unit_code="C62"),
                    agreed_quantity=Quantity(value=112.0, unit_code="C62"),
                    package_quantity=Quantity(value=10.0, unit_code="C62"),
                    per_package_unit_quantity=Quantity(value=10.0, unit_code="C62"),
                ),
                specified_line_trade_settlement=SpecifiedLineTradeSettlement(
                    applicable_trade_tax=ApplicableTradeTax(
                        calculated_amount=12.32,
                        type_code="VAT",
                        exemption_reason="exemption reason",
                        category_code="S",
                        exemption_reason_code="CODE",
                        rate_applicable_percent=20.0,
                    ),
                    specified_trade_settlement_line_monetary_summation=SpecifiedTradeSettlementLineMonetarySummation(
                        line_total_amount=12.32,
                        charge_total_amount=12.32,
                        allowance_total_amount=12.32,
                        tax_total_amount=33.22,
                        total_allowance_charge_amount=12.32,
                    ),
                ),
            )
        ],
        applicable_header_trade_agreement=ApplicableHeaderTradeAgreement(
            buyer_reference="buyer_reference",
            seller_trade_party=TradeParty(
                id="seller_id",
                global_id=GlobalID(id="9876543210321", scheme_id="0160"),
                name="Seller name",
                description="details about seller",
                postal_trade_address=Address(
                    line_one="line one",
                    line_two="line two",
                    postcode_code="12345",
                    city_name="city name",
                    country_id="FR",
                ),
            ),
            buyer_trade_party=TradeParty(
                id="buyer_id",
                global_id=GlobalID(id="9876543210321", scheme_id="0160"),
                name="Buyer name",
                description="details about buyer",
                postal_trade_address=Address(
                    line_one="line one",
                    line_two="line two",
                    postcode_code="12345",
                    city_name="city name",
                    country_id="FR",
                ),
            ),
        ),
        applicable_header_trade_delivery=ApplicableHeaderTradeDelivery(),
        header_trade_settlement=ApplicableHeaderTradeSettlement(
            order_currency_code="EUR",
            applicable_trade_taxes=[
                ApplicableTradeTax(
                    calculated_amount=3.34,  # total vat for this vat
                    type_code="VAT",
                    basis_amount=5.22,
                    category_code="S",
                    rate_applicable_percent="20",
                ),
                ApplicableTradeTax(
                    calculated_amount=5.22,  # total vat for this vat
                    type_code="VAT",
                    basis_amount=6.44,
                    category_code="S",
                    rate_applicable_percent="5.5",
                ),
            ],
            total_amounts=SpecifiedTradeSettlementHeaderMonetarySummation(
                line_total_amount=42.42,
            ),
        ),
    ),
)

print(json.dumps(json.loads(doc.json()), indent=4))
print("==================================================")
# doc.exchanged_document.included_notes[0]._nsmap = {"ram": "tutu:toto:tata"}
bytes_output = serialize(doc)
assert isinstance(bytes_output, bytes)  # nosec  # for mypy
output = bytes_output.decode("utf-8")
assert isinstance(output, str)  # nosec  # for mypy
print(output)
print("==================================================")

print(doc.__xml_tag__)
