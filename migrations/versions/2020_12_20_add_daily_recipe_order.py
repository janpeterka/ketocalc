"""Add daily recipes ordering

Revision ID: beee24f900a0
Revises: 0e33f7c6d78b
Create Date: 2020-12-20 22:31:23.507283

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "beee24f900a0"
down_revision = "0e33f7c6d78b"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "daily_plan_has_recipes", sa.Column("order_index", sa.Integer(), nullable=True)
    )


def downgrade():
    op.drop_column("daily_plan_has_recipes", "order_index")
