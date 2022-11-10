from os import path
from os import walk
from typing import Optional

from app_report.services.settings import PATH_TO_REPORT_FILES


def get_path_file(file_name: str) -> Optional[str]:
    """
    Возвращает путь к файлу по его названию.
    :param file_name: название файла,
    :return: путь к файлу
    """
    catalog = walk(PATH_TO_REPORT_FILES)

    for address, dirs, files in catalog:
        if file_name in files:
            path_file = path.join(address, file_name)
            return path_file
    return None
