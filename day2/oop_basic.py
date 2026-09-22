import json
from pathlib import Path


# =========================
# Student 学生类
# =========================
class Student:

    def __init__(self, name, score):
        self.name = name
        self.score = score

    # 显示学生信息
    def show_info(self):
        print("name:", self.name)
        print("score:", self.score)

    # 修改成绩
    def update_score(self, score):
        if 0 <= score <= 100:
            self.score = score
        else:
            print("成绩必须在0-100之间")

    # 判断是否及格
    def is_passed(self):
        return self.score >= 60

    # print(student) 时显示的内容
    def __str__(self):
        return f"name:{self.name},{self.score}分"

    # Student对象 → 字典
    def to_dict(self):
        return {
            "name": self.name,
            "score": self.score
        }

    # 字典 → Student对象
    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["score"])


# =========================
# StudentManager 学生管理类
# =========================
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

    # 修改学生成绩
    def update_student_score(self, name, score):

        student = self.find_student(name)

        if student is not None:
            student.update_score(score)
            return True

        return False

    # 计算平均分
    def average_score(self):

        if len(self.students) == 0:
            return 0

        total = 0

        for student in self.students:
            total += student.score

        return total / len(self.students)

    # 保存学生数据到JSON
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

    # 从JSON读取学生数据
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


# =========================
# 程序运行部分
# =========================

# 当前Python文件所在目录：
# D:\PythonProject4\day2
BASE_DIR = Path(__file__).parent

# data2文件夹
DATA_DIR = BASE_DIR / "data2"

# 如果data2不存在，自动创建
DATA_DIR.mkdir(exist_ok=True)

# JSON文件完整路径
DATA_FILE = DATA_DIR / "students.json"


# 创建学生管理器
manager = StudentManager()


# =========================
# 添加学生
# =========================

manager.add_student(Student("张三", 90))
manager.add_student(Student("李四", 85))
manager.add_student(Student("王五", 95))


print("===== 所有学生 =====")

for student in manager.students:
    print(student)


# =========================
# 查询学生
# =========================

result = manager.find_student("李四")

print("\n===== 查询结果 =====")
print(result)


# =========================
# 修改成绩
# =========================

manager.update_student_score("张三", 100)

print("\n===== 修改后 =====")

for student in manager.students:
    print(student)


# =========================
# 计算平均分
# =========================

print("\n===== 平均分 =====")

print(manager.average_score())


# =========================
# 删除学生
# =========================

manager.delete_student("李四")

print("\n===== 删除李四后 =====")

for student in manager.students:
    print(student)


# =========================
# 保存JSON
# =========================

manager.save_to_file(DATA_FILE)

print("\n数据保存成功！")
print("保存位置：", DATA_FILE)


# =========================
# 测试从JSON重新读取
# =========================

manager2 = StudentManager()

manager2.load_from_file(DATA_FILE)

print("\n===== 从JSON重新读取 =====")

for student in manager2.students:
    print(student)