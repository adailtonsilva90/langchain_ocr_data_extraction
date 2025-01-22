from langchain_openai import ChatOpenAI 
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain  # Using LLMChain as an alternative to RunnableSequence
import os
from dotenv import load_dotenv
import openai  # Necessary for interacting with the OpenAI API

# Load environment variables from the .env file
load_dotenv()

# Retrieve the API Key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

prompt_template = """
Você recebe um texto de um documento e precisa classificá-lo em um dos seguintes tipos:

1. Comprovante Bancário
2. CEI da Obra

Texto do documento:
{document_text}

Responda com apenas o tipo do documento. Exemplo: "Comprovante Bancário" ou "CEI da Obra".
"""
# Configure LangChain and Prompt
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)  # Changed to ChatOpenAI
prompt = PromptTemplate(input_variables=["document_text"], template=prompt_template)
chain = LLMChain(llm=llm, prompt=prompt)  # Using LLMChain


# Function to classify the document type
def classify_type_document(document_text):
    # Use LangChain to obtain the classification
    document_type = chain.run({"document_text": document_text})
    return document_type.strip()
