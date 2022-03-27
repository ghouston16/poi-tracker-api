"""add categories

Revision ID: 8557a2738ac0
Revises: ec70e81241a2
Create Date: 2022-03-15 00:53:28.073685

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8557a2738ac0"
down_revision = "ec70e81241a2"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("creator", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["creator"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("categories")
    # ### end Alembic commands ###
