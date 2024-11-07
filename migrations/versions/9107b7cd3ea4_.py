"""empty message

Revision ID: 9107b7cd3ea4
Revises: 9f0b21c68086
Create Date: 2024-11-07 10:50:40.589452

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9107b7cd3ea4'
down_revision = '9f0b21c68086'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('goal', schema=None) as batch_op:
        batch_op.add_column(sa.Column('title', sa.String(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('goal', schema=None) as batch_op:
        batch_op.drop_column('title')

    # ### end Alembic commands ###
