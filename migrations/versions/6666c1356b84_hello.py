"""hello

Revision ID: 6666c1356b84
Revises: 
Create Date: 2022-12-17 21:35:11.813275

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6666c1356b84'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('file', schema=None) as batch_op:
        batch_op.add_column(sa.Column('repo', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'repo', ['repo'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('file', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('repo')

    # ### end Alembic commands ###
