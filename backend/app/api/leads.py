
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.core.database import get_db
from app.models.agent_task import AgentTask, TaskStatus


router = APIRouter(prefix="/tasks", tags=["Agent Tasks"])


class TaskCreate(BaseModel):
    client_id: int
    title: str
    description: str | None = None
    agent_name: str


@router.post("/")
async def create_task(
    data: TaskCreate,
    db: AsyncSession = Depends(get_db),
):
    task = AgentTask(
        client_id=data.client_id,
        title=data.title,
        description=data.description,
        agent_name=data.agent_name,
    )

    db.add(task)
    await db.commit()
    await db.refresh(task)

    return {
        "id": task.id,
        "title": task.title,
        "agent_name": task.agent_name,
        "status": task.status.value,
    }


@router.get("/")
async def list_tasks(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(AgentTask))
    tasks = result.scalars().all()

    return [
        {
            "id": task.id,
            "client_id": task.client_id,
            "title": task.title,
            "agent_name": task.agent_name,
            "status": task.status.value,
        }
        for task in tasks
    ]


@router.patch("/{task_id}/status")
async def update_task_status(
    task_id: int,
    status: TaskStatus,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(AgentTask).where(AgentTask.id == task_id)
    )
    task = result.scalar_one_or_none()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    task.status = status
    await db.commit()

    return {
        "message": "Task status updated",
        "task_id": task.id,
        "status": task.status.value,
    }
