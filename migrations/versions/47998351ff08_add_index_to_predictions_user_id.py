"""add index to predictions user_id

Revision ID: 47998351ff08
Revises: e92f0d9699ae
Create Date: 2026-09-19 17:44:14.721529

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '47998351ff08'
down_revision: Union[str, Sequence[str], None] = 'e92f0d9699ae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_index(
    "ix_predictions_user_id",
    "predictions",
    ["user_id"]
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
    "ix_predictions_user_id",
    table_name="predictions"
)
