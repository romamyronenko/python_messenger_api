import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.models import Message

load_dotenv()
OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
model = ChatOpenAI(temperature=0.9, openai_api_key=OPEN_AI_API_KEY)

SYSTEM_TEMPLATE = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages([
    ('system', SYSTEM_TEMPLATE),
    ('user', '{text}')
])

parser = StrOutputParser()
chain = prompt_template | model | parser


def translate(message: Message, language: str = "en"):
    if not message.message_text:
        raise ValueError("Message text cannot be empty.")
    try:
        translation = chain.invoke({
            "text": message.message_text,
            "language": language,
        })
        return translation
    except Exception as e:
        raise RuntimeError(f"Translation failed: {str(e)}")
