"""essage=add 10 days

Revision ID: fb451bdcf0ee
Revises: b517520b0f20
Create Date: 2023-09-14 13:39:28.029526

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fb451bdcf0ee'
down_revision = 'b517520b0f20'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('day1', sa.Date(), nullable=True))
    op.add_column('users', sa.Column('day2', sa.Date(), nullable=True))
    op.add_column('users', sa.Column('day3', sa.Date(), nullable=True))
    op.add_column('users', sa.Column('day4', sa.Date(), nullable=True))
    op.add_column('users', sa.Column('day5', sa.Date(), nullable=True))
    op.add_column('users', sa.Column('day6', sa.Date(), nullable=True))
    op.add_column('users', sa.Column('day7', sa.Date(), nullable=True))
    op.add_column('users', sa.Column('day8', sa.Date(), nullable=True))
    op.add_column('users', sa.Column('day9', sa.Date(), nullable=True))
    op.add_column('users', sa.Column('day10', sa.Date(), nullable=True))
    op.add_column('users', sa.Column('day1_csi', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('day2_csi', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('day3_csi', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('day4_csi', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('day5_csi', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('day6_csi', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('day7_csi', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('day8_csi', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('day9_csi', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('day10_csi', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('day1_comment', sa.String(length=2000), nullable=True))
    op.add_column('users', sa.Column('day2_comment', sa.String(length=2000), nullable=True))
    op.add_column('users', sa.Column('day3_comment', sa.String(length=2000), nullable=True))
    op.add_column('users', sa.Column('day4_comment', sa.String(length=2000), nullable=True))
    op.add_column('users', sa.Column('day5_comment', sa.String(length=2000), nullable=True))
    op.add_column('users', sa.Column('day6_comment', sa.String(length=2000), nullable=True))
    op.add_column('users', sa.Column('day7_comment', sa.String(length=2000), nullable=True))
    op.add_column('users', sa.Column('day8_comment', sa.String(length=2000), nullable=True))
    op.add_column('users', sa.Column('day9_comment', sa.String(length=2000), nullable=True))
    op.add_column('users', sa.Column('day10_comment', sa.String(length=2000), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'day10_comment')
    op.drop_column('users', 'day9_comment')
    op.drop_column('users', 'day8_comment')
    op.drop_column('users', 'day7_comment')
    op.drop_column('users', 'day6_comment')
    op.drop_column('users', 'day5_comment')
    op.drop_column('users', 'day4_comment')
    op.drop_column('users', 'day3_comment')
    op.drop_column('users', 'day2_comment')
    op.drop_column('users', 'day1_comment')
    op.drop_column('users', 'day10_csi')
    op.drop_column('users', 'day9_csi')
    op.drop_column('users', 'day8_csi')
    op.drop_column('users', 'day7_csi')
    op.drop_column('users', 'day6_csi')
    op.drop_column('users', 'day5_csi')
    op.drop_column('users', 'day4_csi')
    op.drop_column('users', 'day3_csi')
    op.drop_column('users', 'day2_csi')
    op.drop_column('users', 'day1_csi')
    op.drop_column('users', 'day10')
    op.drop_column('users', 'day9')
    op.drop_column('users', 'day8')
    op.drop_column('users', 'day7')
    op.drop_column('users', 'day6')
    op.drop_column('users', 'day5')
    op.drop_column('users', 'day4')
    op.drop_column('users', 'day3')
    op.drop_column('users', 'day2')
    op.drop_column('users', 'day1')
    # ### end Alembic commands ###