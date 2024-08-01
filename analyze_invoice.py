import os
import json
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import AddressValue, CurrencyValue
from datetime import date
from typing import List
from dotenv import load_dotenv

load_dotenv()

# Custom JSON encoder to handle AddressValue, CurrencyValue, and date
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, AddressValue):
            return {
                "house_number": obj.house_number,
                "po_box": obj.po_box,
                "road": obj.road,
                "city": obj.city,
                "state": obj.state,
                "postal_code": obj.postal_code,
                "country_region": obj.country_region,
                "street_address": obj.street_address
            }
        if isinstance(obj, CurrencyValue):
            return {
                "amount": obj.amount,
                "symbol": obj.symbol
            }
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)

key_file = os.getenv('AZ_DI_KEY')
endpoint = os.getenv('AZ_DI_ENDPOINT')

def analyze_invoice(file_name):
    with open(f"./invoice_sample/{file_name}.pdf", "rb") as f:
        pdf_bytes = f.read()
    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key_file)
    )

    poller = document_analysis_client.begin_analyze_document(
        "prebuilt-invoice", pdf_bytes
    )

    result = poller.result()

    output = {}

    for idx, invoice in enumerate(result.documents):
        invoice_data = {}

        for field_name, field in invoice.fields.items():
            if field:
                if isinstance(field.value, list):
                    items_field = field
                    items_field_name = field_name
                    if items_field and items_field.value:
                        invoice_items = []
                        for idx, item in enumerate(items_field.value):
                            item_data = {}
                            for field_name, field in item.value.items():
                                if field and not isinstance(field.value, list):
                                    field_value = field.value
                                    item_data[field_name] = {
                                        "value": field_value, 
                                        "confidence": field.confidence
                                    }
                            invoice_items.append(item_data)
                    invoice_data[items_field_name] = invoice_items
                else: 
                    invoice_data[field_name] = {
                        "value": field.value,
                        "confidence": field.confidence
                    }

        output[f"Invoice_{idx + 1}"] = invoice_data

    with open(f"./invoice_sample/{file_name}.json", "w") as json_file:
        json.dump(output, json_file, indent=4, cls=CustomEncoder)

def analyze_invoices(file_names: List[str]):
    for file_name in file_names:
        analyze_invoice(file_name)
        print(f"done file {file_name}")

if __name__ == "__main__":
    analyze_invoice("B&B example 1")
