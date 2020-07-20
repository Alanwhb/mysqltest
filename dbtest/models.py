from django.db import models

# Create your models here.
"""教师表"""
class Teacher(models.Model):
    id = models.IntegerField(primary_key=True)
    password = models.CharField(max_length=20)
    name = models.CharField(max_length=45)

    def __str__(self):
        return self.name


"""班级表"""
class ClassInfo(models.Model):
    id = models.IntegerField(primary_key=True)

    def __str__(self):
        return str(self.id)


"""学生表"""
class Student(models.Model):
    id = models.IntegerField(primary_key=True)
    password = models.CharField(max_length=20)
    name = models.CharField(max_length=45)
    classInfo = models.ForeignKey(ClassInfo, on_delete=models.CASCADE)


"""课程表:同一课名不同老师为不同的课程"""
class Course(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45)
    credit = models.FloatField(default=0)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + "-" + self.teacher.name


"""学生成绩表"""
class StudentCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)


"""管理员表"""
class Manager(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45)
    password = models.CharField(max_length=20)