"""add more value to species enum

Revision ID: 867090de2281
Revises: a96b47a4b034
Create Date: 2023-04-03 14:38:37.874488

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '867090de2281'
down_revision = 'a96b47a4b034'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('catches', 'species', nullable=False, type_=sa.Enum('CARP', 'CATFISH', 'PIKE', 'GRASS_CARP', name='species'), existing_type=sa.Enum('CARP', name='species'))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('catches', 'species', nullable=False, type_=sa.Enum('CARP', name='species'))
    # ### end Alembic commands ###
