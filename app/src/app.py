from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import db, db_context
from models.user import User
from routers import ROUTERS
from utils.logger import get_logger
from utils.middleware import HTTPMiddleware


logger = get_logger(__name__)

app = FastAPI(title="To-do-list-v2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(HTTPMiddleware)


@app.on_event("startup")
async def on_startup() -> None:
    await db.create_tables()
    logger.debug("Created database tables")

    async with db_context():
        await User.init_admin()

    for router in ROUTERS:
        app.include_router(router)
        logger.info(f"Loaded {router.tags} router")
