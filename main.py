from dotenv import load_dotenv
import json
from services.classify import classify_type_document
from services.extract import extract_text_from_file, extract_data
from fastapi import APIRouter, UploadFile, HTTPException,FastAPI


app = FastAPI()
@app.post("/process")
async def process_document(file: UploadFile):
    try:    

        if not file.filename.endswith((".pdf", ".png", ".jpeg", ".jpg")):
            raise HTTPException(status_code=400, detail="Formato de arquivo não suportado.")
        
        document_text = await extract_text_from_file(file)
        if not document_text:
            raise HTTPException(status_code=400, detail="Não foi possível extrair texto do arquivo.")

        document_type = classify_type_document(document_text)
        if not document_type:
            raise HTTPException(status_code=400, detail="Não foi possível classificar o documento.")
        
        # Validate the document based on the classified type
        result = extract_data(document_type, document_text)  
        if not result:
            raise HTTPException(status_code=400, detail="Erro ao processar o documento.")        

        json_response = json.loads(result)
        return {"success": True, "data": json_response }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))