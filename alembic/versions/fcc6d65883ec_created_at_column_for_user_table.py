"""created_at column for user table

Revision ID: fcc6d65883ec
Revises: 63f9e643f573
Create Date: 2022-02-23 23:00:03.852773

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "fcc6d65883ec"
down_revision = "63f9e643f573"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "users",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )
    pass


def downgrade():
    op.drop_column("users", "created_at")
    pass
