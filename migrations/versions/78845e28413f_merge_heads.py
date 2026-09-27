"""merge heads

Revision ID: 78845e28413f
Revises: 47998351ff08, b26584335c7
Create Date: 2026-09-27 23:41:16.196105

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '78845e28413f'
down_revision: Union[str, Sequence[str], None] = ('47998351ff08', 'b26584335c7')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
