"""countries

Revision ID: 822b22b0597b
Revises: 558f8c177097
Create Date: 2023-10-30 21:42:27.193676

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '822b22b0597b'
down_revision = '558f8c177097'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Country', schema=None) as batch_op:
        batch_op.add_column(sa.Column('code', sa.String(length=2), nullable=False))
        batch_op.create_unique_constraint(None, ['code'])
        batch_op.drop_constraint('Country_flag_id_fkey', type_='foreignkey')
        batch_op.drop_column('flag_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Country', schema=None) as batch_op:
        batch_op.add_column(sa.Column('flag_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('Country_flag_id_fkey', 'Image', ['flag_id'], ['id'], ondelete='SET NULL')
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('code')

    # ### end Alembic commands ###