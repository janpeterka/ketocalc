"""Add ingredient info

Revision ID: e82be42f5a24
Revises: beee24f900a0
Create Date: 2021-01-13 00:25:47.781964

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e82be42f5a24"
down_revision = "beee24f900a0"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("ingredients", sa.Column("description", sa.Text(), nullable=True))
    op.add_column("ingredients", sa.Column("ean_code", sa.Integer(), nullable=True))


def downgrade():
    op.drop_column("ingredients", "ean_code")
    op.drop_column("ingredients", "description")
