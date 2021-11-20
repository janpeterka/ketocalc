"""Recreate all, as old files were corrupted

Revision ID: 0efe9783fb05
Revises: 
Create Date: 2021-11-20 14:00:28.073486

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0efe9783fb05"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "ingredients",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("calorie", sa.Float(), server_default=sa.text("'0'"), nullable=False),
        sa.Column("sugar", sa.Float(), server_default=sa.text("'0'"), nullable=False),
        sa.Column("fat", sa.Float(), server_default=sa.text("'0'"), nullable=False),
        sa.Column("protein", sa.Float(), server_default=sa.text("'0'"), nullable=False),
        sa.Column("author", sa.String(length=255), nullable=True),
        sa.Column("created", sa.DateTime(), nullable=True),
        sa.Column("last_updated", sa.DateTime(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("ean_code", sa.String(length=13), nullable=True),
        sa.Column("is_shared", sa.Boolean(), nullable=True),
        sa.Column("is_approved", sa.Boolean(), nullable=True),
        sa.Column("source", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "logs",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("logger", sa.String(length=255), nullable=True),
        sa.Column("level", sa.String(length=255), nullable=True),
        sa.Column("msg", sa.Text(), nullable=True),
        sa.Column("url", sa.String(length=255), nullable=True),
        sa.Column("remote_addr", sa.String(length=255), nullable=True),
        sa.Column("module", sa.String(length=255), nullable=True),
        sa.Column("timestamp", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_logs_level"), "logs", ["level"], unique=False)
    op.create_table(
        "recipes",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("type", sa.Enum("small", "big", "full"), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created", sa.DateTime(), nullable=True),
        sa.Column("last_updated", sa.DateTime(), nullable=True),
        sa.Column("is_shared", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("google_id", sa.String(length=30), nullable=True),
        sa.Column("username", sa.String(length=255), nullable=False),
        sa.Column("pwdhash", sa.CHAR(length=64), nullable=True),
        sa.Column("first_name", sa.String(length=255), nullable=False),
        sa.Column("last_name", sa.String(length=255), nullable=False),
        sa.Column("password_version", sa.String(length=45), nullable=True),
        sa.Column("created", sa.DateTime(), nullable=True),
        sa.Column("last_logged_in", sa.DateTime(), nullable=True),
        sa.Column("login_count", sa.Integer(), nullable=True),
        sa.Column("new_password_token", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("google_id"),
        sa.UniqueConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    op.create_table(
        "daily_plans",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_daily_plans_user_id"), "daily_plans", ["user_id"], unique=False
    )
    op.create_table(
        "diets",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("calorie", sa.Float(), nullable=False),
        sa.Column("sugar", sa.Float(), nullable=False),
        sa.Column("fat", sa.Float(), nullable=False),
        sa.Column("protein", sa.Float(), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=True),
        sa.Column("last_updated", sa.DateTime(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_diets_user_id"), "diets", ["user_id"], unique=False)
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
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["users.id"],
        ),
        sa.ForeignKeyConstraint(
            ["recipe_id"],
            ["recipes.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_files_created_by"), "files", ["created_by"], unique=False)
    op.create_table(
        "recipes_has_ingredients",
        sa.Column("recipes_id", sa.Integer(), nullable=False),
        sa.Column("ingredients_id", sa.Integer(), nullable=False),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(
            ["ingredients_id"],
            ["ingredients.id"],
        ),
        sa.ForeignKeyConstraint(
            ["recipes_id"],
            ["recipes.id"],
        ),
        sa.PrimaryKeyConstraint("recipes_id", "ingredients_id"),
    )
    op.create_index(
        op.f("ix_recipes_has_ingredients_ingredients_id"),
        "recipes_has_ingredients",
        ["ingredients_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_recipes_has_ingredients_recipes_id"),
        "recipes_has_ingredients",
        ["recipes_id"],
        unique=False,
    )
    op.create_table(
        "request_logs",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("url", sa.String(length=255), nullable=True),
        sa.Column("remote_addr", sa.String(length=255), nullable=True),
        sa.Column("duration", sa.Float(precision=4), nullable=True),
        sa.Column("item_type", sa.String(length=255), nullable=True),
        sa.Column("item_id", sa.Integer(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_request_logs_user_id"), "request_logs", ["user_id"], unique=False
    )
    op.create_table(
        "sent_mails",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("subject", sa.String(length=255), nullable=False),
        sa.Column("sender", sa.String(length=255), nullable=False),
        sa.Column("recipient_id", sa.Integer(), nullable=False),
        sa.Column("bcc", sa.String(length=255), nullable=True),
        sa.Column("template", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["recipient_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )
    op.create_index(
        op.f("ix_sent_mails_recipient_id"), "sent_mails", ["recipient_id"], unique=False
    )
    op.create_table(
        "user_recipe_reactions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("recipe_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["recipe_id"],
            ["recipes.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_user_recipe_reactions_recipe_id"),
        "user_recipe_reactions",
        ["recipe_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_user_recipe_reactions_user_id"),
        "user_recipe_reactions",
        ["user_id"],
        unique=False,
    )
    op.create_table(
        "daily_plan_has_recipes",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("recipes_id", sa.Integer(), nullable=False),
        sa.Column("daily_plans_id", sa.Integer(), nullable=False),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column("order_index", sa.Integer(), nullable=True),
        sa.Column("added_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["daily_plans_id"],
            ["daily_plans.id"],
        ),
        sa.ForeignKeyConstraint(
            ["recipes_id"],
            ["recipes.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_daily_plan_has_recipes_daily_plans_id"),
        "daily_plan_has_recipes",
        ["daily_plans_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_daily_plan_has_recipes_recipes_id"),
        "daily_plan_has_recipes",
        ["recipes_id"],
        unique=False,
    )
    op.create_table(
        "diets_has_recipes",
        sa.Column("diet_id", sa.Integer(), nullable=False),
        sa.Column("recipes_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["diet_id"],
            ["diets.id"],
        ),
        sa.ForeignKeyConstraint(
            ["recipes_id"],
            ["recipes.id"],
        ),
        sa.PrimaryKeyConstraint("diet_id", "recipes_id"),
    )
    op.create_index(
        op.f("ix_diets_has_recipes_diet_id"),
        "diets_has_recipes",
        ["diet_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_diets_has_recipes_recipes_id"),
        "diets_has_recipes",
        ["recipes_id"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_diets_has_recipes_recipes_id"), table_name="diets_has_recipes"
    )
    op.drop_index(op.f("ix_diets_has_recipes_diet_id"), table_name="diets_has_recipes")
    op.drop_table("diets_has_recipes")
    op.drop_index(
        op.f("ix_daily_plan_has_recipes_recipes_id"),
        table_name="daily_plan_has_recipes",
    )
    op.drop_index(
        op.f("ix_daily_plan_has_recipes_daily_plans_id"),
        table_name="daily_plan_has_recipes",
    )
    op.drop_table("daily_plan_has_recipes")
    op.drop_index(
        op.f("ix_user_recipe_reactions_user_id"), table_name="user_recipe_reactions"
    )
    op.drop_index(
        op.f("ix_user_recipe_reactions_recipe_id"), table_name="user_recipe_reactions"
    )
    op.drop_table("user_recipe_reactions")
    op.drop_index(op.f("ix_sent_mails_recipient_id"), table_name="sent_mails")
    op.drop_table("sent_mails")
    op.drop_index(op.f("ix_request_logs_user_id"), table_name="request_logs")
    op.drop_table("request_logs")
    op.drop_index(
        op.f("ix_recipes_has_ingredients_recipes_id"),
        table_name="recipes_has_ingredients",
    )
    op.drop_index(
        op.f("ix_recipes_has_ingredients_ingredients_id"),
        table_name="recipes_has_ingredients",
    )
    op.drop_table("recipes_has_ingredients")
    op.drop_index(op.f("ix_files_created_by"), table_name="files")
    op.drop_table("files")
    op.drop_index(op.f("ix_diets_user_id"), table_name="diets")
    op.drop_table("diets")
    op.drop_index(op.f("ix_daily_plans_user_id"), table_name="daily_plans")
    op.drop_table("daily_plans")
    op.drop_table("users")
    op.drop_table("recipes")
    op.drop_index(op.f("ix_logs_level"), table_name="logs")
    op.drop_table("logs")
    op.drop_table("ingredients")
    # ### end Alembic commands ###
