"""add attendance

Revision ID: 9d8b2f1e4a76
Revises: 659d237ebfa5
Create Date: 2026-04-28 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "9d8b2f1e4a76"
down_revision = "659d237ebfa5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if inspector.has_table("attendances"):
        return

    op.create_table(
        "attendances",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("student_id", sa.Integer(), nullable=False),
        sa.Column("attendance_date", sa.Date(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("remarks", sa.String(length=300), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["student_id"], ["students.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("student_id", "attendance_date", name="uq_attendance_student_date"),
    )
    op.create_index(op.f("ix_attendances_id"), "attendances", ["id"], unique=False)
    op.create_index(op.f("ix_attendances_student_id"), "attendances", ["student_id"], unique=False)
    op.create_index(op.f("ix_attendances_attendance_date"), "attendances", ["attendance_date"], unique=False)
    op.create_index(op.f("ix_attendances_status"), "attendances", ["status"], unique=False)


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if not inspector.has_table("attendances"):
        return

    op.drop_index(op.f("ix_attendances_status"), table_name="attendances")
    op.drop_index(op.f("ix_attendances_attendance_date"), table_name="attendances")
    op.drop_index(op.f("ix_attendances_student_id"), table_name="attendances")
    op.drop_index(op.f("ix_attendances_id"), table_name="attendances")
    op.drop_table("attendances")
