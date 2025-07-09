"""Create phone number for user column

Revision ID: 5d8db43ffc53
Revises: 
Create Date: 2025-07-09 12:26:15.030345

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5d8db43ffc53'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'users',
        sa.Column('phone_number', sa.String(length=15), nullable=True)
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
