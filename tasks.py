import os
from http import HTTPStatus
from pathlib import Path
from typing import Generator

import requests

from logger import logger


def create_directory(directory_name: str) -> Generator:
    """Создает директорию."""
    Path(directory_name).mkdir(exist_ok=True)
    logger.info("Directory %s created", directory_name)
    yield


def create_file_and_write(filename: str, content: str) -> Generator:
    """Создает файл и записывает в него содержимое."""
    with open(filename, "w") as file:
        file.write(content)
    logger.info("Created file %s. Content: '%s' writed", filename, content)
    yield


def read_file(filename: str) -> Generator:
    """Читает содержимое файла."""
    logger.info("Read file %s started", filename)
    with open(filename, "r") as file:
        content = file.read()
    logger.info("Read file %s finished. Content: '%s'", filename, content)
    yield


def append_to_file(filename: str, additional_content: str) -> Generator:
    """Дописывает содержимое в конец файла."""
    with open(filename, "a") as file:
        file.write(additional_content)
    logger.info(
        "Append to file %s. Content: '%s' writed",
        filename,
        additional_content,
    )
    yield


def remove_directory(directory_name: str) -> Generator:
    """Удаляет директорию."""
    os.rmdir(directory_name)
    logger.info("Directory %s removed", directory_name)
    yield


def remove_file(filename: str) -> Generator:
    """Удаляет файл."""
    os.remove(filename)
    logger.info("File %s removed", filename)
    yield


def create_file(filename: str) -> Generator:
    """Создает файл."""
    with open(filename, "w") as file:
        file.write('')
    logger.info("File %s created", filename)
    yield


def get_data_from_url(url: str) -> Generator:
    """Получает данные по url."""
    response = requests.get(url)
    if response.status_code == HTTPStatus.OK:
        data = response.text
        data = data[0:100]
        logger.info("Get data from url %s. Data: '%s'", url, data)
    else:
        logger.warning(
            "Unsuccessful get data from url %s. Status code: %s",
            url,
            response.status_code,
        )
    yield
