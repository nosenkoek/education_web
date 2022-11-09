import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Tuple, Type

from pandas import DataFrame, ExcelWriter

from django.db.models import QuerySet
from django.conf import settings

from app_education.models import Direction


COLUMNS = ['Direction', 'Curator', 'Disciplines', 'Num group', 'Females',
           'Males', 'Free places', 'Students']

path_to_file = os.path.join(settings.MEDIA_ROOT, 'reports',
                            'path_to_file.xlsx')


@dataclass
class DirectionData():
    """Датакласс с набором информации 1 направления"""
    direction_name: str
    curator_info: str
    disciplines: str
    group_num: str
    female_count: int
    male_count: int
    free_places: int
    students_info: QuerySet

    def get_row_as_tuple(self) -> Tuple[str, str, str, str,
                                        str, str, str, str]:
        if not self.students_info:
            yield (self.disciplines, self.curator_info, self.disciplines,
                   str(self.group_num), str(self.female_count),
                   str(self.male_count), str(self.free_places), '')

        for index, student in enumerate(self.students_info):
            if not index:
                yield (self.disciplines, self.curator_info, self.disciplines,
                       str(self.group_num), str(self.female_count),
                       str(self.male_count), str(self.free_places), student)
            yield '', '', '', '', '', '', '', student


class BaseData(ABC):
    @abstractmethod
    def get_data(self):
        pass


class DirectionDataAdapter(BaseData):
    """
    Адаптер для данных об направлении.
    Args:
        direction: объект Direction
    """
    def __init__(self, direction: Direction):
        self._direction = direction

    def _create_model(self) -> List[DirectionData]:
        """
        Создания модели и валидация данных.
        :return: список с моделями
        """
        disciplines = ', '.join([discipline.name
                                 for discipline in
                                 self._direction.discipline.all()])
        direction_name = self._direction.name
        curator_info = self._direction.curator_fk.username

        data = []

        for class_cur in self._direction.class_set.all():
            group_num = class_cur.number
            female_count = class_cur.count_female(),
            male_count = class_cur.count_male(),
            free_places = class_cur.free_place(),

            direction_data = DirectionData(
                direction_name=direction_name,
                curator_info=curator_info,
                disciplines=disciplines,
                group_num=group_num,
                female_count=female_count[0],
                male_count=male_count[0],
                free_places=free_places[0],
                students_info=class_cur.student_set.all()
            )
            data.append(direction_data)
        return data

    def get_data(self) -> List[str]:
        """Возвращает строки с данными об направлении"""
        groups_data = self._create_model()
        rows = []
        for group_data in groups_data:
            rows.extend([row for row in group_data.get_row_as_tuple()])
        return rows


class DirectionHandler():
    """
    Фасад, реализующий обработку данных в вид, необходимый для записи
    Args:
        direction: Direction объект направления,
        adapter_cls: класс адаптер, трансформирующий данные из БД
        в построчный формат
    """

    def __init__(self, direction: Direction,
                 adapter_cls: Type[DirectionDataAdapter]):
        self._direction = direction
        self._adapter_cls = adapter_cls

    def get_rows_direction(self) -> List[str]:
        adapter = self._adapter_cls(self._direction)
        return adapter.get_data()


class ReportHandler():
    """
    Объект для создания отчета. Внешний интерфейс.
    Args:
        directions: QuerySet направлений,
    """
    def __init__(self, directions: QuerySet):
        self._directions = directions

    def create_report(self):
        """Создание отчета"""
        data = []

        for direction in self._directions:
            directions_handler = DirectionHandler(direction,
                                                  DirectionDataAdapter)
            rows = directions_handler.get_rows_direction()
            # TODO: необходима запись пакетами
            data.extend(rows)

        df = DataFrame(data, columns=COLUMNS)

        with ExcelWriter(path_to_file) as writer:
            df.to_excel(writer)
