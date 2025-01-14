from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', '管理员'),
        ('teacher', '教师'),
        ('student', '学生'),
    )
    
    phone = models.CharField(max_length=11, blank=True, null=True, verbose_name='手机号')
    role = models.CharField(
        max_length=10, 
        choices=ROLE_CHOICES,
        default='student',
        verbose_name='角色'
    )

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

class Class(models.Model):
    class_id = models.CharField(max_length=20, unique=True, verbose_name='班级编号', default='DEFAULT')
    name = models.CharField(max_length=50, verbose_name='班级名称')
    student_count = models.IntegerField(default=0, verbose_name='学生人数')

    class Meta:
        db_table = 'students_class'
        verbose_name = '班级'
        verbose_name_plural = '班级'

    def __str__(self):
        return self.name

class Student(models.Model):
    GENDER_CHOICES = (
        ('男', '男'),
        ('女', '女'),
    )
    
    student_id = models.CharField(max_length=20, unique=True, verbose_name='学号')
    name = models.CharField(max_length=50, verbose_name='姓名')
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, verbose_name='性别')
    age = models.IntegerField(verbose_name='年龄')
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name='班级')
    phone = models.CharField(max_length=11, verbose_name='联系电话')
    
    class Meta:
        db_table = 'student'
        verbose_name = '学生'
        verbose_name_plural = verbose_name
        
    def __str__(self):
        return f"{self.name}({self.student_id})"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 保存原始班级ID，用于跟踪班级变更
        self._original_class_id = self.class_id if self.id else None

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # 更新原始班级ID
        self._original_class_id = self.class_id

class Course(models.Model):
    course_id = models.CharField(max_length=20, unique=True, verbose_name='课程编号')
    name = models.CharField(max_length=100, verbose_name='课程名称')
    teacher = models.CharField(max_length=50, verbose_name='任课教师')
    credit = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='学分')
    description = models.TextField(blank=True, verbose_name='课程描述')
    
    class Meta:
        db_table = 'course'
        verbose_name = '课程'
        verbose_name_plural = verbose_name
        
    def __str__(self):
        return f"{self.name}({self.course_id})"

class Score(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='学生')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程')
    semester = models.CharField(max_length=20, verbose_name='学期')
    
    class Meta:
        db_table = 'score'
        verbose_name = '成绩'
        verbose_name_plural = verbose_name
        unique_together = ('student', 'course', 'semester')  # 同一学期同一门课只能有一个成绩
        
    def __str__(self):
        return f"{self.student.name}-{self.course.name}-{self.score}"
