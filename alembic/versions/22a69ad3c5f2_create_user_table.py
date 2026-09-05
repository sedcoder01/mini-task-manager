"""create user table

Revision ID: 22a69ad3c5f2
Revises: 
Create Date: 2026-08-18 16:30:53.161877

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '22a69ad3c5f2'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id',sa.Integer,autoincrement=True,primary_key=True,index=True),
        sa.Column('name',sa.String,nullable=False),
        sa.Column('email',sa.String,nullable=False,unique=True),
        sa.Column('create_at',sa.DateTime(timezone=True)),
        sa.Column('create_at_shamsi', sa.String),
        if_not_exists=True
    )


def downgrade() -> None:
    op.drop_table('users',if_exists=True)
