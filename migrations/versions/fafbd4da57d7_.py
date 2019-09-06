"""empty message

Revision ID: fafbd4da57d7
Revises: b1b55177b863
Create Date: 2019-08-26 15:46:05.411984

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'fafbd4da57d7'
down_revision = 'b1b55177b863'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
   ## op.drop_table('activity')
    op.add_column('users', sa.Column('token_reset_password', sa.String(length=500), nullable=True))
    op.create_table('activity',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('start_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('end_time', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('pas', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('km', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('calorie', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('speed', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('type', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='activity_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='activity_pkey')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'token_reset_password')
    # op.create_table('activity',
    # sa.Column('id', sa.INTEGER(), nullable=False),
    # sa.Column('name', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    # sa.Column('start_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    # sa.Column('end_time', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    # sa.Column('pas', sa.INTEGER(), autoincrement=False, nullable=True),
    # sa.Column('km', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    # sa.Column('calorie', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    # sa.Column('speed', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    # sa.Column('type', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    # sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    # sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='activity_user_id_fkey'),
    # sa.PrimaryKeyConstraint('id', name='activity_pkey')
    #)
    # ### end Alembic commands ###
