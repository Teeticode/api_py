"""Create Posts Table

Revision ID: 189de41efd26
Revises: 
Create Date: 2022-07-22 06:54:39.337168

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '189de41efd26'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
    sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
