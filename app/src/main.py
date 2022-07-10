import uvicorn

from utils.environment import HOST, PORT
from utils.logger import get_logger


logger = get_logger(__name__)


if __name__ == "__main__":
    uvicorn.run("app:app", host=HOST, port=PORT, reload=True, debug=True)
