import os
import json
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

key = os.environ.get('DI_KEY')
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
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    poller = document_analysis_client.begin_analyze_document(
        "prebuilt-invoice", pdf_bytes
    )

    result = poller.result()

    output = {
        "styles": [],
        "pages": [],
        "tables": []
    }

    for idx, style in enumerate(result.styles):
        output["styles"].append({
            "content": "handwritten" if style.is_handwritten else "no handwritten"
        })

    for page in result.pages:
        page_data = {
            "page_number": page.page_number,
            "width": page.width,
            "height": page.height,
            "unit": page.unit,
            "lines": [],
            "selection_marks": []
        }

        for line_idx, line in enumerate(page.lines):
            words = line.get_words()
            line_data = {
                "line_index": line_idx,
                "word_count": len(words),
                "text": line.content,
                "polygon": format_polygon(line.polygon),
                "words": []
            }

            for word in words:
                line_data["words"].append({
                    "text": word.content,
                    "confidence": word.confidence
                })

            page_data["lines"].append(line_data)

        for selection_mark in page.selection_marks:
            page_data["selection_marks"].append({
                "state": selection_mark.state,
                "polygon": format_polygon(selection_mark.polygon),
                "confidence": selection_mark.confidence
            })

        output["pages"].append(page_data)

    for table_idx, table in enumerate(result.tables):
        table_data = {
            "table_index": table_idx,
            "row_count": table.row_count,
            "column_count": table.column_count,
            "bounding_regions": [],
            "cells": []
        }

        for region in table.bounding_regions:
            table_data["bounding_regions"].append({
                "page_number": region.page_number,
                "polygon": format_polygon(region.polygon)
            })

        for cell in table.cells:
            cell_data = {
                "row_index": cell.row_index,
                "column_index": cell.column_index,
                "content": cell.content,
                "bounding_regions": []
            }
            for region in cell.bounding_regions:
                cell_data["bounding_regions"].append({
                    "page_number": region.page_number,
                    "polygon": format_polygon(region.polygon)
                })
            table_data["cells"].append(cell_data)

        output["tables"].append(table_data)

    # Write the output to a JSON file
    with open(f"./invoice_sample/{file_name}.json", "w", encoding="utf-8") as json_file:
        json.dump(output, json_file, indent=4)

    print("JSON output written to output.json")

if __name__ == "__main__":
    analyze_layout()
