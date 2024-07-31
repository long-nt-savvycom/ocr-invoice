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

    for page in result.pages:
        for line in page.lines:
            text = line.content
            if ":" in text:
                key, value = map(str.strip, text.split(":", 1))
                output["fields"][key] = value

    table_counter = 1
    for table_idx, table in enumerate(result.tables):
        table_data = {
            "header": [],
            "rows": []
        }

        # Get headers if they exist
        header_cells = [cell for cell in table.cells if cell.kind == "columnHeader"]
        if header_cells:
            table_data["header"] = [cell.content for cell in header_cells]

        # Get rows
        max_row_index = max(cell.row_index for cell in table.cells)
        for row_index in range(max_row_index + 1):
            row = [cell.content for cell in table.cells if cell.row_index == row_index]
            table_data["rows"].append(row)

        output["tables"][f"table{table_counter}"] = table_data
        table_counter += 1

    # Write the output to a JSON file
    with open(f"./invoice_sample/{file_name}.json", "w", encoding="utf-8") as json_file:
        json.dump(output, json_file, indent=4)

    print(f"JSON output written to ./invoice_sample/{file_name}.json")

if __name__ == "__main__":
    analyze_layout()
