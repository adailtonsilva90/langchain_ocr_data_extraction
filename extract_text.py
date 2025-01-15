import os
import easyocr
import fitz  # PyMuPDF
from PIL import Image
import io
import numpy as np
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

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

# Exemplo de uso
caminho_arquivo = os.getenv("FILE_PATH") # No caso de ter o caminho absoluto do arquivo altere para o caminho correto do seu arquivo
texto_extraido = extrair_texto_de_arquivo(caminho_arquivo)
print("Texto extraído:", texto_extraido)
