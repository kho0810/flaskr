"""empty message

Revision ID: 3f055fdcbbd0
Revises: 54f112ff6b1e
Create Date: 2014-08-08 01:42:44.958987

"""

# revision identifiers, used by Alembic.
revision = '3f055fdcbbd0'
down_revision = '54f112ff6b1e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comment', sa.Column('like', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comment', 'like')
    ### end Alembic commands ###
