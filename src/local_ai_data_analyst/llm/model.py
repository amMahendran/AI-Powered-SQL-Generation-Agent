from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os

load_dotenv()

# model_name="qwen3:1.7b"
# model_provider="ollama"

model_name="gemini-3.5-flash-lite"
model_provider="google_genai"

llm=init_chat_model(
    model=model_name,
    model_provider=model_provider,
)

def ask_llm(prompt:str):
    response=llm.invoke(prompt)
    return response.content