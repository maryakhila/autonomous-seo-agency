
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, ConfigDict

from app.core.database import get_db
from app.models.client import Client, ClientStatus


router = APIRouter(prefix="/clients", tags=["Clients"])


class ClientCreate(BaseModel):
    user_id: int
    company_name: str
    website: str | None = None


class ClientResponse(BaseModel):
    id: int
    user_id: int
    company_name: str
    website: str | None
    status: ClientStatus

    model_config = ConfigDict(from_attributes=True)


@router.post("/", response_model=ClientResponse)
async def create_client(
    data: ClientCreate,
    db: AsyncSession = Depends(get_db),
):
    client = Client(
        user_id=data.user_id,
        company_name=data.company_name,
        website=data.website,
    )

    db.add(client)
    await db.commit()
    await db.refresh(client)

    return client


@router.get("/", response_model=list[ClientResponse])
async def list_clients(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Client))
    return result.scalars().all()


@router.get("/{client_id}", response_model=ClientResponse)
async def get_client(
    client_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Client).where(Client.id == client_id)
    )
    client = result.scalar_one_or_none()

    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")

    return client
