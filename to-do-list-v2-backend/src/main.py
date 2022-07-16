import uvicorn

from utils.environment import HOST, PORT
from utils.logger import get_logger


logger = get_logger(__name__)


if __name__ == "__main__":
    uvicorn.run("to-do-list-v2-backend:to-do-list-v2-backend", host=HOST, port=PORT, reload=True, debug=True)
