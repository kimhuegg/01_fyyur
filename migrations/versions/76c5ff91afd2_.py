"""empty message

Revision ID: 76c5ff91afd2
Revises: 
Create Date: 2024-04-18 15:10:17.272620

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76c5ff91afd2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Artist', schema=None) as batch_op:
        batch_op.drop_column('genres')

    with op.batch_alter_table('Show', schema=None) as batch_op:
        batch_op.drop_column('artist_id')
        batch_op.drop_column('venue_id')

    with op.batch_alter_table('Venue', schema=None) as batch_op:
        batch_op.drop_column('genres')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Venue', schema=None) as batch_op:
        batch_op.add_column(sa.Column('genres', sa.VARCHAR(), autoincrement=False, nullable=True))

    with op.batch_alter_table('Show', schema=None) as batch_op:
        batch_op.add_column(sa.Column('venue_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('artist_id', sa.INTEGER(), autoincrement=False, nullable=False))

    with op.batch_alter_table('Artist', schema=None) as batch_op:
        batch_op.add_column(sa.Column('genres', sa.VARCHAR(), autoincrement=False, nullable=True))

    # ### end Alembic commands ###
