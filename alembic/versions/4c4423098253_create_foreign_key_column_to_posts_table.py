"""create foreign-key column to posts table

Revision ID: 4c4423098253
Revises: d49b92bd0a3e
Create Date: 2022-07-22 20:59:04.960815

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c4423098253'
down_revision = 'd49b92bd0a3e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('userid', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users",
    local_cols=["userid"], remote_cols=['userid'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'userid')
    pass
