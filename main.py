from get_files_name import get_file_names
from analyze_invoice import analyze_invoices

def main():
    # Define the directory path for PDF files
    directory_path = './invoice_sample'
    
    # Get the list of filenames without extensions
    file_names = get_file_names(directory_path)
    
    # Print the filenames and their count (for verification)
    print(file_names)
    print(len(file_names))
    
    # Analyze invoices using the obtained filenames
    analyze_invoices(file_names)

if __name__ == "__main__":
    main()
