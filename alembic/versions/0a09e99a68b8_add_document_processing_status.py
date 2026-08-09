"""add document processing status

Revision ID: 0a09e99a68b8
Revises: 7b503daeab00
Create Date: 2026-08-08 15:40:34.519232

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0a09e99a68b8"
down_revision: Union[str, Sequence[str], None] = "7b503daeab00"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "documents",
        sa.Column(
            "status",
            sa.String(),
            nullable=False,
            server_default="UPLOADED",
        ),
    )

    op.alter_column(
        "documents",
        "status",
        server_default=None,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        "documents",
        "status",
    )