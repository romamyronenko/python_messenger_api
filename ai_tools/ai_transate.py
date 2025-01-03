import os

from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langserve import add_routes

from app.main import app
from app.models import Message

load_dotenv()
OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
model = ChatOpenAI(temperature=0.9, openai_api_key=OPEN_AI_API_KEY)

system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', '{text}')
])

parser = StrOutputParser()
chain = prompt_template | model | parser
add_routes(
    app,
    chain,
    path="/chain"
)


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





