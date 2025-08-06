import asyncio
import json
import os
from dotenv import load_dotenv
import websockets
import logging
from concurrent.futures import ThreadPoolExecutor

load_dotenv()
CHAT_ID = 1
TOKEN = os.getenv("TOKEN")
WS_URL = f"ws://localhost:8000/ws/chat/{CHAT_ID}"
executor = ThreadPoolExecutor()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def payload_send_message(message_text: str) -> dict:
    return {
        "action": "send_message",
        "payload": {"message_text": message_text}
    }


def payload_translate(message_text: str, language: str) -> dict:
    return {
        "action": "translate",
        "payload": {
            "message_text": message_text,
            "language": language
        }
    }


commands = {}


def register(command_name):
    def wrapper(func):
        commands[command_name] = func
        return func

    return wrapper


@register("1")
async def handle_send(websocket, loop):
    message_text = await loop.run_in_executor(executor, input, "Enter your message: ")
    payload = payload_send_message(message_text)
    await websocket.send(json.dumps(payload))


@register("2")
async def handle_translate(websocket, loop):
    message_text = await loop.run_in_executor(executor, input, "Text to translate: ")
    language = await loop.run_in_executor(executor, input, "Target language code: ")
    payload = payload_translate(message_text, language)
    await websocket.send(json.dumps(payload))


@register("3")
async def handle_exit(websocket, *_):
    logger.info("Exiting...")
    await websocket.close()


async def sender(websocket, loop):
    while True:
        choice = await loop.run_in_executor(executor, input, "\n[1] Send  [2] Translate  [3] Exit\nChoose: ")

        handler = commands.get(choice)
        if handler:
            await handler(websocket, loop)
            if choice == "3":
                break
        else:
            logger.warning("Invalid choice. Try again.")


async def receiver(websocket):
    while True:
        try:
            message = await websocket.recv()
            logger.info(f"Received: {message}")
        except websockets.exceptions.ConnectionClosed:
            logger.warning("Connection closed by server.")
            break


async def websocket_client():
    headers = {"Authorization": f"Bearer {TOKEN}"}

    async with websockets.connect(WS_URL, additional_headers=headers) as websocket:
        logger.info("Connected to WebSocket")
        loop = asyncio.get_event_loop()
        await asyncio.gather(sender(websocket, loop), receiver(websocket))


"""Run the client after FastAPI server is running"""
if __name__ == "__main__":
    asyncio.run(websocket_client())
