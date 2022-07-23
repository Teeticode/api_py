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


def upgrade():
    op.create_table('posts', 
    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
    sa.Column('title', sa.String(), nullable=False), 
    sa.Column('content', sa.String(), nullable=False),
    sa.Column('postid', sa.BigInteger(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=True, server_default='0'),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), 
    server_default=sa.text('NOW()'), nullable=False),
    sa.Column('published', sa.Boolean(), 
    server_default="TRUE", nullable=False)
    )
    sa.UniqueConstraint("postid")
    
    pass


def downgrade():
    op.drop_table('posts')
    pass
