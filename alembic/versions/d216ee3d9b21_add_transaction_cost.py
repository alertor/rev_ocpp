"""Add transaction cost

Revision ID: d216ee3d9b21
Revises: fc06ff7c4088
Create Date: 2021-03-10 22:05:53.784101

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd216ee3d9b21'
down_revision = 'fc06ff7c4088'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transaction', sa.Column('cost_per_kwh', sa.Float(), nullable=True))
    op.execute('UPDATE transaction SET cost_per_kwh = 0')
    op.alter_column('transaction', 'cost_per_kwh', nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('transaction', 'cost_per_kwh')
    # ### end Alembic commands ###
