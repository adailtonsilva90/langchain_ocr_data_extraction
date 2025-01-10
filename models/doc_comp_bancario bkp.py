from pydantic import BaseModel, Field
import json

class Documento(BaseModel):
    razao_social: str = Field(description="Razão social da empresa. Nome oficial registrado para fins legais e fiscais.")
    agencia: str = Field(description="Numerical representation of the client's bank branch")
    conta: str = Field(description="Numerical representation of the client's bank account")
    nome_banco: str = Field(description="Name of the banking institution")

def gerar_prompt(document_text: str) -> str:
    
    prompt = """
    Você é um agente que extrai informações de comprovantes bancários escaneados.
    Extraia os seguintes campos:
    - Razão social
    - agencia
    - conta

    Texto do documento:
    {document_text}

    Responda no formato JSON:
    {{
        "razao_social": "Preencha com a razão social extraída do documento",
        "agencia": "Preencha com o número da agência extraída do documento",
        "conta": "Preencha com o número da conta extraída do documento",
        "nome_banco": "Preencha com o nome do banco extraído do documento"
    }}
    """
    return prompt.strip()