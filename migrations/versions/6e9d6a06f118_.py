"""empty message

Revision ID: 6e9d6a06f118
Revises: d446a91ee007
Create Date: 2019-07-06 12:51:51.079522

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e9d6a06f118'
down_revision = 'd446a91ee007'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('token', sa.String(length=32), nullable=True))
    op.add_column('users', sa.Column('token_expiration', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_users_token'), 'users', ['token'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_token'), table_name='users')
    op.drop_column('users', 'token_expiration')
    op.drop_column('users', 'token')
    # ### end Alembic commands ###
