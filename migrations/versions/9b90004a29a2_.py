"""empty message

Revision ID: 9b90004a29a2
Revises: a8a0fbdf5043
Create Date: 2020-05-27 15:06:57.969324

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9b90004a29a2"
down_revision = "a8a0fbdf5043"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "daily_plans",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "daily_plan_has_recipes",
        sa.Column("recipes_id", sa.Integer(), nullable=False),
        sa.Column("daily_plans_id", sa.Integer(), nullable=False),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column("added_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["daily_plans_id"], ["daily_plans.id"],),
        sa.ForeignKeyConstraint(["recipes_id"], ["recipes.id"],),
        sa.PrimaryKeyConstraint("recipes_id", "daily_plans_id"),
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
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_daily_plan_has_recipes_recipes_id"),
        table_name="daily_plan_has_recipes",
    )
    op.drop_index(
        op.f("ix_daily_plan_has_recipes_daily_plans_id"),
        table_name="daily_plan_has_recipes",
    )
    op.drop_table("daily_plan_has_recipes")
    op.drop_table("daily_plans")
    # ### end Alembic commands ###
