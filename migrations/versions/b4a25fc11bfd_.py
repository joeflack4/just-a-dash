"""empty message

Revision ID: b4a25fc11bfd
Revises: c0587e8beb97
Create Date: 2016-03-28 01:52:28.108029

"""

# revision identifiers, used by Alembic.
revision = 'b4a25fc11bfd'
down_revision = 'c0587e8beb97'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('messages', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'messages', 'user', ['user_id'], ['id'])
    op.drop_column('messages', 'destinations')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('messages', sa.Column('destinations', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'messages', type_='foreignkey')
    op.drop_column('messages', 'user_id')
    ### end Alembic commands ###
