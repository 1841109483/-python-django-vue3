from rest_framework import serializers
from .models import User, Student, Class, Course, Score
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_active', 'date_joined', 'role', 'password']
        read_only_fields = ['date_joined']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'role': {'required': False}
        }

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email', 'phone']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("两次密码不一致")
        return data

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['id', 'class_id', 'name', 'teacher', 'student_count']
        read_only_fields = ['student_count']  # 学生人数由系统自动计算

class StudentSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source='class_id.name', read_only=True)
    
    class Meta:
        model = Student
        fields = ['id', 'student_id', 'name', 'gender', 'age', 'class_id', 'class_name', 'phone', 'created_at']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'course_id', 'name', 'teacher', 'credit', 'hours', 'description', 'created_at']
        read_only_fields = ['created_at']

class ScoreSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    student_id = serializers.CharField(source='student.student_id', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    course_id = serializers.CharField(source='course.course_id', read_only=True)
    
    class Meta:
        model = Score
        fields = ['id', 'student', 'student_name', 'student_id', 
                 'course', 'course_name', 'course_id', 
                 'score', 'semester', 'created_at']
        read_only_fields = ['created_at'] 