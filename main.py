import os

from config import (ADD_TEXT, DIR_NAME, STATE_FILE, TEMP_FILE_1, TEMP_FILE_2,
                    TEST_TEXT, TEST_URL)
from job import Job
from scheduler import Scheduler
from tasks import (append_to_file, create_directory, create_file,
                   create_file_and_write, get_data_from_url, read_file,
                   remove_directory, remove_file)


def main():
    """Главная функция."""

    scheduler = Scheduler(max_tasks=10)

    if os.path.isfile(STATE_FILE):
        scheduler.load_state(STATE_FILE)

    task1 = Job(
        task_id=1,
        duration=5,
        func=create_directory,
        directory_name=DIR_NAME,
    )
    task2 = Job(
        task_id=2,
        duration=3,
        dependencies=[task1],
        func=create_file_and_write,
        filename=f"{DIR_NAME}/{TEMP_FILE_1}",
        content=TEST_TEXT,
    )
    task3 = Job(
        task_id=3,
        duration=1,
        dependencies=[task1, task2],
        start_time=4,
        restarts=1,
        func=read_file,
        filename=f"{DIR_NAME}/{TEMP_FILE_1}",
    )
    task4 = Job(
        task_id=4,
        duration=1,
        dependencies=[task1],
        start_time=4,
        restarts=1,
        func=create_file,
        filename=f"{DIR_NAME}/{TEMP_FILE_2}",
    )
    task5 = Job(
        task_id=5,
        duration=3,
        dependencies=[task1, task2],
        func=append_to_file,
        filename=f"{DIR_NAME}/{TEMP_FILE_1}",
        additional_content=ADD_TEXT,
    )
    task6 = Job(
        task_id=6,
        duration=1,
        dependencies=[task1, task2, task3, task5],
        start_time=4,
        restarts=1,
        func=remove_file,
        filename=f"{DIR_NAME}/{TEMP_FILE_1}",
    )
    task7 = Job(
        task_id=7,
        duration=1,
        dependencies=[task1, task4],
        start_time=4,
        restarts=1,
        func=remove_file,
        filename=f"{DIR_NAME}/{TEMP_FILE_2}",
    )
    task8 = Job(
        task_id=8,
        duration=1,
        dependencies=[task6, task7],
        start_time=4,
        restarts=1,
        func=remove_directory,
        directory_name=DIR_NAME,
    )
    task9 = Job(
        task_id=9,
        func=get_data_from_url,
        url=TEST_URL,
    )

    scheduler.add_task(task1)
    scheduler.add_task(task2)
    scheduler.add_task(task3)
    scheduler.add_task(task4)
    scheduler.add_task(task5)
    scheduler.add_task(task6)
    scheduler.add_task(task7)
    scheduler.add_task(task8)
    scheduler.add_task(task9)

    scheduler.execute_tasks()
    scheduler.save_state(STATE_FILE)


if __name__ == "__main__":
    main()
