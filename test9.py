import os
import json
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

key_file = os.environ.get('DI_KEY')
endpoint = os.environ.get('DI_ENDPOINT')

file_name = 'Dornbracht sample 1'

with open(f"./invoice_sample/{file_name}.pdf", "rb") as f:
    pdf_bytes = f.read()

def format_polygon(polygon):
    if polygon:
        return [{"x": point.x, "y": point.y} for point in polygon]
    return []

def analyze_layout():
    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key_file)
    )

    poller = document_analysis_client.begin_analyze_document(
        "prebuilt-invoice", pdf_bytes
    )

    result = poller.result()

    output = {
        "fields": {},
        "tables": {}
    }

    for idx, invoice in enumerate(result.documents):
        invoice_data = {}

        vendor_name = invoice.fields.get("VendorName")
        if vendor_name:
            invoice_data["VendorName"] = {"value": vendor_name.value, "confidence": vendor_name.confidence}

        vendor_address = invoice.fields.get("VendorAddress")
        if vendor_address:
            invoice_data["VendorAddress"] = {"value": vendor_address.value, "confidence": vendor_address.confidence}

        vendor_address_recipient = invoice.fields.get("VendorAddressRecipient")
        if vendor_address_recipient:
            invoice_data["VendorAddressRecipient"] = {"value": vendor_address_recipient.value, "confidence": vendor_address_recipient.confidence}

        customer_name = invoice.fields.get("CustomerName")
        if customer_name:
            invoice_data["CustomerName"] = {"value": customer_name.value, "confidence": customer_name.confidence}

        customer_id = invoice.fields.get("CustomerId")
        if customer_id:
            invoice_data["CustomerId"] = {"value": customer_id.value, "confidence": customer_id.confidence}

        customer_address = invoice.fields.get("CustomerAddress")
        if customer_address:
            invoice_data["CustomerAddress"] = {"value": customer_address.value, "confidence": customer_address.confidence}

        customer_address_recipient = invoice.fields.get("CustomerAddressRecipient")
        if customer_address_recipient:
            invoice_data["CustomerAddressRecipient"] = {"value": customer_address_recipient.value, "confidence": customer_address_recipient.confidence}

        invoice_id = invoice.fields.get("InvoiceId")
        if invoice_id:
            invoice_data["InvoiceId"] = {"value": invoice_id.value, "confidence": invoice_id.confidence}

        invoice_date = invoice.fields.get("InvoiceDate")
        if invoice_date:
            invoice_data["InvoiceDate"] = {"value": invoice_date.value, "confidence": invoice_date.confidence}

        invoice_total = invoice.fields.get("InvoiceTotal")
        if invoice_total:
            invoice_data["InvoiceTotal"] = {"value": invoice_total.value, "confidence": invoice_total.confidence}

        due_date = invoice.fields.get("DueDate")
        if due_date:
            invoice_data["DueDate"] = {"value": due_date.value, "confidence": due_date.confidence}

        purchase_order = invoice.fields.get("PurchaseOrder")
        if purchase_order:
            invoice_data["PurchaseOrder"] = {"value": purchase_order.value, "confidence": purchase_order.confidence}

        billing_address = invoice.fields.get("BillingAddress")
        if billing_address:
            invoice_data["BillingAddress"] = {"value": billing_address.value, "confidence": billing_address.confidence}

        billing_address_recipient = invoice.fields.get("BillingAddressRecipient")
        if billing_address_recipient:
            invoice_data["BillingAddressRecipient"] = {"value": billing_address_recipient.value, "confidence": billing_address_recipient.confidence}

        shipping_address = invoice.fields.get("ShippingAddress")
        if shipping_address:
            invoice_data["ShippingAddress"] = {"value": shipping_address.value, "confidence": shipping_address.confidence}

        shipping_address_recipient = invoice.fields.get("ShippingAddressRecipient")
        if shipping_address_recipient:
            invoice_data["ShippingAddressRecipient"] = {"value": shipping_address_recipient.value, "confidence": shipping_address_recipient.confidence}

        invoice_items = []
        for idx, item in enumerate(invoice.fields.get("Items").value):
            item_data = {}
            item_description = item.value.get("Description")
            if item_description:
                item_data["Description"] = {"value": item_description.value, "confidence": item_description.confidence}
            item_quantity = item.value.get("Quantity")
            if item_quantity:
                item_data["Quantity"] = {"value": item_quantity.value, "confidence": item_quantity.confidence}
            unit = item.value.get("Unit")
            if unit:
                item_data["Unit"] = {"value": unit.value, "confidence": unit.confidence}
            product_code = item.value.get("ProductCode")
            if product_code:
                item_data["ProductCode"] = {"value": product_code.value, "confidence": product_code.confidence}
            item_date = item.value.get("Date")
            if item_date:
                item_data["Date"] = {"value": item_date.value, "confidence": item_date.confidence}
            tax = item.value.get("Tax")
            if tax:
                item_data["Tax"] = {"value": tax.value, "confidence": tax.confidence}
            amount = item.value.get("Amount")
            if amount:
                item_data["Amount"] = {"value": amount.value, "confidence": amount.confidence}
            invoice_items.append(item_data)
        
        invoice_data["Items"] = invoice_items

        subtotal = invoice.fields.get("SubTotal")
        if subtotal:
            invoice_data["SubTotal"] = {"value": subtotal.value, "confidence": subtotal.confidence}

        total_tax = invoice.fields.get("TotalTax")
        if total_tax:
            invoice_data["TotalTax"] = {"value": total_tax.value, "confidence": total_tax.confidence}

        previous_unpaid_balance = invoice.fields.get("PreviousUnpaidBalance")
        if previous_unpaid_balance:
            invoice_data["PreviousUnpaidBalance"] = {"value": previous_unpaid_balance.value, "confidence": previous_unpaid_balance.confidence}

        amount_due = invoice.fields.get("AmountDue")
        if amount_due:
            invoice_data["AmountDue"] = {"value": amount_due.value, "confidence": amount_due.confidence}

        service_start_date = invoice.fields.get("ServiceStartDate")
        if service_start_date:
            invoice_data["ServiceStartDate"] = {"value": service_start_date.value, "confidence": service_start_date.confidence}

        service_end_date = invoice.fields.get("ServiceEndDate")
        if service_end_date:
            invoice_data["ServiceEndDate"] = {"value": service_end_date.value, "confidence": service_end_date.confidence}

        service_address = invoice.fields.get("ServiceAddress")
        if service_address:
            invoice_data["ServiceAddress"] = {"value": service_address.value, "confidence": service_address.confidence}

        service_address_recipient = invoice.fields.get("ServiceAddressRecipient")
        if service_address_recipient:
            invoice_data["ServiceAddressRecipient"] = {"value": service_address_recipient.value, "confidence": service_address_recipient.confidence}

        remittance_address = invoice.fields.get("RemittanceAddress")
        if remittance_address:
            invoice_data["RemittanceAddress"] = {"value": remittance_address.value, "confidence": remittance_address.confidence}

        remittance_address_recipient = invoice.fields.get("RemittanceAddressRecipient")
        if remittance_address_recipient:
            invoice_data["RemittanceAddressRecipient"] = {"value": remittance_address_recipient.value, "confidence": remittance_address_recipient.confidence}

        output["fields"][f"Invoice_{idx + 1}"] = invoice_data

    print(output)
    # with open("invoice_output.json", "w") as json_file:
    #     json.dump(output, json_file, indent=4)

if __name__ == "__main__":
    analyze_layout()
