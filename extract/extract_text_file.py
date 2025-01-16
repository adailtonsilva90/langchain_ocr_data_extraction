from langchain_openai import ChatOpenAI 
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain  # Using LLMChain as an alternative to RunnableSequence
#imports from pydantic for validation
#from pydantic import ValidationError
#from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv
import fitz  # PyMuPDF (does not require Poppler)
import easyocr  # Using EasyOCR for OCR to avoid installing Tesseract on the server
from PIL import Image
import io
import numpy as np
from models.doc_receipt_bank import generate_prompt_receipt_bank
from models.doc_cei_obra import generate_prompt_cei_obra
from classify.classify import classify_type_document


# Load environment variables from the .env file
load_dotenv()

# Function to extract text from PDF files (with OCR for image-based PDFs)
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
            
            # Use EasyOCR to perform OCR on the page image
            text += extract_text_from_image(img)
    return text


# Function to extract text from an image
def extract_text_from_image(image_path):

    # Check if the input is a string (file path) or a PIL image
    if isinstance(image_path, str):
        # If it's a file path, EasyOCR can process it directly
        img = image_path
    else:
        # If it's a PIL image, convert it to a numpy array
        img = np.array(image_path)
    
    # Initialize the EasyOCR reader
    reader = easyocr.Reader(['pt', 'en'])  # Supports multiple languages
    result = reader.readtext(img)
    
    text = ""
    for item in result:
        text += item[1] + "\n"  # Extract text from images
    return text

# Main function to handle different file types
def extract_text_from_file(file_path):
    # Check the file extension
    extension = file_path.lower().split('.')[-1]

    if extension == "pdf":
        return extract_text_from_pdf(file_path)
    
    elif extension in ["png", "jpeg", "jpg"]:
        return extract_text_from_image(file_path)
    
    else:
        raise ValueError("Unsupported file type!")


