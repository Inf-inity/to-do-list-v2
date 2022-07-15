from fastapi import APIRouter, Request

from database import db, filter_by
from models import User, UserTask
from schemas.task import Task as Ta
from utils.auth import get_token, user_auth


router = APIRouter(tags=["/tasks"])


@router.post("/task/new", dependencies=[user_auth])
async def new_task(request: Request, task: Ta):
    user = await User.get_user_by_token(get_token(request))
    task_obj = await UserTask.create(task.title, task.description, task.end, task.priority, user)
    return task_obj.serialize


@router.get("/task/all", dependencies=[user_auth])
async def all_tasks(request: Request):
    user = await User.get_user_by_token(get_token(request))
    tasks = await db.all(filter_by(UserTask, creator_id=user.id))
    return tasks
