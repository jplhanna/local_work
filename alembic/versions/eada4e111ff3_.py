"""empty message

Revision ID: eada4e111ff3
Revises: dd5001604d65
Create Date: 2022-05-15 21:29:44.873852

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "eada4e111ff3"
down_revision = "dd5001604d65"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "quest",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("datetime_created", sa.DateTime(), nullable=False),
        sa.Column("experience", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user_quest",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("quest_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["quest_id"],
            ["quest.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("user_id", "quest_id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user_quest")
    op.drop_table("quest")
    # ### end Alembic commands ###
