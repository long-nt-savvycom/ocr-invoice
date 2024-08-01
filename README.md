# Invoice OCR Demo

This project is a Python-based application designed to process and analyze invoices stored in PDF format. It utilizes the Azure AI Form Recognizer for extracting structured data from the invoices.

## Project Structure# Install


## Prerequisites

- Python 3.x
- `pip` (Python package installer)

## Setup

1. **Clone the repository**:

    ```bash
    git clone <repository-url>
    cd my_project
    ```

2. **Create and activate a virtual environment**:

    - Using `venv` (recommended):

        ```bash
        python -m venv venv
        ```

    - Activate the virtual environment:

        - On **Windows**:
        
            ```bash
            .\venv\Scripts\activate
            ```

        - On **macOS/Linux**:

            ```bash
            source venv/bin/activate
            ```

3. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```


4. **After install dependencies**:
    ```bash
    pip freeze > requirements.txt
    ```


## Usage

To run the project, ensure you have activated the virtual environment and then execute your main script. For example:

```bash
python main.py
