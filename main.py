from langchain_openai import ChatOpenAI 
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain  # Using LLMChain as an alternative to RunnableSequence
#imports from pydantic for validation
#from pydantic import ValidationError
#from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv
import openai  # Necessary for interacting with the OpenAI API
import json
from models.doc_receipt_bank import generate_prompt_receipt_bank
from models.doc_cei_obra import generate_prompt_cei_obra
from classify.classify import classify_type_document
from extract.extract_text_file import extract_text_from_file

# Load environment variables from the .env file
load_dotenv()

# Retrieve the API Key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configure LangChain and Prompt
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)  # Changed to ChatOpenAI

def extract_data(document_type, document_text):
    try:
        if document_type == "Comprovante Bancário":     
            prompt_template = generate_prompt_receipt_bank(document_text)     
            prompt = PromptTemplate(input_variables=["document_text"], template=prompt_template)
            

        elif document_type == "CEI da Obra":
            prompt_template = generate_prompt_cei_obra(document_text)     
            prompt = PromptTemplate(input_variables=["document_text"], template=prompt_template)

        else:
            return {"success": False, "error": "Unknown or unsupported document type!"}        
        
        chain = LLMChain(llm=llm, prompt=prompt)  # Using LLMChain
        response = chain.run({"document_text": document_text})
        return response
        
            
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})


file_path = os.getenv("FILE_PATH")  # If using an absolute file path, replace it with the correct path to your file
document_text = extract_text_from_file(file_path)
document_type = classify_type_document(document_text)

result = extract_data(document_type, document_text)  # Validate the document based on the classified type
if result:
    print("\n\n", result)
