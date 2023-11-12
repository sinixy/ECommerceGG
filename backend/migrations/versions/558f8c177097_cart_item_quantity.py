"""cart item quantity

Revision ID: 558f8c177097
Revises: 5bd1e3c1ba48
Create Date: 2022-08-09 02:28:53.003626

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '558f8c177097'
down_revision = '5bd1e3c1ba48'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # https://medium.com/the-andela-way/alembic-how-to-add-a-non-nullable-field-to-a-populated-table-998554003134
    op.add_column('CartItem', sa.Column('quantity', sa.Integer(), nullable=True))
    op.execute('UPDATE public."CartItem" SET quantity = 1')
    op.alter_column('CartItem', 'quantity', nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('CartItem', 'quantity')
    # ### end Alembic commands ###