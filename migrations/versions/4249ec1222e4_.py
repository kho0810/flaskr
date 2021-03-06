"""empty message

Revision ID: 4249ec1222e4
Revises: 481d4a3fef63
Create Date: 2014-08-14 22:02:40.703605

"""

# revision identifiers, used by Alembic.
revision = '4249ec1222e4'
down_revision = '481d4a3fef63'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_info',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_info')
    ### end Alembic commands ###
