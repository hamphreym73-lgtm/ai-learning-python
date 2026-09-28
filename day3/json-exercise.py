import json
student = {
    "name": "小明",
    "age": 19,
    "score": 95
}

with open("data3.json","w",encoding="utf-8") as file:
    json.dump(
        student,
        file,
        ensure_ascii=False,
        indent=4
    )
with open("data3.json","r",encoding="utf-8") as file:
    group = json.load(file)

print(group)