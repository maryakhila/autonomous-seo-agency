
import enum
from datetime import datetime

from sqlalchemy import String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    COMPLETED = "completed"
    FAILED = "failed"


class AgentTask(Base):
    __tablename__ = "agent_tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    client_id: Mapped[int] = mapped_column(
        ForeignKey("clients.id"),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(255), nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )

    agent_name: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus),
        default=TaskStatus.PENDING,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
