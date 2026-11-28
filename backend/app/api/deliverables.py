
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.core.database import get_db
from app.models.deliverable import Deliverable


router = APIRouter(
    prefix="/deliverables",
    tags=["SEO Deliverables"],
)


class DeliverableCreate(BaseModel):
    client_id: int
    title: str
    deliverable_type: str
    content: str | None = None


@router.post("/")
async def create_deliverable(
    data: DeliverableCreate,
    db: AsyncSession = Depends(get_db),
):
    item = Deliverable(
        client_id=data.client_id,
        title=data.title,
        deliverable_type=data.deliverable_type,
        content=data.content,
    )

    db.add(item)
    await db.commit()
    await db.refresh(item)

    return {
        "id": item.id,
        "title": item.title,
        "type": item.deliverable_type,
        "status": item.status,
    }


@router.get("/")
async def list_deliverables(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Deliverable))
    items = result.scalars().all()

    return [
        {
            "id": item.id,
            "client_id": item.client_id,
            "title": item.title,
            "type": item.deliverable_type,
            "status": item.status,
        }
        for item in items
    ]


@router.get("/{deliverable_id}")
async def get_deliverable(
    deliverable_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Deliverable).where(
            Deliverable.id == deliverable_id
        )
    )
    item = result.scalar_one_or_none()

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Deliverable not found",
        )

    return {
        "id": item.id,
        "client_id": item.client_id,
        "title": item.title,
        "type": item.deliverable_type,
        "content": item.content,
        "status": item.status,
    }
