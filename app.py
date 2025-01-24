import os
import json
import streamlit as st
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
import fitz  # PyMuPDF

# Load environment variables
load_dotenv()

# Set up the endpoint and key
endpoint = os.environ["DOCUMENTINTELLIGENCE_ENDPOINT"]
key = os.environ["DOCUMENTINTELLIGENCE_API_KEY"]

# Initialize the client
document_intelligence_client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))

# Streamlit app
st.set_page_config(page_title="Document Analysis", page_icon="📄", layout="wide")
st.title("Azure Document Intelligence - Document Analysis 📄")

# Dropdown to select the type of model
model_type = st.selectbox("Select the type of model:", ["prebuilt-layout", "prebuilt-receipt", "prebuilt-creditCard"])

uploaded_file = st.file_uploader("Choose a document image or PDF...", type=["png", "jpg", "jpeg", "pdf"])

if uploaded_file is not None:
    file_extension = uploaded_file.name.split(".")[-1].lower()
    
    if file_extension in ["png", "jpg", "jpeg"]:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        show_preview = st.empty()
        show_preview.image(image, caption='Uploaded Document Image', use_column_width=True)
        
        with st.spinner("Analyzing document... ⏳"):
            uploaded_file.seek(0)  # Reset file pointer to the beginning
            poller = document_intelligence_client.begin_analyze_document(
                model_type, analyze_request=uploaded_file, locale="en-US", content_type="application/octet-stream"
            )
            analysis_result = poller.result()

        st.success("Analysis complete! ✅")
        # Annotate the image with extracted text
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()

        for document in analysis_result.documents:
            for field_name, field in document.fields.items():
                if field.bounding_regions:
                    for region in field.bounding_regions:
                        if region.polygon:
                            points = [(region.polygon[i], region.polygon[i + 1]) for i in range(0, len(region.polygon), 2)]
                            draw.polygon(points, outline="red", width=3)
                            draw.text((points[0][0], points[0][1]), field_name, fill="red", font=font)

        # Replace the preview image with the annotated image
        show_preview.image(image, caption='Annotated Document Image', use_column_width=True)
        
        st.json(analysis_result.as_dict())

    elif file_extension == "pdf":
        # Display the uploaded PDF
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            st.image(img, caption=f'Page {page_num + 1} of Uploaded PDF', use_column_width=True)

        with st.spinner("Analyzing document... ⏳"):
            uploaded_file.seek(0)  # Reset file pointer to the beginning
            poller = document_intelligence_client.begin_analyze_document(
                model_type, analyze_request=uploaded_file, locale="en-US", content_type="application/octet-stream"
            )
            analysis_result = poller.result()

        st.success("Analysis complete! ✅")
        st.json(analysis_result.as_dict())

    if analysis_result.documents:
        for idx, document in enumerate(analysis_result.documents):
            st.write(f"--------Analysis of document #{idx + 1}--------")
            st.write(f"Document type: {document.doc_type if document.doc_type else 'N/A'}")
            if document.fields:
                merchant_name = document.fields.get("MerchantName")
                if merchant_name:
                    st.write(
                        f"Merchant Name: {merchant_name.value} has confidence: "
                        f"{merchant_name.confidence}"
                    )
                transaction_date = document.fields.get("TransactionDate")
                if transaction_date:
                    st.write(
                        f"Transaction Date: {transaction_date.value} has confidence: "
                        f"{transaction_date.confidence}"
                    )
                items = document.fields.get("Items")
                if items:
                    st.write("Document items:")
                    for idx, item in enumerate(items.value):
                        st.write(f"...Item #{idx + 1}")
                        item_description = item.value.get("Description")
                        if item_description:
                            st.write(
                                f"......Item Description: {item_description.value} has confidence: "
                                f"{item_description.confidence}"
                            )
                        item_quantity = item.value.get("Quantity")
                        if item_quantity:
                            st.write(
                                f"......Item Quantity: {item_quantity.value} has confidence: "
                                f"{item_quantity.confidence}"
                            )
                        item_total_price = item.value.get("TotalPrice")
                        if item_total_price:
                            st.write(
                                f"......Total Item Price: {item_total_price.value} has confidence: "
                                f"{item_total_price.confidence}"
                            )
                subtotal = document.fields.get("Subtotal")
                if subtotal:
                    st.write(
                        f"Subtotal: {subtotal.value} has confidence: {subtotal.confidence}"
                    )
                tax = document.fields.get("TotalTax")
                if tax:
                    st.write(f"Total tax: {tax.value} has confidence: {tax.confidence}")
                tip = document.fields.get("Tip")
                if tip:
                    st.write(f"Tip: {tip.value} has confidence: {tip.confidence}")
                total = document.fields.get("Total")
                if total:
                    st.write(f"Total: {total.value} has confidence: {total.confidence}")
            st.write("--------------------------------------")