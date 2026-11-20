"""Align the matchmaking table with the queue model without dropping data.

Revision ID: 6f5acf08ed23
Revises:
Create Date: 2026-11-16 15:43:34.066817
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

revision: str = "6f5acf08ed23"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    if "matchmaking" not in inspector.get_table_names():
        op.create_table(
            "matchmaking",
            sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
            sa.Column("playerID", sa.String(), nullable=False, unique=True),
            sa.Column("ticketID", sa.String(), nullable=False, unique=True),
            sa.Column("playerStatus", sa.Boolean(), nullable=False),
            sa.Column("joinAT", sa.DateTime(timezone=True), nullable=True),
            sa.Column(
                "matching_status",
                sa.String(),
                nullable=False,
                server_default="waiting",
            ),
        )
        return

    columns = {column["name"] for column in inspector.get_columns("matchmaking")}
    if "status" in columns and "matching_status" not in columns:
        op.alter_column("matchmaking", "status", new_column_name="matching_status")
        columns.remove("status")
        columns.add("matching_status")

    if "playerStatus" not in columns:
        op.add_column(
            "matchmaking",
            sa.Column("playerStatus", sa.Boolean(), nullable=False, server_default=sa.true()),
        )
        op.alter_column("matchmaking", "playerStatus", server_default=None)

    if "matching_status" not in columns:
        op.add_column(
            "matchmaking",
            sa.Column(
                "matching_status",
                sa.String(),
                nullable=False,
                server_default="waiting",
            ),
        )
        op.alter_column("matchmaking", "matching_status", server_default=None)


def downgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    if "matchmaking" not in inspector.get_table_names():
        return

    columns = {column["name"] for column in inspector.get_columns("matchmaking")}
    if "matching_status" in columns and "status" not in columns:
        op.alter_column("matchmaking", "matching_status", new_column_name="status")
    if "playerStatus" in columns:
        op.drop_column("matchmaking", "playerStatus")
