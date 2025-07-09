import asyncio
import json
import websockets
from concurrent.futures import ThreadPoolExecutor

CHAT_ID = 1
TOKEN = "your-jwt-token-here"
WS_URL = f"ws://localhost:8000/ws/chat/{CHAT_ID}"


async def websocket_client():
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }

    async with websockets.connect(WS_URL, additional_headers=headers) as websocket:
        print("Connected to WebSocket")

        loop = asyncio.get_event_loop()
        executor = ThreadPoolExecutor()

        async def sender():
            while True:
                choice = await loop.run_in_executor(executor, input, "\n[1] Send  [2] Translate  [3] Exit\nChoose: ")

                if choice == "1":
                    message_text = await loop.run_in_executor(executor, input, "Enter your message: ")
                    payload = {
                        "action": "send_message",
                        "payload": {
                            "message_text": message_text
                        }
                    }
                    await websocket.send(json.dumps(payload))

                elif choice == "2":
                    message_text = await loop.run_in_executor(executor, input, "Text to translate: ")
                    language = await loop.run_in_executor(executor, input, "Target language code: ")
                    payload = {
                        "action": "translate",
                        "payload": {
                            "message_text": message_text,
                            "language": language
                        }
                    }
                    await websocket.send(json.dumps(payload))

                elif choice == "3":
                    print("Exiting...")
                    await websocket.close()
                    break

        async def receiver():
            while True:
                try:
                    message = await websocket.recv()
                    print(f"\nReceived: {message}")
                except websockets.exceptions.ConnectionClosed:
                    print("Connection closed by server.")
                    break

        await asyncio.gather(sender(), receiver())


if __name__ == "__main__":
    asyncio.run(websocket_client())
