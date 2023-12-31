"""essage=Добавил date_csi к User

Revision ID: 689917b61f18
Revises: cb88a945ff82
Create Date: 2023-06-13 09:23:50.545857

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '689917b61f18'
down_revision = 'cb88a945ff82'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('date1_csi', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('date2_csi', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('date3_csi', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('date4_csi', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('date5_csi', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('date6_csi', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'date6_csi')
    op.drop_column('users', 'date5_csi')
    op.drop_column('users', 'date4_csi')
    op.drop_column('users', 'date3_csi')
    op.drop_column('users', 'date2_csi')
    op.drop_column('users', 'date1_csi')
    # ### end Alembic commands ###
