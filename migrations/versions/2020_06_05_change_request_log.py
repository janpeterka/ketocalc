"""Change request log

Revision ID: 27cf1eba3af3
Revises: a157327dd8c5
Create Date: 2020-06-05 15:11:44.544495

"""
from alembic import op
from sqlalchemy.dialects import mysql


# revision identifiers, used by Alembic.
revision = "27cf1eba3af3"
down_revision = "a157327dd8c5"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "request_logs",
        "item_type",
        existing_type=mysql.ENUM("user", "diet", "recipe", "ingredient"),
        type_=mysql.VARCHAR(length=255),
    )


def downgrade():
    op.alter_column(
        "request_logs",
        "item_type",
        existing_type=mysql.VARCHAR(length=255),
        type_=mysql.ENUM("user", "diet", "recipe", "ingredient"),
    )
