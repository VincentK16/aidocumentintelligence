# Getting Started with Azure Document Intelligence Streamlit App

This guide will help you set up and run the Azure Document Intelligence Streamlit app in your local environment.

## Prerequisites

Before you begin, ensure you have the following installed:

- [Python 3.7+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)
- [Azure Account](https://azure.microsoft.com/en-us/free/)
- [Azure Cognitive Services](https://azure.microsoft.com/en-us/services/cognitive-services/)

## Setup

### 1. Clone the Repository

Clone the repository to your local machine using the following command:

```sh
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```
### 2. Create a Virtual Environment
Create and activate a virtual environment to manage dependencies:

```sh
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```
### 3. Install Dependencies
Install the required Python packages using pip:

```sh
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a .env file in the root directory of the project and add your Azure Document Intelligence endpoint and API key:
```sh
DOCUMENTINTELLIGENCE_ENDPOINT="https://your-endpoint.cognitiveservices.azure.com/"
DOCUMENTINTELLIGENCE_API_KEY="your-api-key"
```
Replace your-endpoint and your-api-key with your actual Azure Document Intelligence endpoint and API key.

### 5. Run the Streamlit App
Start the Streamlit app using the following command:
```sh
streamlit run app.py
```
This will start the Streamlit server and open the app in your default web browser.

## Usage
- Select Model Type: Choose the type of model you want to use for document analysis (e.g., prebuilt-layout, prebuilt-invoice, prebuilt-creditCard).
- Upload Document: Upload a document image or PDF file for analysis.
- View Results: The app will display the uploaded document, perform the analysis, and show the annotated document with extracted text and bounding boxes.
