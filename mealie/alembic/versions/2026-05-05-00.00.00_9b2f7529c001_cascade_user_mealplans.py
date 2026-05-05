"""cascade user meal plans

Revision ID: 9b2f7529c001
Revises: 4395a04f7784
Create Date: 2026-05-05 00:00:00.000000

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "9b2f7529c001"
down_revision = "4395a04f7784"
branch_labels: str | tuple[str, ...] | None = None
depends_on: str | tuple[str, ...] | None = None


def upgrade():
    with op.batch_alter_table("group_meal_plans", schema=None) as batch_op:
        batch_op.drop_constraint("fk_user_mealplans", type_="foreignkey")
        batch_op.create_foreign_key(
            "fk_user_mealplans",
            "users",
            ["user_id"],
            ["id"],
            ondelete="CASCADE",
        )


def downgrade():
    with op.batch_alter_table("group_meal_plans", schema=None) as batch_op:
        batch_op.drop_constraint("fk_user_mealplans", type_="foreignkey")
        batch_op.create_foreign_key(
            "fk_user_mealplans",
            "users",
            ["user_id"],
            ["id"],
        )
