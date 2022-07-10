import uvicorn

from utils.logger import get_logger


logger = get_logger(__name__)


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True, debug=True)
