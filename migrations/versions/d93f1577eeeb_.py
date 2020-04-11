"""empty message

Revision ID: d93f1577eeeb
Revises: efe33eafa19a
Create Date: 2020-04-11 18:52:56.027140

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


# revision identifiers, used by Alembic.
revision = "d93f1577eeeb"
down_revision = "efe33eafa19a"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "recipes",
        "type",
        existing_nullable=False,
        existing_type=mysql.ENUM("small", "big"),
        type_=mysql.ENUM("small", "big", "full"),
        server_default="full",
    )
    pass


def downgrade():
    op.alter_column(
        "recipes",
        "type",
        existing_nullable=False,
        existing_type=mysql.ENUM("small", "big", "full"),
        type_=mysql.ENUM("small", "big"),
    )
    pass
