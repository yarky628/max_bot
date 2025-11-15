import sqlalchemy as sa
from .database import metadata

users = sa.Table(
    "users",
    metadata,
    sa.Column("id", sa.String, primary_key=True),
    sa.Column("pseudo_name", sa.String, nullable=True),
    sa.Column("phone_encrypted", sa.Text, nullable=True),
    sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"))
)

partners = sa.Table(
    "partners",
    metadata,
    sa.Column("id", sa.String, primary_key=True),
    sa.Column("name", sa.String, nullable=False),
    sa.Column("region", sa.String, nullable=True),
    sa.Column("contact", sa.String, nullable=True),
    sa.Column("type", sa.String, nullable=True),
    sa.Column("notes", sa.Text, nullable=True),
    sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"))
)

requests = sa.Table(
    "requests",
    metadata,
    sa.Column("id", sa.String, primary_key=True),
    sa.Column("category", sa.String),
    sa.Column("region", sa.String),
    sa.Column("short_text", sa.Text),
    sa.Column("phone_encrypted", sa.Text),
    sa.Column("consent", sa.Boolean, server_default=sa.text("false")),
    sa.Column("status", sa.String, server_default="'new'"),
    sa.Column("assigned_to", sa.String, nullable=True),
    sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"))
)

audit_logs = sa.Table(
    "audit_logs",
    metadata,
    sa.Column("id", sa.String, primary_key=True),
    sa.Column("request_id", sa.String),
    sa.Column("action", sa.String),
    sa.Column("actor", sa.String),
    sa.Column("timestamp", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"))
)

