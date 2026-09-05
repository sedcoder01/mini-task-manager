"""create_tasks_table

Revision ID: b7cd9d1a1fd3
Revises: 22a69ad3c5f2
Create Date: 2026-08-22 14:54:12.230736

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b7cd9d1a1fd3'
down_revision: Union[str, Sequence[str], None] = '22a69ad3c5f2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'tasks',
        sa.Column('id',sa.Integer,autoincrement=True,primary_key=True,index=True),
        sa.Column('title',sa.String,nullable=False),
        sa.Column('description',sa.String,nullable=False),
        sa.Column(
            'status',
            sa.Enum('todo', 'in_progress', 'done', name='status'),
            nullable=False
        ),
        sa.Column(
            'priority',
            sa.Enum('low', 'medium', 'high', name='priority'),
            nullable=False
        ),
        sa.Column('due_date',sa.Date,nullable=False),
        sa.Column('user_id',sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('create_at',sa.DateTime(timezone=True),nullable=False),
        sa.Column('update_at',sa.DateTime(timezone=True),onupdate=sa.DateTime(timezone=True),nullable=False),
        if_not_exists=True
    )


def downgrade() -> None:
    op.drop_table('tasks',if_exists=True)