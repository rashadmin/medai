"""empty message

Revision ID: 4ef309018f61
Revises: 16fd25fb146d
Create Date: 2024-04-08 22:47:52.375892

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ef309018f61'
down_revision = '16fd25fb146d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('anonyuser', schema=None) as batch_op:
        batch_op.add_column(sa.Column('referrer', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_anonyuser_referrer_user'), 'user', ['referrer'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('anonyuser', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_anonyuser_referrer_user'), type_='foreignkey')
        batch_op.drop_column('referrer')

    # ### end Alembic commands ###
