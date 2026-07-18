# -*- coding: utf-8 -*-
"""
实体类模块 - 学生、课程、成绩
"""


class Student:
    """学生实体类"""

    def __init__(self, stu_id, name, gender=None, age=None,
                 major=None, class_name=None, phone=None):
        self.stu_id = stu_id        # 学号
        self.name = name            # 姓名
        self.gender = gender        # 性别
        self.age = age              # 年龄
        self.major = major          # 专业
        self.class_name = class_name  # 班级
        self.phone = phone          # 联系电话

    def __str__(self):
        return (f"学号：{self.stu_id} | 姓名：{self.name} | 性别：{self.gender or '—'} | "
                f"年龄：{self.age or '—'} | 专业：{self.major or '—'} | "
                f"班级：{self.class_name or '—'} | 电话：{self.phone or '—'}")

    def to_dict(self):
        return {
            'stu_id': self.stu_id,
            'name': self.name,
            'gender': self.gender,
            'age': self.age,
            'major': self.major,
            'class_name': self.class_name,
            'phone': self.phone
        }


class Course:
    """课程实体类"""

    def __init__(self, course_id, course_name, credit=None,
                 teacher=None, semester=None):
        self.course_id = course_id      # 课程号
        self.course_name = course_name  # 课程名
        self.credit = credit            # 学分
        self.teacher = teacher          # 授课教师
        self.semester = semester        # 学期

    def __str__(self):
        return (f"课程号：{self.course_id} | 课程名：{self.course_name} | "
                f"学分：{self.credit or '—'} | 教师：{self.teacher or '—'} | "
                f"学期：{self.semester or '—'}")


class Grade:
    """成绩实体类"""

    def __init__(self, stu_id, course_id, score=None,
                 stu_name=None, course_name=None):
        self.stu_id = stu_id            # 学号
        self.course_id = course_id      # 课程号
        self.score = score              # 成绩
        self.stu_name = stu_name        # 学生姓名（联表查询时用）
        self.course_name = course_name  # 课程名（联表查询时用）

    def __str__(self):
        name_part = f" | 姓名：{self.stu_name}" if self.stu_name else ""
        course_part = f" | 课程：{self.course_name}" if self.course_name else ""
        return (f"学号：{self.stu_id}{name_part} | 课程号：{self.course_id}"
                f"{course_part} | 成绩：{self.score if self.score is not None else '未录入'}")
