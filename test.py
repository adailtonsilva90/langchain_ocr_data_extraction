
import openai
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém a API Key da variável de ambiente
openai.api_key = os.getenv("OPENAI_API_KEY")


# Teste uma requisição simples usando a nova interface de chat
#try:
response = openai.chat.completions.create(
    model="gpt-3.5-turbo",  # Pode ser "gpt-3.5-turbo"
    messages=[
        {"role": "system", "content": "Você é um assistente inteligente."},
        {"role": "user", "content": "Qual é a capital da França?"}
    ]
)

print("Resposta do modelo:", response.choices[0].message.content)


#except openai.error.OpenAIError as e:
#  print(f"Erro na API: {e}")
  