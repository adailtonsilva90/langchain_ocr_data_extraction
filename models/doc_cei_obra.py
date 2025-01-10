from langchain.chains import LLMChain  # Usando LLMChain, pois é uma alternativa ao RunnableSequence
from pydantic import BaseModel, Field

#Caso queira usar po pydantic
# class Documento(BaseModel):
#     razao_social: str =  Field(description="Nome oficial registrado para fins legais e fiscais.")
#     cnpj: str  = Field(description=
#                         "Cadastro Nacional da Pessoa Jurídica (CNPJ). "
#                         "Deve conter 14 dígitos e pode ser fornecido com ou sem formatação. "
#                         "Exemplos válidos: '12.345.678/0001-95' ou '12345678000195'.")
#     endereco: str = Field(description=
#                            "Endereço completo da empresa ou pessoa. "
#                             "Deve incluir rua, número, complemento (se houver), bairro, cidade, estado e CEP. "
#                             "Exemplo: 'Rua das Flores, 123, Apto 45, Bairro Centro, São Paulo, SP, 01234-567'.")

def gerar_prompt_cei_obra(document_text: str) -> str:

  prompt = """
  Você é um agente que extrai informações de documentos de CEI da Obra. 
  Extraia os seguintes campos formatando no encoding UTF-8:
  - Razão Social do cliente : "Nome oficial registrado para fins legais e fiscais."

  - CNPJ :"Cadastro Nacional da Pessoa Jurídica (CNPJ). "
          "Deve conter 14 dígitos e pode ser fornecido com ou sem formatação. "
          "Exemplos válidos: '12.345.678/0001-95' ou '12345678000195'."

  - Endereço :  "Endereço completo da empresa ou pessoa. "
                "Deve incluir rua, número, complemento (casa, apto, se houver), bairro, cidade, estado e CEP. "
                "Exemplo: 'Rua das Flores, Numero 123, Apto 45, Bairro Centro, São Paulo, SP, CEP: 01234-567'."


  Texto do documento:
  {document_text}

  Responda no formato JSON:
  {{
    "razao_social": "Preencha com a razão social extraída do documento",
    "cnpj": "Preencha com o cnpja extraído do documento",
    "endereco": "Preencha com o endereço extraído do documento
  }}
  """
  return prompt.strip()

