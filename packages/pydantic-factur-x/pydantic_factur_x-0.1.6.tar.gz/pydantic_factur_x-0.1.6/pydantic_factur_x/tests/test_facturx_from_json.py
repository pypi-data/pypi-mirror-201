# ruff: noqa: F403, F405
"""Test output for factur-X.
"""
import json
import os

from pydantic_factur_x.factur_x import *


with open(
    os.path.join(os.path.dirname(__file__), "fixtures/invoice_1.json"),
    "r",
) as filed:
    doc = json.load(filed)


print(doc)
print("==================================================")
# doc.exchanged_document.included_notes[0]._nsmap = {"ram": "tutu:toto:tata"}
bytes_output = serialize(doc)
assert isinstance(bytes_output, bytes)  # nosec  # for mypy
output = bytes_output.decode("utf-8")
assert isinstance(output, str)  # nosec  # for mypy
print(output)
print("==================================================")

print(doc.__xml_tag__)
