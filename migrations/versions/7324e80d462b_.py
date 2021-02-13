"""empty message

Revision ID: 7324e80d462b
Revises: 373347b04d53
Create Date: 2020-05-26 17:53:24.830882

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7324e80d462b'
down_revision = '373347b04d53'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'cash',
                    existing_type=sa.FLOAT(),
                    nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'cash',
                    existing_type=sa.FLOAT(),
                    nullable=True)
    # ### end Alembic commands ###
