"""create table

Revision ID: b9b0742b0f72
Revises: 
Create Date: 2025-05-03 22:53:15.074074

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'b9b0742b0f72'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('permission',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('permission_routes', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('permission_type', sa.Enum('ADMIN', 'GET', 'PUT', 'PATCH', 'DELETE', 'POST', name='permissiontype'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('project',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('role',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('user',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_unique_constraint('uq_user_email', 'user', ['email'])

    op.create_table('role_permission',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('permission_id', sa.Uuid(), nullable=False),
        sa.Column('role_id', sa.Uuid(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_foreign_key('fk_role_permission_permission_id', 'role_permission', 'permission', ['permission_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('fk_role_permission_role_id', 'role_permission', 'role', ['role_id'], ['id'], ondelete='CASCADE')
    op.create_unique_constraint('uq_role_permission_permission_id_role_id', 'role_permission', ['permission_id', 'role_id'])

    op.create_table('user_role',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('user_id', sa.Uuid(), nullable=False),
        sa.Column('role_id', sa.Uuid(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_foreign_key('fk_user_role_user_id', 'user_role', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('fk_user_role_role_id', 'user_role', 'role', ['role_id'], ['id'], ondelete='CASCADE')
    op.create_unique_constraint('uq_user_role_user_id_role_id', 'user_role', ['user_id', 'role_id'])

    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_role')
    op.drop_table('role_permission')
    op.drop_table('user')
    op.drop_table('role')
    op.drop_table('project')
    op.drop_table('permission')

    op.execute('DROP TYPE permissiontype')
    # ### end Alembic commands ###
