import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from azure.core.credentials import AzureKeyCredential

# Replace with your Azure Form Recognizer endpoint and key
# endpoint = "https://<your-form-recognizer-endpoint>.cognitiveservices.azure.com/"
# api_key = "<your-form-recognizer-api-key>"
api_key = os.environ.get('DI_KEY')
# key = "abc";
endpoint = os.environ.get('DI_ENDPOINT')

# Initialize the client
client = DocumentIntelligenceClient(endpoint, AzureKeyCredential(api_key))

# Read the PDF file as bytes
with open("./invoice_sample/LIN-0223100266.pdf", "rb") as f:
    pdf_bytes = f.read()

# Create an AnalyzeDocumentRequest instance with the bytes_source parameter
request = AnalyzeDocumentRequest(bytes_source=pdf_bytes)

# Now you can use the client to analyze the document
poller = client.begin_analyze_document("prebuilt-invoice", request)
result = poller.result()

# Convert the result to JSON and print
import json
result_json = result.to_dict()
print(json.dumps(result_json, indent=4))
