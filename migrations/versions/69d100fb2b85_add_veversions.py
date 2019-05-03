"""Add veversions

Revision ID: 69d100fb2b85
Revises: 3afe172c9500
Create Date: 2019-05-02 20:49:19.868076

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '69d100fb2b85'
down_revision = '3afe172c9500'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ver_tags',
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('page_version_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['page_version_id'], ['page_version.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], ),
    sa.PrimaryKeyConstraint('tag_id', 'page_version_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ver_tags')
    # ### end Alembic commands ###
