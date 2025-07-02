"""Change ondelete

Revision ID: f1ed1ca9adbd
Revises: ad919495751e
Create Date: 2025-06-07 09:06:24.113176

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'f1ed1ca9adbd'
down_revision: Union[str, None] = 'ad919495751e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
