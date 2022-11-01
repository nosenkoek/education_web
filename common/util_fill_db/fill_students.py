import random
import uuid
from abc import ABC
from dataclasses import dataclass, astuple

from datetime import datetime
from typing import List, Dict

import psycopg2
from faker import Faker
from psycopg2.extras import execute_batch
from psycopg2.extensions import cursor

from common.util_fill_db.settings import COUNT_STUDENT, DSN, PAGE_SIZE


@dataclass
class Student():
    id: str
    first_name: str
    last_name: str
    patronymic: str
    email: str
    tel_number: str
    gender: str
    direction_fk: str


class DirectionDataHandler():
    """Обработчик процесса получения данных и формирования объекта.
    Внешний интерфейс"""

    def __init__(self, cur: cursor) -> None:
        self.cur = cur

    def __call__(self) -> List[str]:
        query = 'SELECT (id) FROM direction'
        self.cur.execute(query)
        direction_ids = [direction[0] for direction in self.cur]
        return direction_ids


class StudentLoadDataHandler():
    """Обработчик процесса заполнения БД фейковыми данными
    Внешний интерфейс"""

    def __init__(self, cur: cursor, direction_ids):
        self.cur = cur
        self.data = direction_ids

    def __call__(self) -> None:
        query = 'INSERT INTO student ' \
                '(id, first_name, last_name, patronymic, email, ' \
                'tel_number, gender, direction_fk) ' \
                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'

        students = []
        for _ in range(COUNT_STUDENT):
            students.append(
                Student(id=str(uuid.uuid4()),
                        first_name=fake.first_name(),
                        last_name=fake.last_name(),
                        patronymic=fake.last_name(),
                        email=fake.email(),
                        tel_number=str(random.randint(10 ** 9, 10 ** 10)),
                        gender=random.choice(['female', 'male']),
                        direction_fk=random.choice(self.data))
            )

        data_student = [astuple(student) for student in students]
        execute_batch(self.cur, query, data_student,
                      page_size=PAGE_SIZE)


if __name__ == '__main__':
    fake = Faker()
    now = datetime.now()

    with psycopg2.connect(**DSN) as conn, conn.cursor() as curs:
        download_handler = DirectionDataHandler(curs)
        direction_data = download_handler()

        load_handler = StudentLoadDataHandler(curs, direction_data)
        load_handler()
