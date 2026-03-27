from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_ollama import OllamaEmbeddings, ChatOllama
# from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings

# model_03 = ChatOllama(model="qwen3-vl:8b", temperature=0.3)
# model_0 = ChatOllama(model="qwen3-vl:8b", temperature=0)
# model = ChatOllama(model="qwen3-vl:8b")
# embeddings_model = OllamaEmbeddings(model="nomic-embed-text")

from dotenv import load_dotenv
import os

load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
os.environ["GOOGLE_API_KEY"] = google_api_key
os.environ["OPENAI_API_KEY"] = openai_api_key

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=1.0, 
    max_tokens=None,
    timeout=None,
    max_retries=2, 
)

model_03 = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3, 
    max_tokens=None,
    timeout=None,
    max_retries=2
)

model_0 = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.0, 
    max_tokens=None,
    timeout=None,
    max_retries=2
)

os.environ
embeddings_model = HuggingFaceEmbeddings(
    model_name="all-mpnet-base-v2"  # very popular, small & fast
)