"""empty message

Revision ID: 3909ca955e60
Revises: 00a7bda981ce
Create Date: 2024-04-20 14:43:06.169060

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3909ca955e60'
down_revision = '00a7bda981ce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('artist', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('city',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
        batch_op.alter_column('state',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
        batch_op.alter_column('genres',
               existing_type=postgresql.ARRAY(sa.VARCHAR()),
               nullable=True)

    with op.batch_alter_table('venue', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('city',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
        batch_op.alter_column('state',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
        batch_op.alter_column('genres',
               existing_type=postgresql.ARRAY(sa.VARCHAR()),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('venue', schema=None) as batch_op:
        batch_op.alter_column('genres',
               existing_type=postgresql.ARRAY(sa.VARCHAR()),
               nullable=False)
        batch_op.alter_column('state',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
        batch_op.alter_column('city',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(),
               nullable=False)

    with op.batch_alter_table('artist', schema=None) as batch_op:
        batch_op.alter_column('genres',
               existing_type=postgresql.ARRAY(sa.VARCHAR()),
               nullable=False)
        batch_op.alter_column('state',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
        batch_op.alter_column('city',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(),
               nullable=False)

    # ### end Alembic commands ###
