import os
import json

def analyze_confidence(data):
    count_high_confidence = 0
    count_low_confidence = 0
    total_confidence_fields = 0

    def traverse_json(obj):
        global count_high_confidence, count_low_confidence, total_confidence_fields
        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, dict):
                    print(value)
                    # Check if this dictionary contains a confidence field
                    if "confidence" in value:
                        confidence = value.get("confidence")
                        if confidence is not None:
                            total_confidence_fields += 1
                            if confidence > 0.8:
                                count_high_confidence += 1
                            elif confidence < 0.5:
                                count_low_confidence += 1
                    # Recursively traverse nested dictionaries
                    traverse_json(value)
                elif isinstance(value, list):
                    # Recursively traverse lists
                    for item in value:
                        traverse_json(item)

                # Start traversal
                traverse_json(data)

    return {
        'count_high_confidence': count_high_confidence,
        'count_low_confidence': count_low_confidence,
        'total_confidence_fields': total_confidence_fields
    }


# Iterate over the JSON files in the directory

# Define the directory where your JSON files are located
directory_path = "./invoice_sample"

# Initialize counters
for file_name in os.listdir(directory_path):
    if file_name.endswith(".json"):
        file_path = os.path.join(directory_path, file_name)

        with open(file_path, "r") as json_file:
            data = json.load(json_file)

        # Analyze confidence fields
        summary = analyze_confidence(data)

        # Define the output file path
        output_file_path = os.path.join(directory_path,
                                        f"{file_name}_confidence_summary.json")

        # Write the summary to the output file
        with open(output_file_path, "w") as output_file:
            json.dump(summary, output_file, indent=4)

print(f"Summary written to {output_file_path}")
