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


def can_join_strings(str1, str2):
    # Split the strings into words
    words1 = str1.split()
    words2 = str2.split()
    
    if not words1 or not words2:
        return False
    
    # Get the last word of the first string and the first word of the second string
    last_word_str1 = words1[-1]
    first_word_str2 = words2[0]
    
    # Check if the last word of str1 and the first word of str2 are the same (case-insensitive)
    if last_word_str1.lower() != first_word_str2.lower():
        return False
    
    # Check if the last character of str1 is not a punctuation mark
    if str1[-1] in string.punctuation:
        return False
    
    # Check if the first character of str2 is not uppercase
    if str2[0].isupper():
        return False
    
    return True

def analyze_layout():
    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key_file)
    )

    poller = document_analysis_client.begin_analyze_document(
        "prebuilt-document", pdf_bytes
    )

    result = poller.result()

    output = {
        "fields": {},
        "tables": {}
    }
    print(result);

    count = 1
    for page in result.pages:
        prevField = ""
        for line in page.lines:
            text = line.content
            if ":" in text:
                key, value = map(str.strip, text.split(":", 1))
                prevField = key
                output["fields"][key] = value
            else:
                print(f"prevField : {prevField}")
                if  prevField != "" and output["fields"][prevField] == "":
                    print(f"prevField <> "" : {prevField}")
                    output["fields"][prevField] = text

                elif prevField != "" and output["fields"][prevField] != "" and can_join_strings(output["fields"][prevField], text):
                    output["fields"][prevField] += text
                else:
                    print(f"prevField == "" : {prevField}")
                    output["fields"][f"miss_key_{count}"] = text
                    count += 1



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
    with open(f"./invoice_sample/{file_name}_document.json", "w", encoding="utf-8") as json_file:
        json.dump(output, json_file, indent=4)

    print(f"JSON output written to ./invoice_sample/{file_name}.json")

if __name__ == "__main__":
    analyze_layout()
