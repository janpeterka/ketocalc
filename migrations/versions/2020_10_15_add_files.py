"""Add files

Revision ID: 530497042e9d
Revises: 82f0a4250028
Create Date: 2020-10-15 18:32:24.866082

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "530497042e9d"
down_revision = "82f0a4250028"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "files",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("extension", sa.String(length=255), nullable=False),
        sa.Column("path", sa.String(length=255), nullable=False),
        sa.Column("hash", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("recipe_id", sa.Integer(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=False),
        sa.Column("file_type", sa.String(length=40), nullable=True),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"],),
        sa.ForeignKeyConstraint(["recipe_id"], ["recipes.id"],),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"],),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_files_created_by"), "files", ["created_by"], unique=False)


def downgrade():
    op.drop_table("files")
