# -*- coding: utf-8 -*-
"""
教务管理系统主类 - 业务逻辑 + 控制台菜单
"""

from database import Database
from models import Student, Course, Grade


class AdminSystem:
    """教务管理系统主控类"""

    def __init__(self):
        self.db = Database()

    # ========== 主菜单 ==========
    def show_main_menu(self):
        print("\n" + "=" * 50)
        print("          教 务 管 理 系 统")
        print("=" * 50)
        print("  1. 学生信息管理")
        print("  2. 课程信息管理")
        print("  3. 成绩管理")
        print("  4. 统计查询")
        print("  0. 退出系统")
        print("=" * 50)

    # ========== 学生管理子菜单 ==========
    def student_menu(self):
        while True:
            print("\n----- 学生信息管理 -----")
            print("1. 添加学生")
            print("2. 删除学生")
            print("3. 修改学生信息")
            print("4. 查询学生（按学号）")
            print("5. 查看所有学生")
            print("0. 返回主菜单")
            choice = input("请选择：").strip()

            if choice == '1':
                self.add_student()
            elif choice == '2':
                self.delete_student()
            elif choice == '3':
                self.update_student()
            elif choice == '4':
                self.query_student()
            elif choice == '5':
                self.list_all_students()
            elif choice == '0':
                break
            else:
                print("输入有误，请重新选择！")

    def add_student(self):
        print("\n【添加学生】")
        stu_id = input("学号：").strip()
        if not stu_id:
            print("学号不能为空！")
            return
        # 检查是否已存在
        if self.db.query_one("SELECT stu_id FROM student WHERE stu_id=%s", stu_id):
            print("该学号已存在！")
            return

        name = input("姓名：").strip()
        if not name:
            print("姓名不能为空！")
            return
        gender = input("性别（男/女）：").strip() or None
        age = input("年龄：").strip()
        age = int(age) if age.isdigit() else None
        major = input("专业：").strip() or None
        class_name = input("班级：").strip() or None
        phone = input("联系电话：").strip() or None

        sql = ("INSERT INTO student (stu_id, name, gender, age, major, class_name, phone) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s)")
        result = self.db.execute(sql, (stu_id, name, gender, age, major, class_name, phone))
        if result:
            print("添加成功！")
        else:
            print("添加失败！")

    def delete_student(self):
        print("\n【删除学生】")
        stu_id = input("请输入要删除的学号：").strip()
        if not self.db.query_one("SELECT stu_id FROM student WHERE stu_id=%s", stu_id):
            print("该学生不存在！")
            return
        confirm = input(f"确认删除学号为 {stu_id} 的学生吗？(y/n)：").strip().lower()
        if confirm == 'y':
            result = self.db.execute("DELETE FROM student WHERE stu_id=%s", stu_id)
            print("删除成功！" if result else "删除失败！")

    def update_student(self):
        print("\n【修改学生信息】")
        stu_id = input("请输入要修改的学号：").strip()
        row = self.db.query_one("SELECT * FROM student WHERE stu_id=%s", stu_id)
        if not row:
            print("该学生不存在！")
            return
        print(f"当前信息：{Student(**row)}")
        print("（直接回车表示不修改）")

        name = input(f"姓名[{row['name']}]：").strip() or row['name']
        gender = input(f"性别[{row['gender'] or '—'}]：").strip() or row['gender']
        age_input = input(f"年龄[{row['age'] or '—'}]：").strip()
        age = int(age_input) if age_input.isdigit() else row['age']
        major = input(f"专业[{row['major'] or '—'}]：").strip() or row['major']
        class_name = input(f"班级[{row['class_name'] or '—'}]：").strip() or row['class_name']
        phone = input(f"电话[{row['phone'] or '—'}]：").strip() or row['phone']

        sql = ("UPDATE student SET name=%s, gender=%s, age=%s, "
               "major=%s, class_name=%s, phone=%s WHERE stu_id=%s")
        result = self.db.execute(sql, (name, gender, age, major, class_name, phone, stu_id))
        print("修改成功！" if result else "修改失败！")

    def query_student(self):
        print("\n【查询学生】")
        stu_id = input("请输入学号：").strip()
        row = self.db.query_one("SELECT * FROM student WHERE stu_id=%s", stu_id)
        if row:
            print(Student(**row))
        else:
            print("未找到该学生！")

    def list_all_students(self):
        print("\n【所有学生列表】")
        rows = self.db.query_all("SELECT * FROM student ORDER BY stu_id")
        if not rows:
            print("暂无学生数据。")
            return
        for i, row in enumerate(rows, 1):
            print(f"{i}. {Student(**row)}")
        print(f"共 {len(rows)} 名学生。")

    # ========== 课程管理子菜单 ==========
    def course_menu(self):
        while True:
            print("\n----- 课程信息管理 -----")
            print("1. 添加课程")
            print("2. 删除课程")
            print("3. 修改课程信息")
            print("4. 查询课程（按课程号）")
            print("5. 查看所有课程")
            print("0. 返回主菜单")
            choice = input("请选择：").strip()

            if choice == '1':
                self.add_course()
            elif choice == '2':
                self.delete_course()
            elif choice == '3':
                self.update_course()
            elif choice == '4':
                self.query_course()
            elif choice == '5':
                self.list_all_courses()
            elif choice == '0':
                break
            else:
                print("输入有误，请重新选择！")

    def add_course(self):
        print("\n【添加课程】")
        course_id = input("课程号：").strip()
        if not course_id:
            print("课程号不能为空！")
            return
        if self.db.query_one("SELECT course_id FROM course WHERE course_id=%s", course_id):
            print("该课程号已存在！")
            return

        course_name = input("课程名：").strip()
        if not course_name:
            print("课程名不能为空！")
            return
        credit_input = input("学分：").strip()
        credit = float(credit_input) if credit_input else None
        teacher = input("授课教师：").strip() or None
        semester = input("学期（如 2025-2026-2）：").strip() or None

        sql = ("INSERT INTO course (course_id, course_name, credit, teacher, semester) "
               "VALUES (%s, %s, %s, %s, %s)")
        result = self.db.execute(sql, (course_id, course_name, credit, teacher, semester))
        print("添加成功！" if result else "添加失败！")

    def delete_course(self):
        print("\n【删除课程】")
        course_id = input("请输入要删除的课程号：").strip()
        if not self.db.query_one("SELECT course_id FROM course WHERE course_id=%s", course_id):
            print("该课程不存在！")
            return
        confirm = input(f"确认删除课程号 {course_id} 吗？(y/n)：").strip().lower()
        if confirm == 'y':
            result = self.db.execute("DELETE FROM course WHERE course_id=%s", course_id)
            print("删除成功！" if result else "删除失败！")

    def update_course(self):
        print("\n【修改课程信息】")
        course_id = input("请输入要修改的课程号：").strip()
        row = self.db.query_one("SELECT * FROM course WHERE course_id=%s", course_id)
        if not row:
            print("该课程不存在！")
            return
        print(f"当前信息：{Course(**row)}")
        print("（直接回车表示不修改）")

        course_name = input(f"课程名[{row['course_name']}]：").strip() or row['course_name']
        credit_input = input(f"学分[{row['credit'] or '—'}]：").strip()
        credit = float(credit_input) if credit_input else row['credit']
        teacher = input(f"教师[{row['teacher'] or '—'}]：").strip() or row['teacher']
        semester = input(f"学期[{row['semester'] or '—'}]：").strip() or row['semester']

        sql = ("UPDATE course SET course_name=%s, credit=%s, teacher=%s, semester=%s "
               "WHERE course_id=%s")
        result = self.db.execute(sql, (course_name, credit, teacher, semester, course_id))
        print("修改成功！" if result else "修改失败！")

    def query_course(self):
        print("\n【查询课程】")
        keyword = input("请输入课程号或课程名关键字：").strip()
        rows = self.db.query_all(
            "SELECT * FROM course WHERE course_id LIKE %s OR course_name LIKE %s",
            (f'%{keyword}%', f'%{keyword}%')
        )
        if rows:
            for row in rows:
                print(Course(**row))
        else:
            print("未找到匹配的课程！")

    def list_all_courses(self):
        print("\n【所有课程列表】")
        rows = self.db.query_all("SELECT * FROM course ORDER BY course_id")
        if not rows:
            print("暂无课程数据。")
            return
        for i, row in enumerate(rows, 1):
            print(f"{i}. {Course(**row)}")
        print(f"共 {len(rows)} 门课程。")

    # ========== 成绩管理子菜单 ==========
    def grade_menu(self):
        while True:
            print("\n----- 成绩管理 -----")
            print("1. 录入成绩")
            print("2. 修改成绩")
            print("3. 删除成绩记录")
            print("4. 按学生查询成绩")
            print("5. 按课程查询成绩")
            print("0. 返回主菜单")
            choice = input("请选择：").strip()

            if choice == '1':
                self.add_grade()
            elif choice == '2':
                self.update_grade()
            elif choice == '3':
                self.delete_grade()
            elif choice == '4':
                self.query_grade_by_student()
            elif choice == '5':
                self.query_grade_by_course()
            elif choice == '0':
                break
            else:
                print("输入有误，请重新选择！")

    def add_grade(self):
        print("\n【录入成绩】")
        stu_id = input("学号：").strip()
        if not self.db.query_one("SELECT stu_id FROM student WHERE stu_id=%s", stu_id):
            print("该学生不存在！")
            return
        course_id = input("课程号：").strip()
        if not self.db.query_one("SELECT course_id FROM course WHERE course_id=%s", course_id):
            print("该课程不存在！")
            return
        # 检查是否已录入
        if self.db.query_one(
            "SELECT id FROM grade WHERE stu_id=%s AND course_id=%s", (stu_id, course_id)
        ):
            print("该学生此课程成绩已存在，请使用【修改成绩】功能！")
            return

        score_input = input("成绩：").strip()
        score = float(score_input) if score_input else None

        result = self.db.execute(
            "INSERT INTO grade (stu_id, course_id, score) VALUES (%s, %s, %s)",
            (stu_id, course_id, score)
        )
        print("录入成功！" if result else "录入失败！")

    def update_grade(self):
        print("\n【修改成绩】")
        stu_id = input("学号：").strip()
        course_id = input("课程号：").strip()
        row = self.db.query_one(
            "SELECT * FROM grade WHERE stu_id=%s AND course_id=%s", (stu_id, course_id)
        )
        if not row:
            print("该成绩记录不存在！")
            return
        print(f"当前成绩：{row['score'] if row['score'] is not None else '未录入'}")
        score_input = input("新成绩：").strip()
        score = float(score_input) if score_input else None

        result = self.db.execute(
            "UPDATE grade SET score=%s WHERE stu_id=%s AND course_id=%s",
            (score, stu_id, course_id)
        )
        print("修改成功！" if result else "修改失败！")

    def delete_grade(self):
        print("\n【删除成绩记录】")
        stu_id = input("学号：").strip()
        course_id = input("课程号：").strip()
        if not self.db.query_one(
            "SELECT id FROM grade WHERE stu_id=%s AND course_id=%s", (stu_id, course_id)
        ):
            print("该成绩记录不存在！")
            return
        confirm = input("确认删除该成绩记录吗？(y/n)：").strip().lower()
        if confirm == 'y':
            result = self.db.execute(
                "DELETE FROM grade WHERE stu_id=%s AND course_id=%s", (stu_id, course_id)
            )
            print("删除成功！" if result else "删除失败！")

    def query_grade_by_student(self):
        print("\n【按学生查询成绩】")
        stu_id = input("请输入学号：").strip()
        stu_row = self.db.query_one("SELECT name FROM student WHERE stu_id=%s", stu_id)
        if not stu_row:
            print("该学生不存在！")
            return
        sql = ("SELECT g.stu_id, g.course_id, g.score, c.course_name "
               "FROM grade g JOIN course c ON g.course_id = c.course_id "
               "WHERE g.stu_id=%s ORDER BY g.course_id")
        rows = self.db.query_all(sql, stu_id)
        if not rows:
            print("该学生暂无成绩记录。")
            return
        print(f"\n学生：{stu_row['name']}（{stu_id}）的成绩单：")
        total = 0
        count = 0
        for row in rows:
            print(f"  {row['course_name']}（{row['course_id']}）："
                  f"{row['score'] if row['score'] is not None else '未录入'}")
            if row['score'] is not None:
                total += row['score']
                count += 1
        if count > 0:
            print(f"  平均分：{total / count:.2f}")

    def query_grade_by_course(self):
        print("\n【按课程查询成绩】")
        course_id = input("请输入课程号：").strip()
        course_row = self.db.query_one(
            "SELECT course_name FROM course WHERE course_id=%s", course_id
        )
        if not course_row:
            print("该课程不存在！")
            return
        sql = ("SELECT g.stu_id, g.course_id, g.score, s.name as stu_name "
               "FROM grade g JOIN student s ON g.stu_id = s.stu_id "
               "WHERE g.course_id=%s ORDER BY g.score DESC")
        rows = self.db.query_all(sql, course_id)
        if not rows:
            print("该课程暂无成绩记录。")
            return
        print(f"\n课程：{course_row['course_name']}（{course_id}）的成绩表：")
        for i, row in enumerate(rows, 1):
            print(f"  第{i}名 {row['stu_name']}（{row['stu_id']}）："
                  f"{row['score'] if row['score'] is not None else '未录入'}")

    # ========== 统计查询子菜单 ==========
    def stats_menu(self):
        while True:
            print("\n----- 统计查询 -----")
            print("1. 学生总数统计")
            print("2. 课程总数统计")
            print("3. 各班学生人数")
            print("4. 各专业学生人数")
            print("5. 某门课程成绩分布")
            print("0. 返回主菜单")
            choice = input("请选择：").strip()

            if choice == '1':
                self.stat_student_count()
            elif choice == '2':
                self.stat_course_count()
            elif choice == '3':
                self.stat_by_class()
            elif choice == '4':
                self.stat_by_major()
            elif choice == '5':
                self.stat_course_distribution()
            elif choice == '0':
                break
            else:
                print("输入有误，请重新选择！")

    def stat_student_count(self):
        row = self.db.query_one("SELECT COUNT(*) as cnt FROM student")
        print(f"\n学生总数：{row['cnt']} 人")

    def stat_course_count(self):
        row = self.db.query_one("SELECT COUNT(*) as cnt FROM course")
        print(f"\n课程总数：{row['cnt']} 门")

    def stat_by_class(self):
        rows = self.db.query_all(
            "SELECT class_name, COUNT(*) as cnt FROM student "
            "WHERE class_name IS NOT NULL GROUP BY class_name ORDER BY class_name"
        )
        if not rows:
            print("\n暂无数据。")
            return
        print("\n【各班学生人数】")
        for row in rows:
            print(f"  {row['class_name']}：{row['cnt']} 人")

    def stat_by_major(self):
        rows = self.db.query_all(
            "SELECT major, COUNT(*) as cnt FROM student "
            "WHERE major IS NOT NULL GROUP BY major ORDER BY major"
        )
        if not rows:
            print("\n暂无数据。")
            return
        print("\n【各专业学生人数】")
        for row in rows:
            print(f"  {row['major']}：{row['cnt']} 人")

    def stat_course_distribution(self):
        course_id = input("\n请输入课程号：").strip()
        course_row = self.db.query_one(
            "SELECT course_name FROM course WHERE course_id=%s", course_id
        )
        if not course_row:
            print("该课程不存在！")
            return

        # 统计各分数段
        ranges = [
            ("优秀 (90-100)", 90, 100),
            ("良好 (80-89)", 80, 89.9),
            ("中等 (70-79)", 70, 79.9),
            ("及格 (60-69)", 60, 69.9),
            ("不及格 (<60)", 0, 59.9),
        ]
        print(f"\n【{course_row['course_name']} 成绩分布】")
        total_pass = 0
        total_count = 0
        for label, low, high in ranges:
            row = self.db.query_one(
                "SELECT COUNT(*) as cnt FROM grade "
                "WHERE course_id=%s AND score BETWEEN %s AND %s",
                (course_id, low, high)
            )
            cnt = row['cnt']
            total_count += cnt
            if low >= 60:
                total_pass += cnt
            print(f"  {label}：{cnt} 人")

        if total_count > 0:
            print(f"\n  总人数：{total_count} 人")
            print(f"  及格率：{total_pass / total_count * 100:.2f}%")

    # ========== 运行入口 ==========
    def run(self):
        while True:
            self.show_main_menu()
            choice = input("请输入选项：").strip()
            if choice == '1':
                self.student_menu()
            elif choice == '2':
                self.course_menu()
            elif choice == '3':
                self.grade_menu()
            elif choice == '4':
                self.stats_menu()
            elif choice == '0':
                print("\n感谢使用教务管理系统，再见！")
                self.db.close()
                break
            else:
                print("输入有误，请重新选择！")
