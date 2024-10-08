"""Normalna migratiya

Revision ID: ae150705e8e3
Revises: 
Create Date: 2024-09-24 15:31:26.253033

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ae150705e8e3'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('streets',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_streets_id'), 'streets', ['id'], unique=True)
    op.create_table('cameras',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('streetId', sa.Uuid(), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['streetId'], ['streets.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cameras_id'), 'cameras', ['id'], unique=True)
    op.create_table('archivestask',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('cameraId', sa.Uuid(), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['cameraId'], ['cameras.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_archivestask_id'), 'archivestask', ['id'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_archivestask_id'), table_name='archivestask')
    op.drop_table('archivestask')
    op.drop_index(op.f('ix_cameras_id'), table_name='cameras')
    op.drop_table('cameras')
    op.drop_index(op.f('ix_streets_id'), table_name='streets')
    op.drop_table('streets')
    # ### end Alembic commands ###
