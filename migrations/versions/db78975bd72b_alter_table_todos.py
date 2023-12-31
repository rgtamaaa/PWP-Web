"""Alter table Todos

Revision ID: db78975bd72b
Revises: 2745df4d1d11
Create Date: 2023-12-28 08:35:36.366943

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db78975bd72b'
down_revision = '2745df4d1d11'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('todos',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('todo', sa.String(length=140), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('todos', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_todos_created_at'), ['created_at'], unique=False)
        batch_op.create_index(batch_op.f('ix_todos_updated_at'), ['updated_at'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('todos', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_todos_updated_at'))
        batch_op.drop_index(batch_op.f('ix_todos_created_at'))

    op.drop_table('todos')
    # ### end Alembic commands ###
