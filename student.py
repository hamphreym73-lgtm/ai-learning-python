import json


def load_students():

    try:
        with open(
            "data1/students.json",
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except FileNotFoundError:

        return []


def save_students(students):

    with open(
        "data1/students.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            students,
            file,
            ensure_ascii=False,
            indent=4
        )


def show_students(students):

    for student in students:

        print(
            f'{student["name"]}：'
            f'{student["score"]}分'
        )