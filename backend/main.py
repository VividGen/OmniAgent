import uvicorn

if __name__ == "__main__":
    uvicorn.run("omniagent.app:app", host="0.0.0.0", reload=True, port=8001)
