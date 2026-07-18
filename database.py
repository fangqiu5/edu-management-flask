# -*- coding: utf-8 -*-
"""
数据库操作类 - 封装 MySQL 连接与基础 CRUD
"""

import pymysql
from db_config import DB_CONFIG


class Database:
    """数据库管理类，单例模式"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connect()
        return cls._instance

    def _connect(self):
        """建立数据库连接"""
        try:
            self.conn = pymysql.connect(
                host=DB_CONFIG['host'],
                port=DB_CONFIG['port'],
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password'],
                charset=DB_CONFIG['charset'],
                cursorclass=pymysql.cursors.DictCursor
            )
            self.cursor = self.conn.cursor()
            self._init_database()
            print("数据库连接成功！")
        except Exception as e:
            print(f"数据库连接失败：{e}")
            raise

    def _init_database(self):
        """初始化数据库和表"""
        # 创建数据库
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']} "
                            f"DEFAULT CHARACTER SET utf8mb4")
        self.cursor.execute(f"USE {DB_CONFIG['database']}")

        # 创建学生表
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS student (
                stu_id VARCHAR(20) PRIMARY KEY COMMENT '学号',
                name VARCHAR(50) NOT NULL COMMENT '姓名',
                gender VARCHAR(4) COMMENT '性别',
                age INT COMMENT '年龄',
                major VARCHAR(50) COMMENT '专业',
                class_name VARCHAR(50) COMMENT '班级',
                phone VARCHAR(20) COMMENT '联系电话'
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)

        # 创建课程表
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS course (
                course_id VARCHAR(20) PRIMARY KEY COMMENT '课程号',
                course_name VARCHAR(100) NOT NULL COMMENT '课程名',
                credit FLOAT COMMENT '学分',
                teacher VARCHAR(50) COMMENT '授课教师',
                semester VARCHAR(20) COMMENT '学期'
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)

        # 创建成绩表
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS grade (
                id INT AUTO_INCREMENT PRIMARY KEY,
                stu_id VARCHAR(20) NOT NULL COMMENT '学号',
                course_id VARCHAR(20) NOT NULL COMMENT '课程号',
                score FLOAT COMMENT '成绩',
                UNIQUE KEY uk_stu_course (stu_id, course_id),
                FOREIGN KEY (stu_id) REFERENCES student(stu_id) ON DELETE CASCADE,
                FOREIGN KEY (course_id) REFERENCES course(course_id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        # 创建管理员表
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL COMMENT '用户名',
                password VARCHAR(50) NOT NULL COMMENT '密码'
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)

        # 默认插入一个管理员账号
        self.cursor.execute(
            "INSERT IGNORE INTO admin (username, password) VALUES ('admin', '123456')"
        )

        self.conn.commit()


        self.conn.commit()

    def execute(self, sql, params=None):
        """执行增删改操作"""
        try:
            result = self.cursor.execute(sql, params)
            self.conn.commit()
            return result
        except Exception as e:
            self.conn.rollback()
            print(f"执行出错：{e}")
            return 0

    def query_one(self, sql, params=None):
        """查询单条记录"""
        self.cursor.execute(sql, params)
        return self.cursor.fetchone()

    def query_all(self, sql, params=None):
        """查询所有记录"""
        self.cursor.execute(sql, params)
        return self.cursor.fetchall()

    def close(self):
        """关闭连接"""
        if hasattr(self, 'cursor'):
            self.cursor.close()
        if hasattr(self, 'conn'):
            self.conn.close()
        print("数据库连接已关闭。")
