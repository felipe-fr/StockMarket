"""empty message

Revision ID: 373347b04d53
Revises: c9a8330c9091
Create Date: 2020-05-26 17:08:05.355922

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '373347b04d53'
down_revision = 'c9a8330c9091'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('cash', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'cash')
    # ### end Alembic commands ###
