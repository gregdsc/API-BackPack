"""empty message

Revision ID: 56310b5f7fd0
Revises: b623d18b7a77
Create Date: 2019-11-24 23:48:28.639497

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '56310b5f7fd0'
down_revision = 'b623d18b7a77'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rambles', sa.Column('tag_id', sa.Integer(), nullable=True))
    op.add_column('rambles', sa.Column('visible', sa.Boolean(), nullable=True))
    op.create_foreign_key(None, 'rambles', 'tags', ['tag_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'rambles', type_='foreignkey')
    op.drop_column('rambles', 'visible')
    op.drop_column('rambles', 'tag_id')
    # ### end Alembic commands ###
