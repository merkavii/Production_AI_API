"""add processing time

Revision ID: afd88191b0f3
Revises: 23b742b3d9d2
Create Date: 2026-09-13 12:13:59.282189

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'afd88191b0f3'
down_revision: Union[str, Sequence[str], None] = '23b742b3d9d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        'predictions',
        sa.Column(
            'processing_time',
            sa.Float(),
            nullable=True
        )
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        'predictions',
        'processing_time'
    )