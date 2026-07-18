# -*- coding: utf-8 -*-
"""
Flask Web 版教务管理系统
运行后浏览器访问 http://127.0.0.1:5000
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import Database

app = Flask(__name__)
app.secret_key = 'edu_system_secret'

db = Database()

from functools import wraps

# 登录校验装饰器
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# ========== 登录页 ==========
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = db.query_one(
            "SELECT * FROM admin WHERE username=%s AND password=%s",
            (username, password)
        )
        if admin:
            session['username'] = username
            flash('登录成功！', 'success')
            return redirect(url_for('index'))
        else:
            flash('用户名或密码错误！', 'error')
    return render_template('login.html')


# ========== 退出登录 ==========
@app.route('/logout')
def logout():
    session.clear()
    flash('已退出登录', 'success')
    return redirect(url_for('login'))



# ========== 首页 ==========
@app.route('/')
@login_required
def index():
    # 统计数据展示在首页
    stu_count = db.query_one("SELECT COUNT(*) as cnt FROM student")['cnt']
    course_count = db.query_one("SELECT COUNT(*) as cnt FROM course")['cnt']
    grade_count = db.query_one("SELECT COUNT(*) as cnt FROM grade")['cnt']
    return render_template('index.html',
                           stu_count=stu_count,
                           course_count=course_count,
                           grade_count=grade_count)


# ========== 学生管理 ==========
@app.route('/students')
@login_required
def students():
    keyword = request.args.get('keyword', '')
    if keyword:
        rows = db.query_all(
            "SELECT * FROM student WHERE stu_id LIKE %s OR name LIKE %s ORDER BY stu_id",
            (f'%{keyword}%', f'%{keyword}%')
        )
    else:
        rows = db.query_all("SELECT * FROM student ORDER BY stu_id")
    return render_template('students.html', students=rows, keyword=keyword)


@app.route('/student/add', methods=['POST'])
@login_required
def add_student():
    stu_id = request.form['stu_id']
    name = request.form['name']
    gender = request.form.get('gender') or None
    age = request.form.get('age') or None
    major = request.form.get('major') or None
    class_name = request.form.get('class_name') or None
    phone = request.form.get('phone') or None

    if db.query_one("SELECT stu_id FROM student WHERE stu_id=%s", stu_id):
        flash('学号已存在！', 'error')
    else:
        db.execute(
            "INSERT INTO student (stu_id, name, gender, age, major, class_name, phone) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (stu_id, name, gender, age, major, class_name, phone)
        )
        flash('添加成功！', 'success')
    return redirect(url_for('students'))


@app.route('/student/delete/<stu_id>')
@login_required
def delete_student(stu_id):
    db.execute("DELETE FROM student WHERE stu_id=%s", stu_id)
    flash('删除成功！', 'success')
    return redirect(url_for('students'))


# ========== 课程管理 ==========
@app.route('/courses')
@login_required
def courses():
    keyword = request.args.get('keyword', '')
    if keyword:
        rows = db.query_all(
            "SELECT * FROM course WHERE course_id LIKE %s OR course_name LIKE %s ORDER BY course_id",
            (f'%{keyword}%', f'%{keyword}%')
        )
    else:
        rows = db.query_all("SELECT * FROM course ORDER BY course_id")
    return render_template('courses.html', courses=rows, keyword=keyword)


@app.route('/course/add', methods=['POST'])
@login_required
def add_course():
    course_id = request.form['course_id']
    course_name = request.form['course_name']
    credit = request.form.get('credit') or None
    teacher = request.form.get('teacher') or None
    semester = request.form.get('semester') or None

    if db.query_one("SELECT course_id FROM course WHERE course_id=%s", course_id):
        flash('课程号已存在！', 'error')
    else:
        db.execute(
            "INSERT INTO course (course_id, course_name, credit, teacher, semester) "
            "VALUES (%s, %s, %s, %s, %s)",
            (course_id, course_name, credit, teacher, semester)
        )
        flash('添加成功！', 'success')
    return redirect(url_for('courses'))


@app.route('/course/delete/<course_id>')
@login_required
def delete_course(course_id):
    db.execute("DELETE FROM course WHERE course_id=%s", course_id)
    flash('删除成功！', 'success')
    return redirect(url_for('courses'))


# ========== 成绩管理 ==========
@app.route('/grades')
@login_required
def grades():
    # 默认按学生查
    view = request.args.get('view', 'student')
    keyword = request.args.get('keyword', '')
    grades_data = []

    if view == 'student' and keyword:
        grades_data = db.query_all(
            "SELECT g.id, g.stu_id, s.name as stu_name, g.course_id, "
            "c.course_name, g.score FROM grade g "
            "JOIN student s ON g.stu_id = s.stu_id "
            "JOIN course c ON g.course_id = c.course_id "
            "WHERE g.stu_id = %s OR s.name LIKE %s "
            "ORDER BY g.stu_id, g.course_id",
            (keyword, f'%{keyword}%')
        )
    elif view == 'course' and keyword:
        grades_data = db.query_all(
            "SELECT g.id, g.stu_id, s.name as stu_name, g.course_id, "
            "c.course_name, g.score FROM grade g "
            "JOIN student s ON g.stu_id = s.stu_id "
            "JOIN course c ON g.course_id = c.course_id "
            "WHERE g.course_id = %s OR c.course_name LIKE %s "
            "ORDER BY g.score DESC",
            (keyword, f'%{keyword}%')
        )

    return render_template('grades.html',
                           grades=grades_data,
                           view=view,
                           keyword=keyword)


@app.route('/grade/add', methods=['POST'])
@login_required
def add_grade():
    stu_id = request.form['stu_id']
    course_id = request.form['course_id']
    score = request.form.get('score') or None

    if not db.query_one("SELECT stu_id FROM student WHERE stu_id=%s", stu_id):
        flash('学生不存在！', 'error')
    elif not db.query_one("SELECT course_id FROM course WHERE course_id=%s", course_id):
        flash('课程不存在！', 'error')
    elif db.query_one(
        "SELECT id FROM grade WHERE stu_id=%s AND course_id=%s", (stu_id, course_id)
    ):
        flash('该成绩已存在！', 'error')
    else:
        db.execute(
            "INSERT INTO grade (stu_id, course_id, score) VALUES (%s, %s, %s)",
            (stu_id, course_id, score)
        )
        flash('录入成功！', 'success')
    return redirect(url_for('grades'))


@app.route('/grade/delete/<int:grade_id>')
@login_required
def delete_grade(grade_id):
    db.execute("DELETE FROM grade WHERE id=%s", grade_id)
    flash('删除成功！', 'success')
    return redirect(url_for('grades'))

# ========== 编辑学生 ==========
@app.route('/student/edit/<stu_id>', methods=['GET', 'POST'])
@login_required
def edit_student(stu_id):
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form.get('gender') or None
        age = request.form.get('age') or None
        major = request.form.get('major') or None
        class_name = request.form.get('class_name') or None
        phone = request.form.get('phone') or None

        db.execute(
            "UPDATE student SET name=%s, gender=%s, age=%s, "
            "major=%s, class_name=%s, phone=%s WHERE stu_id=%s",
            (name, gender, age, major, class_name, phone, stu_id)
        )
        flash('修改成功！', 'success')
        return redirect(url_for('students'))

    stu = db.query_one("SELECT * FROM student WHERE stu_id=%s", stu_id)
    return render_template('student_edit.html', stu=stu)


# ========== 编辑课程 ==========
@app.route('/course/edit/<course_id>', methods=['GET', 'POST'])
@login_required
def edit_course(course_id):
    if request.method == 'POST':
        course_name = request.form['course_name']
        credit = request.form.get('credit') or None
        teacher = request.form.get('teacher') or None
        semester = request.form.get('semester') or None

        db.execute(
            "UPDATE course SET course_name=%s, credit=%s, teacher=%s, semester=%s "
            "WHERE course_id=%s",
            (course_name, credit, teacher, semester, course_id)
        )
        flash('修改成功！', 'success')
        return redirect(url_for('courses'))

    course = db.query_one("SELECT * FROM course WHERE course_id=%s", course_id)
    return render_template('course_edit.html', course=course)


# ========== 编辑成绩 ==========
@app.route('/grade/edit/<int:grade_id>', methods=['GET', 'POST'])
@login_required
def edit_grade(grade_id):
    if request.method == 'POST':
        score = request.form.get('score') or None
        db.execute("UPDATE grade SET score=%s WHERE id=%s", (score, grade_id))
        flash('修改成功！', 'success')
        return redirect(url_for('grades'))

    grade = db.query_one(
        "SELECT g.*, s.name as stu_name, c.course_name FROM grade g "
        "JOIN student s ON g.stu_id = s.stu_id "
        "JOIN course c ON g.course_id = c.course_id "
        "WHERE g.id=%s", grade_id
    )
    return render_template('grade_edit.html', grade=grade)



# ========== 启动 ==========
if __name__ == '__main__':
    app.run(debug=True)
