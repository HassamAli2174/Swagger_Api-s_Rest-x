"""Roles updated

Revision ID: e8693d4a748f
Revises: 944b41cfa8e0
Create Date: 2024-09-10 15:29:43.269840

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8693d4a748f'
down_revision = '944b41cfa8e0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('role_name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('role_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('roles')
    # ### end Alembic commands ###