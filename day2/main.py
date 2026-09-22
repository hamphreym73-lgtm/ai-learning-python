from pathlib import Path

from models.student import Student
from services.student_manager import StudentManager


# =========================
# 数据文件路径
# =========================

BASE_DIR = Path(__file__).parent

DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(exist_ok=True)

DATA_FILE = DATA_DIR / "students.json"


# =========================
# 创建学生管理器
# =========================

manager = StudentManager()

# 启动程序时读取以前的数据
manager.load_from_file(DATA_FILE)


# =========================
# 主菜单
# =========================

while True:

    print("\n===== 学生管理系统 =====")
    print("1. 添加学生")
    print("2. 删除学生")
    print("3. 修改成绩")
    print("4. 查询学生")
    print("5. 显示所有学生")
    print("6. 查看平均分")
    print("0. 退出系统")

    choice = input("请输入操作：")


    # =====================
    # 1. 添加学生
    # =====================

    if choice == "1":

        name = input("请输入学生姓名：").strip()

        try:
            score = int(input("请输入学生成绩："))
        except ValueError:
            print("成绩必须输入数字")
            continue
        if score<0 or score>100:
            print("成绩必须0-100")
            continue

        student = Student(name, score)

        manager.add_student(student)

        manager.save_to_file(DATA_FILE)

        print("添加成功")


    # =====================
    # 2. 删除学生
    # =====================

    elif choice == "2":

        name = input("请输入要删除的学生姓名：")

        result = manager.delete_student(name)

        if result:
            manager.save_to_file(DATA_FILE)
            print("删除成功")
        else:
            print("没有找到该学生")


    # =====================
    # 3. 修改成绩
    # =====================

    elif choice == "3":

        name = input("请输入学生姓名：").strip()

        try:
            score = int(input("请输入新成绩："))
        except ValueError:
            print("成绩必须输入数字")
            continue
        if score<0 or score>100:
            print("成绩必须是数字在0-100")
            continue

        result = manager.update_student_score(name, score)

        if result:
            manager.save_to_file(DATA_FILE)
            print("修改成功")
        else:
            print("没有找到该学生")


    # =====================
    # 4. 查询学生
    # =====================

    elif choice == "4":

        name = input("请输入要查询的学生姓名：")

        student = manager.find_student(name)

        if student is not None:
            print("查询结果：", student)
        else:
            print("没有找到该学生")


    # =====================
    # 5. 显示所有学生
    # =====================

    elif choice == "5":

        if len(manager.students) == 0:
            print("当前没有学生")

        else:
            print("\n===== 所有学生 =====")

            for student in manager.students:
                print(student)


    # =====================
    # 6. 查看平均分
    # =====================

    elif choice == "6":

        average = manager.average_score()

        print("平均分：", average)


    # =====================
    # 0. 退出
    # =====================

    elif choice == "0":

        print("程序退出")
        break


    # =====================
    # 非法输入
    # =====================

    else:

        print("无效操作，请重新输入")