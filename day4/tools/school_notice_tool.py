from pathlib import Path
import json


BASE_DIR = Path(__file__).parent.parent

DATA_FILE = BASE_DIR / "data" / "notices.json"


def search_school_notices(keyword):

    with open(
        DATA_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        notices = json.load(file)


    results = []

    for notice in notices:

        if keyword in notice["title"] or keyword in notice["category"]:
            results.append(notice)


    return results


print(search_school_notices("奖学金"))