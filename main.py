from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"hello": "world"}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app")
