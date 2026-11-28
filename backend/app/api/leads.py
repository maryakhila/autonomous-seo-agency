
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.core.database import get_db
from app.models.lead import Lead, LeadStatus


router = APIRouter(prefix="/leads", tags=["Leads"])


class LeadCreate(BaseModel):
    name: str
    email: str
    company_name: str | None = None
    website: str | None = None
    notes: str | None = None


@router.post("/")
async def create_lead(
    data: LeadCreate,
    db: AsyncSession = Depends(get_db),
):
    lead = Lead(
        name=data.name,
        email=data.email,
        company_name=data.company_name,
        website=data.website,
        notes=data.notes,
    )

    db.add(lead)
    await db.commit()
    await db.refresh(lead)

    return {
        "id": lead.id,
        "name": lead.name,
        "email": lead.email,
        "status": lead.status.value,
    }


@router.get("/")
async def list_leads(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Lead))
    leads = result.scalars().all()

    return [
        {
            "id": lead.id,
            "name": lead.name,
            "email": lead.email,
            "company_name": lead.company_name,
            "status": lead.status.value,
        }
        for lead in leads
    ]
