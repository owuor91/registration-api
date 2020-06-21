"""add student_course relationship

Revision ID: e351b02aa3d4
Revises: b40fa0180116
Create Date: 2020-06-21 21:41:11.311791

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e351b02aa3d4'
down_revision = 'b40fa0180116'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('student_courses',
                    sa.Column('student_course_id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('student_id', postgresql.UUID(as_uuid=True), nullable=True),
                    sa.Column('course_id', postgresql.UUID(as_uuid=True), nullable=True),
                    sa.ForeignKeyConstraint(['course_id'], ['courses.course_id'], ),
                    sa.ForeignKeyConstraint(['student_id'], ['students.student_id'], ),
                    sa.PrimaryKeyConstraint('student_course_id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('student_courses')
    # ### end Alembic commands ###
