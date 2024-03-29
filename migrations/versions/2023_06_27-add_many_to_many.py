"""add_many_to_many

Revision ID: f74b65f618d3
Revises: 9294ae927ff4
Create Date: 2023-06-27 13:11:33.670450

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f74b65f618d3'
down_revision = '9294ae927ff4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category_right',
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('right_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.ForeignKeyConstraint(['right_id'], ['rights.id'], )
    )
    op.drop_constraint('rights_category_id_fkey', 'rights', type_='foreignkey')
    op.drop_column('rights', 'category_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rights', sa.Column('category_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('rights_category_id_fkey', 'rights', 'categories', ['category_id'], ['id'])
    op.drop_table('category_right')
    # ### end Alembic commands ###
