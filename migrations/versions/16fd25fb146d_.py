"""empty message

Revision ID: 16fd25fb146d
Revises: 0804ed50dd67
Create Date: 2024-04-07 15:25:18.568169

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '16fd25fb146d'
down_revision = '0804ed50dd67'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint('uq_user_username', type_='unique')
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.create_unique_constraint('uq_user_username', ['username'])

    # ### end Alembic commands ###
