from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import os
from dotenv import load_dotenv
import fitz  # PyMuPDF (does not require Poppler)
from PIL import Image
import io
import tempfile
from fastapi import UploadFile
from langchain_openai import ChatOpenAI 
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain  # Using LLMChain as an alternative to RunnableSequence
import os
from dotenv import load_dotenv
import openai  # Necessary for interacting with the OpenAI API
import json
import re
from models.doc_receipt_bank import generate_prompt_receipt_bank
from models.doc_cei_obra import generate_prompt_cei_obra

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
    """
    Extrai texto usando o Azure OCR.
    """
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
def extract_text_from_pdf(file_path):
    text = ""

    # Open the PDF by file path
    with fitz.open(file_path) as doc:
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)

            # Convert the page to an image
            image = page.get_pixmap()
            image_bytes = image.tobytes("png")
            img = Image.open(io.BytesIO(image_bytes))

            # Save a temporary image for processing in Azure
            temp_image_path = f"temp_page_{page_num}.png"
            img.save(temp_image_path)

            # Use Azure OCR to extract text
            text += extract_text_with_azure(temp_image_path)

            # Remove the temporary file
            os.remove(temp_image_path)

        return text

# Main function to handle different file types
async def extract_text_from_file(file: UploadFile):
    """
    Processa diferentes tipos de arquivos para extrair texto.
    """
    # Criar um arquivo temporário para salvar o conteúdo
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.filename.split('.')[-1]}") as temp_file:
        temp_file.write(await file.read())
        temp_file_path = temp_file.name  # Caminho do arquivo salvo temporariamente

    try:
        # Identificar a extensão do arquivo
        extension = file.filename.lower().split('.')[-1]

        if extension == "pdf":
            # Processar PDF
            return extract_text_from_pdf(temp_file_path)
        elif extension in ["jpeg", "jpg", "png"]:
            # Processar imagem usando Azure OCR
            return extract_text_with_azure(temp_file_path)
        else:
            raise ValueError("Tipo de arquivo não suportado.")
    finally:
        # Remover o arquivo temporário após o processamento
        os.remove(temp_file_path)


# Retrieve the API Key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configure LangChain and Prompt
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)  # Changed to ChatOpenAI

def extract_data(document_type, document_text):
    try:
        match document_type:
            case "Comprovante Bancário":
                prompt_template = generate_prompt_receipt_bank(document_type, document_text)
                prompt = PromptTemplate(input_variables=["document_type","document_text"], template=prompt_template)
                
            case _:
                return {"success": False, "error": "Unknown or unsupported document type!"}        
        
        chain = LLMChain(llm=llm, prompt=prompt)  # Using LLMChain
        response = chain.run({"document_type": document_type, "document_text": document_text})
        match = re.search(r"\{.*?\}", response, re.DOTALL)
        if match:
            match = match.group(0)

        return match 
        
            
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})
