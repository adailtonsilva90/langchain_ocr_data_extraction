from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import os
from dotenv import load_dotenv
import fitz  # PyMuPDF (does not require Poppler)
from PIL import Image
import io

# Load environment variables from the .env file
load_dotenv()

# Azure credentials
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
AZURE_API_KEY = os.getenv("AZURE_API_KEY")

# Initialize Azure Form Recognizer client
document_analysis_client = DocumentAnalysisClient(
    endpoint=AZURE_ENDPOINT,
    credential=AzureKeyCredential(AZURE_API_KEY)
)

# Function to extract text from a file using Azure Form Recognizer
def extract_text_with_azure(file_path):
    with open(file_path, "rb") as file_stream:
        poller = document_analysis_client.begin_analyze_document(
            "prebuilt-read", document=file_stream
        )
        result = poller.result()
    
    text = ""
    for page in result.pages:
        for line in page.lines:
            text += line.content + "\n"
    return text

# Function to extract text from PDF files
def extract_text_from_pdf(pdf_path):
    text = ""
    # Open the PDF file using PyMuPDF
    with fitz.open(pdf_path) as doc:
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)

            # Convert the page to an image
            image = page.get_pixmap()
            image_bytes = image.tobytes("png")
            img = Image.open(io.BytesIO(image_bytes))

            # Save the image temporarily for Azure processing
            temp_image_path = f"temp_page_{page_num}.png"
            img.save(temp_image_path)
            
            # Use Azure Form Recognizer to perform OCR on the page image
            text += extract_text_with_azure(temp_image_path)
            
            # Remove the temporary file
            os.remove(temp_image_path)
    return text

# Main function to handle different file types
def extract_text_from_file(file_path):
    # Check the file extension
    extension = file_path.lower().split('.')[-1]

    if extension == "pdf":
        return extract_text_from_pdf(file_path)
    
    elif extension in ["png", "jpeg", "jpg"]:
        return extract_text_with_azure(file_path)
    
    else:
        raise ValueError("Unsupported file type!")