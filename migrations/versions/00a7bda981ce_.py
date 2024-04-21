"""empty message

Revision ID: 00a7bda981ce
Revises: c31c2df9ff22
Create Date: 2024-04-20 12:00:45.105501

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00a7bda981ce'
down_revision = 'c31c2df9ff22'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('artist', schema=None) as batch_op:
        batch_op.add_column(sa.Column('seeking_venue', sa.Boolean(), nullable=True))
        batch_op.drop_column('seeking_talent')
        batch_op.drop_column('address')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('artist', schema=None) as batch_op:
        batch_op.add_column(sa.Column('address', sa.VARCHAR(length=120), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('seeking_talent', sa.BOOLEAN(), autoincrement=False, nullable=True))
        batch_op.drop_column('seeking_venue')

    # ### end Alembic commands ###