import uvicorn

if __name__ == "__main__":
    uvicorn.run("omniagent.app:app", host="127.0.0.1", reload=True, port=8001)
