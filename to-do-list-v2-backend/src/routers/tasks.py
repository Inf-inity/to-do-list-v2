from fastapi import APIRouter, Request

from database import db, filter_by
from models import User, UserTask
from schemas.task import Task as Ta
from utils.auth import get_token, user_auth
from utils.exceptions import InvalidTask

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


@router.delete("/task/delete", dependencies=[user_auth])
async def delete_task(request: Request, task_id: int):
    user = await User.get_user_by_token(get_token(request))
    task = await db.get(UserTask, id=task_id)
    if not task:
        raise InvalidTask

    if task not in user.tasks or not user.admin:
        raise InvalidTask

    await task.remove()

    return True
