from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.template import loader
from .models import *

# Create your views here.
"""所有学生的信息列表（仅做测试用）"""
def index(request):
    student_list = Student.objects.order_by('id')
    context = {
        'student_list': student_list,
    }
    return render(request, 'dbtest/index.html', context)


"""学号为sid的基本信息和各科成绩"""
def studentInfo(request, sid):
    if not request.COOKIES.get('student'):
        messages.error(request, '请先登录!')
        return redirect('login')
    elif request.COOKIES.get('student') != str(sid):
        messages.error(request, '请先退出当前账号!')
        return redirect('studentInfo', sid=int(request.COOKIES.get('student')))
    student = get_object_or_404(Student, pk=sid)
    score_list = student.studentcourse_set.all()
    context = {
        'student': student,
        'score_list': score_list,
    }
    return render(request, 'dbtest/studentInfo.html', context)


# 以下为正式代码
"""登录界面"""
def login(request):
    if request.method == 'GET':
        return render(request, 'dbtest/login.html')
    id = request.POST['id']
    password = request.POST['password']
    type = request.POST['type']
    if type == 'student':
        person = Student.objects.filter(id=id).first()
    elif type == 'teacher':
        person = Teacher.objects.filter(id=id).first()
    elif type == 'manager':
        person = Manager.objects.filter(id=id).first()
    if not person or person.password != password:
        return render(request, 'dbtest/login.html', {'error_message': '账号或密码错误'})
    # 这里不知道怎么优化能比两次判断类型好点
    if type == 'student':
        req = redirect('studentInfo', sid=id)
        req.set_cookie('student', str(id))
    elif type == 'teacher':
        pass
    elif type == 'manager':
        req = redirect('manager')
        req.set_cookie('manager', str(id))
    return req


"""登出"""
def logout(request):
    req = redirect('login')
    # 此处应有改进
    req.delete_cookie('student')
    req.delete_cookie('manager')
    return req


"""管理员界面"""
def manager(request):
    return render(request, 'dbtest/manager.html')


"""管理员获取班级列表"""
def classList(request):
    class_list = ClassInfo.objects.order_by('id')
    context = { 'classList': class_list, }
    return render(request, 'dbtest/classList.html', context)


"""管理员获取某班所有学生(仅供好看，可以不用）"""
def classStudent(request, cid):
    classInfo = get_object_or_404(ClassInfo, pk=cid)
    return render(request, 'dbtest/classStudent.html', {'classInfo': classInfo})


"""管理员添加班级"""
def addClass(request):
    if request.method == 'GET':
        return render(request, 'dbtest/addClass.html')
    if request.method == 'POST':
        id = int(request.POST['id'])
        if ClassInfo.objects.filter(pk=id):
            return render(request, 'dbtest/addClass.html', {'error_message': "该班级已存在!!!"})
        classInfo = ClassInfo(id=id)
        classInfo.save()
        return render(request, 'dbtest/addClass.html', {'success_message': "添加成功!"})


"""管理员获取学生列表"""
def studentList(request):
    student_list = Student.objects.order_by('id')
    context = {
        'student_list': student_list,
    }
    return render(request, 'dbtest/studentList.html', context)


"""管理员：添加学生"""
def addStudent(request):
    if request.method == 'GET':
        return render(request, 'dbtest/addStudent.html')
    if request.method == 'POST':
        try:
            classInfo = ClassInfo.objects.get(pk=int(request.POST['classInfo']))
        except (KeyError, ClassInfo.DoesNotExist):
            return render(request, 'dbtest/addStudent.html', {'error_message': "不存在此班级!!!"})
        id = int(request.POST['id'])
        if Student.objects.filter(pk=id):
            return render(request, 'dbtest/addStudent.html', {'error_message': "该学号已存在!!!"})
        name = request.POST['name']
        password = request.POST['password']
        newStudent = Student(id=id,classInfo=classInfo,name=name,password=password)
        newStudent.save()
        return render(request, 'dbtest/addStudent.html', {'success_message': "添加成功!"})


"""管理员删除学生"""
def deleteStudent(request, sid):
    student = Student.objects.filter(id=sid)
    if not student:
        messages.error(request, '无效的学生id')
    else:
        student = student[0]
        student.delete()
        messages.success(request, '删除成功')
    return redirect('studentList')


"""管理员修改学生信息"""
def updateStudent(request, sid):
    if request.method == 'GET':
        student = get_object_or_404(Student, id=sid)
        return render(request, 'dbtest/updateStudent.html', {'sid': sid, 'student': student})
    if request.method == 'POST':
        student = get_object_or_404(Student, id=sid)
        id = int(request.POST['id'])
        name, password = request.POST['name'], request.POST['password']
        try:
            classInfo = ClassInfo.objects.get(pk=int(request.POST['classInfo']))
        except (KeyError, ClassInfo.DoesNotExist):
            context = {
                'sid': sid,
                'student': student,
                'error_message': '不存在此班级!!!'
            }
            return render(request, 'dbtest/updateStudent.html', context)
        # 如果要改学号,先判断改动后是否影响别的记录
        if id != sid:
            if Student.objects.filter(pk=id):
                context = {
                    'sid': sid,
                    'student': student,
                    'error_message': '该学号已存在!!!'
                }
                return render(request, 'dbtest/updateStudent.html', context)
        data = { 'id': id, 'classInfo': classInfo, 'name': name, 'password': password }
        Student.objects.filter(pk=sid).update(**data)
        messages.success(request, '修改成功')
        return redirect('studentList')


