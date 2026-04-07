import os
from dotenv import load_dotenv, dotenv_values
from langchain_openai import ChatOpenAI

load_dotenv(override=True)

llm = ChatOpenAI(model="gpt-4o-mini")
print(llm.invoke("Xin chào?").content)