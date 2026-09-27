"""add password hash to users

Revision ID: your_revision_id
Revises: previous_revision_id
Create Date: 2026-09-27

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b26584335c7"
down_revision: Union[str, Sequence[str], None] = "afd88191b0f3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # مرحله ۱:
    # اضافه کردن ستون به صورت nullable
    op.add_column(
        "users",
        sa.Column(
            "password_hash",
            sa.Text(),
            nullable=True
        )
    )

    # مرحله ۲:
    # مقدار موقت برای Userهای قبلی
    op.execute(
        """
        UPDATE users
        SET password_hash = 'TEMP_PASSWORD_HASH'
        WHERE password_hash IS NULL
        """
    )

    # مرحله ۳:
    # تبدیل ستون به اجباری
    op.alter_column(
        "users",
        "password_hash",
        existing_type=sa.Text(),
        nullable=False
    )


def downgrade() -> None:
    op.drop_column(
        "users",
        "password_hash"
    )