
import enum
from datetime import datetime

from sqlalchemy import String, Integer, DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ClientStatus(str, enum.Enum):
    ACTIVE = "active"
    ONBOARDING = "onboarding"
    PAUSED = "paused"
    COMPLETED = "completed"


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    company_name: Mapped[str] = mapped_column(
        String(255), nullable=False
    )

    website: Mapped[str | None] = mapped_column(
        String(500), nullable=True
    )

    status: Mapped[ClientStatus] = mapped_column(
        Enum(ClientStatus),
        default=ClientStatus.ONBOARDING,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
