from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from passlib.hash import bcrypt

revision = "0e9bca78f8fe"
down_revision = "c19564ab1904"

def upgrade():
    users_table = table(
        "users",
        column("email", sa.String),
        column("hashed_password", sa.String),
    )

    # Hash de contraseña admin
    admin_password = bcrypt.hash("admin")

    op.bulk_insert(
        users_table,
        [
            {
                "email": "admin@task.com",
                "hashed_password": admin_password,
            }
        ]
    )

def downgrade():
    op.execute("DELETE FROM users WHERE email = 'admin@task.com'")
