"""Add ingredient info

Revision ID: 5e82e2bc758c
Revises: beee24f900a0
Create Date: 2021-01-13 12:09:42.712611

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "5e82e2bc758c"
down_revision = "beee24f900a0"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("ingredients", sa.Column("description", sa.Text(), nullable=True))
    op.add_column(
        "ingredients", sa.Column("ean_code", sa.String(length=13), nullable=True)
    )


def downgrade():
    op.drop_column("ingredients", "ean_code")
    op.drop_column("ingredients", "description")
