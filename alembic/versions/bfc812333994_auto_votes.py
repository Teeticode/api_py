"""auto-votes

Revision ID: bfc812333994
Revises: 4c4423098253
Create Date: 2022-07-23 07:44:54.281343

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bfc812333994'
down_revision = '4c4423098253'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('votes',
    sa.Column('userid', sa.BigInteger(), nullable=False),
    sa.Column('postid', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['postid'], ['posts.postid'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['userid'], ['users.userid'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('userid', 'postid')
    )
    op.create_unique_constraint(None, 'posts', ['postid'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'posts', type_='unique')
    op.drop_table('votes')
    # ### end Alembic commands ###
