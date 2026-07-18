# -*- coding: utf-8 -*-
"""
初始化测试数据脚本 - 运行后会自动插入示例学生、课程和成绩
使用方法：python init_data.py
"""

from database import Database


def init_test_data():
    db = Database()

    # 插入示例学生
    students = [
        ('2023001', '张三', '男', 20, '软件工程', '软工2301', '13800138001'),
        ('2023002', '李四', '女', 19, '软件工程', '软工2301', '13800138002'),
        ('2023003', '王五', '男', 20, '软件工程', '软工2302', '13800138003'),
        ('2023004', '赵六', '女', 21, '计算机科学', '计科2301', '13800138004'),
        ('2023005', '孙七', '男', 19, '计算机科学', '计科2301', '13800138005'),
    ]
    for stu in students:
        db.execute(
            "INSERT IGNORE INTO student (stu_id, name, gender, age, major, class_name, phone) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)", stu
        )
    print(f"已插入 {len(students)} 条学生数据")

    # 插入示例课程
    courses = [
        ('C001', 'Python程序设计', 3.0, '刘老师', '2025-2026-2'),
        ('C002', '数据结构', 4.0, '陈老师', '2025-2026-2'),
        ('C003', '数据库原理', 3.5, '王老师', '2025-2026-2'),
        ('C004', '计算机网络', 3.0, '张老师', '2025-2026-2'),
    ]
    for course in courses:
        db.execute(
            "INSERT IGNORE INTO course (course_id, course_name, credit, teacher, semester) "
            "VALUES (%s, %s, %s, %s, %s)", course
        )
    print(f"已插入 {len(courses)} 条课程数据")

    # 插入示例成绩
    grades = [
        ('2023001', 'C001', 85.5),
        ('2023001', 'C002', 78.0),
        ('2023001', 'C003', 92.0),
        ('2023002', 'C001', 90.0),
        ('2023002', 'C002', 88.5),
        ('2023003', 'C001', 65.0),
        ('2023003', 'C003', 72.5),
        ('2023004', 'C001', 95.0),
        ('2023004', 'C002', 82.0),
        ('2023004', 'C004', 58.0),
        ('2023005', 'C002', 76.0),
    ]
    for grade in grades:
        db.execute(
            "INSERT IGNORE INTO grade (stu_id, course_id, score) VALUES (%s, %s, %s)", grade
        )
    print(f"已插入 {len(grades)} 条成绩数据")

    db.close()
    print("\n测试数据初始化完成！")


if __name__ == '__main__':
    init_test_data()
