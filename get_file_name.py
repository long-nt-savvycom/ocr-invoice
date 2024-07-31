import os

# Define the directory path
directory_path = './invoice_sample'

# Initialize an empty list to store the filenames without extensions
file_names = []

# Iterate over the files in the directory
for file in os.listdir(directory_path):
    # Get the filename without extension
    if file.endswith('.pdf'):
      file_name = os.path.splitext(file)[0]
      # Append to the list
      file_names.append(file_name)

print(file_names)