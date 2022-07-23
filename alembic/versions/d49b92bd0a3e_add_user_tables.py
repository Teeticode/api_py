"""add user tables

Revision ID: d49b92bd0a3e
Revises: 12c244d5e617
Create Date: 2022-07-22 19:56:17.751637

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd49b92bd0a3e'
down_revision = '189de41efd26'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users', 
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), 
                server_default=sa.text('now()'), nullable=False),
        sa.Column('userid', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('userid')
    )
    pass


def downgrade():
    op.drop_table('users')
    pass