"""管理员获取老师列表"""
def teacherList(request):
    teacher_list = Teacher.objects.order_by('id')
    return render(request, 'dbtest/teacherList.html', {'teacher_list': teacher_list})


"""管理员：增加老师"""
def addTeacher(request):
    if request.method == 'GET':
        return render(request, 'dbtest/addTeacher.html')
    if request.method == 'POST':
        id = int(request.POST['id'])
        if Teacher.objects.filter(pk=id):
            return render(request, 'dbtest/addTeacher.html', {'error_message': "该工号已存在!!!"})
        name = request.POST['name']
        password = request.POST['password']
        newTeacher = Teacher(id=id, name=name, password=password)
        newTeacher.save()
        return render(request, 'dbtest/addTeacher.html', {'success_message': "添加成功!"})


"""管理员：删除老师"""
def deleteTeacher(request, tid):
    teacher = Teacher.objects.filter(id=tid)
    if not teacher:
        messages.error(request, '无效的教师id')
    else:
        teacher = teacher[0]
        teacher.delete()
        messages.success(request, '删除成功')
    return redirect('teacherList')


"""管理员：修改老师信息"""
def updateTeacher(request, tid):
    if request.method == 'GET':
        teacher = get_object_or_404(Teacher, id=tid)
        return render(request, 'dbtest/updateTeacher.html', {'tid': tid, 'teacher': teacher})
    if request.method == 'POST':
        teacher = get_object_or_404(Teacher, id=tid)
        id = int(request.POST['id'])
        name, password = request.POST['name'], request.POST['password']
        # 如果要改工号,先判断改动后是否影响别的记录
        if id != tid:
            if Teacher.objects.filter(pk=id):
                context = {
                    'tid': tid,
                    'teacher': teacher,
                    'error_message': '该工号已存在!!!'
                }
                return render(request, 'dbtest/updateTeacher.html', context)
        data = {'id': id, 'name': name, 'password': password}
        Teacher.objects.filter(pk=tid).update(**data)
        messages.success(request, '修改成功')
        return redirect('teacherList')


"""管理员：获取课程列表"""
def courseList(request):
    course_list = Course.objects.order_by('id')
    return render(request, 'dbtest/courseList.html', {'course_list': course_list})


"""管理员：增加课程"""
def addCourse(request):
    if request.method == 'GET':
        return render(request, 'dbtest/addCourse.html')
    if request.method == 'POST':
        id = int(request.POST['id'])
        if Course.objects.filter(id=id):
            return render(request, 'dbtest/addCourse.html', {'error_message': "该课程号已存在!!!"})
        tid = int(request.POST['tid'])
        teacher = Teacher.objects.filter(pk=tid).first()
        if not teacher:
            return render(request, 'dbtest/addCourse.html', {'error_message': "该教师不存在!!!"})
        name = request.POST['name']
        credit = float(request.POST['credit'])
        newCourse = Course(id=id, teacher=teacher, name=name, credit=credit)
        newCourse.save()
        return render(request, 'dbtest/addCourse.html', {'success_message': "添加成功!"})


"""管理员：删除课程"""
def deleteCourse(request, cid):
    course = Course.objects.filter(id=cid)
    if not course:
        messages.error(request, '无效的课程id')
    else:
        course = course[0]
        course.delete()
        messages.success(request, '删除成功')
    return redirect('courseList')


"""管理员：修改课程信息"""
def updateCourse(request, cid):
    if request.method == 'GET':
        course = get_object_or_404(Course, id=cid)
        return render(request, 'dbtest/updateCourse.html', {'cid': cid, 'course': course})
    if request.method == 'POST':
        course = get_object_or_404(Course, id=cid)
        try:
            teacher = Teacher.objects.get(id=int(request.POST['tid']))
        except (KeyError, Teacher.DoesNotExist):
            context = {
                'course': course,
                'error_message': "该教工ID不存在!!!"
            }
            return render(request, 'dbtest/updateCourse.html', context)
        id = int(request.POST['id'])
        # 如果要改课程号,先判断改动后是否影响别的记录
        if id != cid:
            if Course.objects.filter(id=cid):
                context = {
                    'cid': cid,
                    'course': course,
                    'error_message': '该课程号已存在!!!'
                }
                return render(request, 'dbtest/updateCourse.html', context)
        name, credit = request.POST['name'], float(request.POST['credit'])
        data = {'id': id, 'teacher': teacher, 'name': name, 'credit': credit}
        Course.objects.filter(id=cid).update(**data)
        messages.success(request, '修改成功')
        return redirect('courseList')


""""""

