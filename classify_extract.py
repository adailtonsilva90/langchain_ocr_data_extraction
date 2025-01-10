from langchain_openai import ChatOpenAI 
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain  # Usando LLMChain, pois é uma alternativa ao RunnableSequence
from pydantic import ValidationError
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import fitz  # PyMuPDF (não precisa do Poppler)
import openai  # Necessário para interação com a OpenAI API
import easyocr  # Usando EasyOCR para OCR para não precisar instalar o tesseract no servidor
from PIL import Image
import io
import numpy as np
import json
from models.doc_comp_bancario import gerar_prompt_comp_banco
from models.doc_cei_obra import gerar_prompt_cei_obra


# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém a API Key da variável de ambiente
openai.api_key = os.getenv("OPENAI_API_KEY")

prompt_template = """
Você recebe um texto de um documento e precisa classificá-lo em um dos seguintes tipos:

1. Comprovante Bancário
2. CEI da Obra

Texto do documento:
{document_text}

Responda com apenas o tipo do documento. Exemplo: "Comprovante Bancário" ou "CEI da Obra".
"""
# Passo 1: Configurar LangChain e Prompt
llm = ChatOpenAI(model="gpt-4", temperature=0)  # Alterado para ChatOpenAI
prompt = PromptTemplate(input_variables=["document_text"], template=prompt_template)
chain = LLMChain(llm=llm, prompt=prompt)  # Usando LLMChain

# Função para extrair texto de arquivos PDF (com OCR se for imagem)
def extrair_texto_pdf(caminho_pdf):
    texto = ""
    # Abre o arquivo PDF com PyMuPDF
    with fitz.open(caminho_pdf) as doc:
        for pagina_num in range(doc.page_count):
            pagina = doc.load_page(pagina_num)

            # Converte a página em imagem
            imagem = pagina.get_pixmap()
            imagem_bytes = imagem.tobytes("png")
            img = Image.open(io.BytesIO(imagem_bytes))
            
            # Usando EasyOCR para fazer OCR na imagem da página
            texto += extrair_texto_imagem(img)
    return texto


def extrair_texto_imagem(caminho_imagem):

    # Verifica se a entrada é uma string (caminho de arquivo) ou imagem PIL
    if isinstance(caminho_imagem, str):
        # Se for caminho de arquivo, o EasyOCR pode processar diretamente
        img = caminho_imagem
    else:
        # Se for imagem PIL, converte para numpy array
        img = np.array(caminho_imagem)
    
    # Inicializa o leitor do EasyOCR
    reader = easyocr.Reader(['pt', 'en'])  # Suporta múltiplos idiomas
    resultado = reader.readtext(img)
    
    texto = ""
    for item in resultado:
        texto += item[1] + "\n"  # Extrai o texto das imagens
    
    return texto

# Função principal para lidar com diferentes tipos de arquivo
def extrair_texto_de_arquivo(caminho_arquivo):   

    # Verifica a extensão do arquivo
    extensao = caminho_arquivo.lower().split('.')[-1]

    if extensao == "pdf":
        return extrair_texto_pdf(caminho_arquivo)
    
    elif extensao in ["png", "jpeg", "jpg"]:
        return extrair_texto_imagem(caminho_arquivo)
    
    else:
        raise ValueError("Tipo de arquivo não suportado!")
    


# Passo 2: Função para classificar o tipo de documento
def classificar_tipo_documento(document_text):
    # Usa o LangChain para obter a classificação
    tipo_documento = chain.run({"document_text": document_text})
    return tipo_documento.strip()


def extrair_dados(tipo_documento, document_text):
    try:
        if tipo_documento == "Comprovante Bancário":     
            prompt_template = gerar_prompt_comp_banco(document_text)     
            prompt = PromptTemplate(input_variables=["document_text"], template=prompt_template)
            

        elif tipo_documento == "CEI da Obra":
            prompt_template = gerar_prompt_cei_obra(document_text)     
            prompt = PromptTemplate(input_variables=["document_text"], template=prompt_template)

        else:
            return {"success": False, "error": "Tipo de documento desconhecido"}        
        
        chain = LLMChain(llm=llm, prompt=prompt)  # Usando LLMChain
        response = chain.run({"document_text": document_text})
        return response
        
            
    except Exception  as e:
        return json.dumps({"success": False, "error": str(e)})



caminho_arquivo = os.getenv("FILE_PATH") # No caso de ter o caminho absoluto do arquivo altere para o caminho correto do seu arquivo
document_text = extrair_texto_de_arquivo(caminho_arquivo)
tipo_documento = classificar_tipo_documento(document_text)

resultado = extrair_dados(tipo_documento, document_text)  # Valida o documento conforme o tipo classificado
if resultado:
    print("\n\n",resultado)


