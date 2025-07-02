"""Change ondelete 2

Revision ID: 9a3d02a85b75
Revises: f1ed1ca9adbd
Create Date: 2025-06-07 09:10:17.529853

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '9a3d02a85b75'
down_revision: Union[str, None] = 'f1ed1ca9adbd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
