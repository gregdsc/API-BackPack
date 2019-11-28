"""empty message

Revision ID: af73dde586d8
Revises: d95054e3733c
Create Date: 2019-11-28 11:24:59.192012

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'af73dde586d8'
down_revision = 'd95054e3733c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ramble_tag_association')
    op.drop_table('tags')
    op.add_column('rambles', sa.Column('tag', sa.String(length=255), nullable=True))
    op.drop_constraint('rambles_tag_id_fkey', 'rambles', type_='foreignkey')
    op.drop_column('rambles', 'tag_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rambles', sa.Column('tag_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('rambles_tag_id_fkey', 'rambles', 'tags', ['tag_id'], ['id'])
    op.drop_column('rambles', 'tag')
    op.create_table('tags',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('tags_id_seq'::regclass)"), nullable=False),
    sa.Column('name', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='tags_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('ramble_tag_association',
    sa.Column('ramble_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('tag_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['ramble_id'], ['tags.id'], name='ramble_tag_association_ramble_id_fkey'),
    sa.ForeignKeyConstraint(['tag_id'], ['rambles.id'], name='ramble_tag_association_tag_id_fkey')
    )
    # ### end Alembic commands ###
