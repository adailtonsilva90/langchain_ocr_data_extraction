from pydantic import BaseModel, Field
import json

#Caso queira usar po pydantic
# class Documento(BaseModel):
#     razao_social: str = Field(description="Razão social da empresa. Nome oficial registrado para fins legais e fiscais.")
#     agencia: str = Field(description="Numerical representation of the client's bank branch")
#     conta: str = Field(description="Numerical representation of the client's bank account")
#     nome_banco: str = Field(description="Name of the banking institution")

def gerar_prompt_comp_banco(document_text: str) -> str:
    
    prompt = """
    Você é um agente que extrai informações de comprovantes bancários escaneados.
    Extraia os seguintes campos formatando no encoding UTF-8:
    - Razão social :  Nome oficial registrado para fins legais e fiscais.
    - agência : Código numérico que identifica a agência bancária onde a conta do cliente está registrada
    - conta: Número único que identifica a conta do cliente em uma instituição financeira.
    - Nome do Banco: Nome da instituição financeira onde a conta bancária do cliente está registrada

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