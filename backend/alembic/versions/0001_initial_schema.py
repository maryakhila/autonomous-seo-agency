
"""Create initial database tables."""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    user_role = postgresql.ENUM(
        "SUPER_ADMIN", "STAFF", "CLIENT",
        name="userrole",
    )
    client_status = postgresql.ENUM(
        "ACTIVE", "ONBOARDING", "PAUSED", "COMPLETED",
        name="clientstatus",
    )
    lead_status = postgresql.ENUM(
        "NEW", "CONTACTED", "QUALIFIED", "PROPOSAL_SENT",
        "CONVERTED", "LOST",
        name="leadstatus",
    )
    task_status = postgresql.ENUM(
        "PENDING", "IN_PROGRESS", "REVIEW", "COMPLETED", "FAILED",
        name="taskstatus",
    )

    user_role.create(op.get_bind(), checkfirst=True)
    client_status.create(op.get_bind(), checkfirst=True)
    lead_status.create(op.get_bind(), checkfirst=True)
    task_status.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("full_name", sa.String(255), nullable=False),
        sa.Column("role", user_role, nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.create_index("ix_users_id", "users", ["id"])
    op.create_index("ix_users_email", "users", ["email"])

    op.create_table(
        "clients",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("company_name", sa.String(255), nullable=False),
        sa.Column("website", sa.String(500), nullable=True),
        sa.Column("status", client_status, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_clients_id", "clients", ["id"])
    op.create_index("ix_clients_user_id", "clients", ["user_id"])

    op.create_table(
        "leads",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("company_name", sa.String(255), nullable=True),
        sa.Column("website", sa.String(500), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("status", lead_status, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_leads_id", "leads", ["id"])
    op.create_index("ix_leads_email", "leads", ["email"])

    op.create_table(
        "agent_tasks",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("client_id", sa.Integer(), sa.ForeignKey("clients.id"), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("agent_name", sa.String(100), nullable=False),
        sa.Column("status", task_status, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_agent_tasks_id", "agent_tasks", ["id"])
    op.create_index("ix_agent_tasks_client_id", "agent_tasks", ["client_id"])

    op.create_table(
        "deliverables",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("client_id", sa.Integer(), sa.ForeignKey("clients.id"), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("deliverable_type", sa.String(100), nullable=False),
        sa.Column("content", sa.Text(), nullable=True),
        sa.Column("status", sa.String(50), nullable=False, server_default="draft"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_deliverables_id", "deliverables", ["id"])
    op.create_index("ix_deliverables_client_id", "deliverables", ["client_id"])


def downgrade() -> None:
    op.drop_table("deliverables")
    op.drop_table("agent_tasks")
    op.drop_table("leads")
    op.drop_table("clients")
    op.drop_table("users")

    for enum_name in (
        "taskstatus",
        "leadstatus",
        "clientstatus",
        "userrole",
    ):
        postgresql.ENUM(name=enum_name).drop(
            op.get_bind(),
            checkfirst=True,
        )
