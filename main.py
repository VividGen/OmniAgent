import uvicorn
from dotenv import load_dotenv
from loguru import logger

if __name__ == "__main__":
    load_dotenv()
    logger.info("Starting OmniAgent")
    uvicorn.run("omniagent.app:app", host="0.0.0.0", reload=False, port=8000)
