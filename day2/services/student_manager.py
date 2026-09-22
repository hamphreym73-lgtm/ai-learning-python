import json

from models.student import Student


class StudentManager:

    def __init__(self):
        self.students = []

    # 添加学生
    def add_student(self, student):
        self.students.append(student)

    # 查询学生
    def find_student(self, name):
        for student in self.students:
            if student.name == name:
                return student

        return None

    # 删除学生
    def delete_student(self, name):
        student = self.find_student(name)

        if student is not None:
            self.students.remove(student)
            return True

        return False

    # 修改成绩
    def update_student_score(self, name, score):
        student = self.find_student(name)

        if student is not None:
            return  student.update_score(score)


        return False

    # 计算平均分
    def average_score(self):
        if len(self.students) == 0:
            return 0

        total = 0

        for student in self.students:
            total += student.score

        return total / len(self.students)

    # 保存JSON
    def save_to_file(self, file_name):
        data = []

        for student in self.students:
            data.append(student.to_dict())

        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4
            )

    # 读取JSON
    def load_from_file(self, file_name):
        try:
            with open(file_name, "r", encoding="utf-8") as file:
                data = json.load(file)

            self.students = []

            for item in data:
                student = Student.from_dict(item)
                self.students.append(student)

        except FileNotFoundError:
            print("数据文件不存在，将使用空学生列表")
            self.students = []

        except json.JSONDecodeError:
            print("JSON文件格式错误")
            self.students = []