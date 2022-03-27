"""add fields pois table

Revision ID: 63f9e643f573
Revises: f0b6eb23553e
Create Date: 2022-02-23 01:00:26.657090

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "63f9e643f573"
down_revision = "f0b6eb23553e"
branch_labels = None
depends_on = None


def upgrade():
    # Add User Table so User ID can be used as FK in POI table
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
    )

    # add_column max 4 positional args so each column added indiviually
    op.add_column(
        "pois",
        sa.Column("description", sa.String(), nullable=False),
    )
    # Lat Column
    op.add_column(
        "pois",
        sa.Column("lat", sa.String(), nullable=True),
    )

    op.add_column(
        "pois",
        sa.Column("lng", sa.String(), nullable=True),
    )
    op.add_column(
        "pois",
        sa.Column("category", sa.String(), nullable=True),
    )
    op.add_column(
        "pois",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )
    op.add_column("pois", sa.Column("published", sa.Boolean(), server_default="TRUE"))
    # Add creator column
    op.add_column(
        "pois",
        sa.Column("creator", sa.Integer(), nullable=False),
    )
    # Make creator (user.id) FK
    op.create_foreign_key(
        "pois_users_fk",
        source_table="pois",
        referent_table="users",
        local_cols=["creator"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )
    pass


def downgrade():
    op.drop_constraint("pois_users_fk", table_name="pois")
    op.drop_column("pois", "creator")
    op.drop_table("users")
    op.drop_column("pois", "description")
    op.drop_column("pois", "lat")
    op.drop_column("pois", "lng")
    op.drop_column("pois", "category")
    op.drop_column("pois", "published")
    op.drop_column("pois", "created_at")
    pass
