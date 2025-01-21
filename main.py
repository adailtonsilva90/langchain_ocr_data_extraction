from langchain_openai import ChatOpenAI 
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain  # Using LLMChain as an alternative to RunnableSequence
import os
from dotenv import load_dotenv
import openai  # Necessary for interacting with the OpenAI API
import json
from models.doc_receipt_bank import generate_prompt_receipt_bank
from models.doc_cei_obra import generate_prompt_cei_obra
from classify.classify import classify_type_document
from extract.extract_text_file import extract_text_from_file
import re
from fastapi import APIRouter, UploadFile, HTTPException,FastAPI

# Load environment variables from the .env file
load_dotenv()

# Retrieve the API Key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configure LangChain and Prompt
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)  # Changed to ChatOpenAI

def extract_data(document_type, document_text):
    try:
        match document_type:
            case "Comprovante Bancário":
                prompt_template = generate_prompt_receipt_bank(document_text)
                prompt = PromptTemplate(input_variables=["document_text"], template=prompt_template)
                
            case "CEI da Obra":
                prompt_template = generate_prompt_cei_obra(document_text)
                prompt = PromptTemplate(input_variables=["document_text"], template=prompt_template)
                
            case _:
                return {"success": False, "error": "Unknown or unsupported document type!"}        
        
        chain = LLMChain(llm=llm, prompt=prompt)  # Using LLMChain
        response = chain.run({"document_text": document_text})
        match = re.search(r"\{.*?\}", response, re.DOTALL)
        if match:
            match = match.group(0)

        return match 
        
            
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})

app = FastAPI()
@app.post("/process")
async def process_document(file: UploadFile):
    try:    
        #Validar extensão do arquivo
        if not file.filename.endswith((".pdf", ".png", ".jpeg", ".jpg")):
            raise HTTPException(status_code=400, detail="Formato de arquivo não suportado.")
        
        
        #print(file)
        document_text = await extract_text_from_file(file)
        if not document_text:
            raise HTTPException(status_code=400, detail="Não foi possível extrair texto do arquivo.")

        document_type = classify_type_document(document_text)
        if not document_type:
            raise HTTPException(status_code=400, detail="Não foi possível classificar o documento.")
        
        result = extract_data(document_type, document_text)  # Validate the document based on the classified type
        if not result:
            raise HTTPException(status_code=400, detail="Erro ao processar o documento.")
        

        json_response = json.loads(result)
        return {"success": True, "data": json_response }
        
        # print(file)
        # return {"success": True, "data": file}
        # if result:
        #     print("\n\n", result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))