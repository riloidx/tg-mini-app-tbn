"""insert_question_options

Revision ID: 003
Revises: 002
Create Date: 2024-01-01 00:00:02.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '003'
down_revision: Union[str, None] = '002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Insert question options
    connection = op.get_bind()
    
    # Options for questions 1-2 (Да/Не полн/Нет)
    for q_num in [1, 2, 16, 31, 32, 42]:
        result = connection.execute(sa.text(f"SELECT id FROM questions WHERE number = {q_num}"))
        q_id = result.fetchone()[0]
        
        if q_num == 1:
            options = [('Да', 2, 1), ('Не полн', 1, 2), ('Нет', 0, 3)]
        elif q_num == 2:
            options = [('Да', 3, 1), ('Не полн', 1, 2), ('Нет', 0, 3)]
        elif q_num == 16:
            options = [('Да', 2, 1), ('Не полн', 1, 2), ('Нет', 0, 3)]
        elif q_num == 31:
            options = [('Да', 2, 1), ('Не полн', 1, 2), ('Нет', 0, 3)]
        elif q_num == 32:
            options = [('Да', 2, 1), ('Нет', 0, 2)]
        elif q_num == 42:
            options = [('Да', 2, 1), ('Не полн', 1, 2), ('Нет', 0, 3)]
        
        for label, points, sort_idx in options:
            connection.execute(sa.text(
                "INSERT INTO question_options (question_id, label, points, sort_index) "
                f"VALUES ({q_id}, '{label}', {points}, {sort_idx})"
            ))
    
    # Options for simple Да/Нет questions (most questions)
    simple_questions = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 33, 34, 35, 36, 37, 38, 39, 40]
    
    for q_num in simple_questions:
        result = connection.execute(sa.text(f"SELECT id FROM questions WHERE number = {q_num}"))
        q_id = result.fetchone()[0]
        
        options = [('Да', 1, 1), ('Нет', 0, 2)]
        
        for label, points, sort_idx in options:
            connection.execute(sa.text(
                "INSERT INTO question_options (question_id, label, points, sort_index) "
                f"VALUES ({q_id}, '{label}', {points}, {sort_idx})"
            ))
    
    # Question 41 (business ownership)
    result = connection.execute(sa.text("SELECT id FROM questions WHERE number = 41"))
    q_id = result.fetchone()[0]
    options = [('Да', 2, 1), ('Нет', 0, 2)]
    for label, points, sort_idx in options:
        connection.execute(sa.text(
            "INSERT INTO question_options (question_id, label, points, sort_index) "
            f"VALUES ({q_id}, '{label}', {points}, {sort_idx})"
        ))
    
    # Question 43 (investment capital)
    result = connection.execute(sa.text("SELECT id FROM questions WHERE number = 43"))
    q_id = result.fetchone()[0]
    options = [
        ('До 100 000 руб.', 0, 1),
        ('От 100 000 до 1 000 000 руб.', 2, 2),
        ('От 1 000 000 до 3 000 000 руб.', 4, 3),
        ('От 3 000 000 до 10 000 000 руб.', 6, 4),
        ('От 10 000 000 до 50 000 000 руб.', 8, 5),
        ('От 50 000 000 до 100 000 000 руб.', 10, 6)
    ]
    for label, points, sort_idx in options:
        connection.execute(sa.text(
            "INSERT INTO question_options (question_id, label, points, sort_index) "
            f"VALUES ({q_id}, '{label}', {points}, {sort_idx})"
        ))
    
    # Question 44 (environment level)
    result = connection.execute(sa.text("SELECT id FROM questions WHERE number = 44"))
    q_id = result.fetchone()[0]
    options = [
        ('Слабое окружение', 0, 1),
        ('На вашем уровне', 5, 2),
        ('Сильное окружение', 10, 3)
    ]
    for label, points, sort_idx in options:
        connection.execute(sa.text(
            "INSERT INTO question_options (question_id, label, points, sort_index) "
            f"VALUES ({q_id}, '{label}', {points}, {sort_idx})"
        ))
    
    # Questions 45-46 (active/passive income)
    for q_num in [45, 46]:
        result = connection.execute(sa.text(f"SELECT id FROM questions WHERE number = {q_num}"))
        q_id = result.fetchone()[0]
        options = [
            ('До 10 000 руб./мес.', 0, 1),
            ('От 10 000 до 50 000 руб./мес.', 2, 2),
            ('От 50 000 до 100 000 руб./мес.', 4, 3),
            ('От 100 000 до 300 000 руб./мес.', 6, 4),
            ('От 300 000 до 1 000 000 руб./мес.', 8, 5),
            ('От 1 000 000 руб./мес.', 10, 6)
        ]
        for label, points, sort_idx in options:
            connection.execute(sa.text(
                "INSERT INTO question_options (question_id, label, points, sort_index) "
                f"VALUES ({q_id}, '{label}', {points}, {sort_idx})"
            ))
    
    # Questions 47-51 (freedom questions)
    for q_num in [47, 48, 49, 50, 51]:
        result = connection.execute(sa.text(f"SELECT id FROM questions WHERE number = {q_num}"))
        q_id = result.fetchone()[0]
        options = [('Да', 2, 1), ('Нет', 0, 2)]
        for label, points, sort_idx in options:
            connection.execute(sa.text(
                "INSERT INTO question_options (question_id, label, points, sort_index) "
                f"VALUES ({q_id}, '{label}', {points}, {sort_idx})"
            ))


def downgrade() -> None:
    op.execute("DELETE FROM question_options")