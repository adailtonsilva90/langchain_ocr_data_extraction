from langchain.chains import LLMChain  # Usando LLMChain, pois é uma alternativa ao RunnableSequence
from pydantic import BaseModel, Field

#Caso queira usar do pydantic
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

def generate_prompt_cei_obra(document_text: str) -> str:

  prompt = """
  Você é um agente que extrai informações de documentos de CEI da Obra. 
  Extraia os seguintes campos formatando no encoding UTF-8:
  - Razão Social do cliente : "Nome oficial registrado para fins legais e fiscais."

  - CNPJ :"Cadastro Nacional da Pessoa Jurídica (CNPJ). "
          "Deve conter 14 dígitos numéricos e pode ser fornecido com ou sem formatação. "
          "Exemplos válidos: '12.345.678/0001-95' ou '12345678000195'."

  - Endereço :  "Endereço completo da empresa ou pessoa. "
                "Deve incluir: 
                  Rua: Nome da via pública onde o imóvel está localizado. Pode incluir avenidas, ruas, travessas, praças, etc. Exemplos: "Avenida Paulista", "Rua das Flores".
                  Número: Número do imóvel na rua especificada. Pode ser numérico ou alfanumérico. Exemplos: "123", "45A".
                  Complemento: Informação adicional que ajuda a identificar o imóvel. Pode incluir detalhes como "Apartamento 302", "Casa 1", "Bloco B". Caso não haja complemento, deve ser informado como vazio.
                  Bairro: Subdivisão geográfica ou administrativa da cidade onde o imóvel está localizado. Exemplos: "Centro", "Jardim das Palmeiras".
                  Cidade: Nome do município onde o imóvel está localizado. Exemplos: "São Paulo", "Rio de Janeiro".
                  Estado: Unidade federativa (UF) onde o imóvel está localizado. Deve ser informado no formato abreviado de duas letras. Exemplos: "SP" para São Paulo, "RJ" para Rio de Janeiro.
                  CEP: Código postal usado para identificar a localização exata do imóvel. Deve conter oito dígitos no formato "12345-678".
                "Exemplo: 'Rua das Flores, 123, Apto 45, Bairro Centro, São Paulo, SP, CEP: 01234-567'."


  Texto do documento:
  {document_text}

  Responda apenas no formato o JSON:
  {{
    "razao_social": "Preencha com a razão social extraída do documento",
    "cnpj": "Preencha com o cnpja extraído do documento",
    "endereco": "Preencha com o endereço extraído do documento
  }}

  Caso não encontre o dado retorne "Não foi possível localizar este campo"
  """
  return prompt.strip()

