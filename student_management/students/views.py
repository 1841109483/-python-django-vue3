from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta
import uuid
from .models import User, Student, Class, Course, Score
from .serializers import UserSerializer, RegisterSerializer, StudentSerializer, ClassSerializer, CourseSerializer, ScoreSerializer
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.db.models import Q, Avg, Count

User = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password'],
                email=serializer.validated_data['email'],
                phone=serializer.validated_data['phone']
            )
            return Response({'message': '注册成功'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        phone = request.data.get('phone')
        new_password = request.data.get('new_password')
        
        try:
            # 验证用户信息是否匹配
            user = User.objects.get(
                username=username,
                email=email,
                phone=phone
            )
            # 更新密码
            user.set_password(new_password)
            user.save()
            return Response({'message': '密码重置成功'})
        except User.DoesNotExist:
            return Response(
                {'message': '用户信息验证失败，请确保用户名、邮箱和手机号都正确'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
    def get_queryset(self):
        queryset = Student.objects.all()
        name = self.request.query_params.get('name', None)
        student_id = self.request.query_params.get('student_id', None)
        
        if name:
            queryset = queryset.filter(name__icontains=name)
        if student_id:
            queryset = queryset.filter(student_id__icontains=student_id)
            
        return queryset

class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer

    def perform_create(self, serializer):
        # 验证数据
        class_id = self.request.data.get('class_id')
        name = self.request.data.get('name')
        teacher = self.request.data.get('teacher')

        if not all([class_id, name, teacher]):
            raise serializers.ValidationError('班级编号、名称和班主任都是必填项')

        # 检查班级编号是否已存在
        if Class.objects.filter(class_id=class_id).exists():
            raise serializers.ValidationError('该班级编号已存在')

        serializer.save()

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    
    def get_queryset(self):
        queryset = Course.objects.all()
        name = self.request.query_params.get('name', None)
        course_id = self.request.query_params.get('course_id', None)
        
        if name:
            queryset = queryset.filter(name__icontains=name)
        if course_id:
            queryset = queryset.filter(course_id__icontains=course_id)
            
        return queryset

    def perform_create(self, serializer):
        # 验证数据
        course_id = self.request.data.get('course_id')
        name = self.request.data.get('name')
        teacher = self.request.data.get('teacher')
        credit = self.request.data.get('credit')
        hours = self.request.data.get('hours')

        if not all([course_id, name, teacher, credit, hours]):
            raise serializers.ValidationError('课程编号、名称、教师、学分和课时都是必填项')

        # 检查课程编号是否已存在
        if Course.objects.filter(course_id=course_id).exists():
            raise serializers.ValidationError('该课程编号已存在')

        try:
            credit = float(credit)
            hours = int(hours)
            if credit <= 0 or hours <= 0:
                raise ValueError
        except ValueError:
            raise serializers.ValidationError('学分和课时必须是正数')

        serializer.save()

class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    
    def get_queryset(self):
        queryset = Score.objects.all()
        student_id = self.request.query_params.get('student_id', None)
        course_id = self.request.query_params.get('course_id', None)
        semester = self.request.query_params.get('semester', None)
        
        if student_id:
            queryset = queryset.filter(student__student_id__icontains=student_id)
        if course_id:
            queryset = queryset.filter(course__course_id__icontains=course_id)
        if semester:
            queryset = queryset.filter(semester=semester)
            
        return queryset

    def perform_create(self, serializer):
        # 验证数据
        student = self.request.data.get('student')
        course = self.request.data.get('course')
        score = self.request.data.get('score')
        semester = self.request.data.get('semester')

        if not all([student, course, score, semester]):
            raise serializers.ValidationError('学生、课程、成绩和学期都是必填项')

        try:
            score = float(score)
            if not 0 <= score <= 100:
                raise ValueError
        except ValueError:
            raise serializers.ValidationError('成绩必须是0-100之间的数字')

        # 检查是否已存在该学生同一学期同一课程的成绩
        if Score.objects.filter(
            student_id=student,
            course_id=course,
            semester=semester
        ).exists():
            raise serializers.ValidationError('该学生在该学期的这门课程已有成绩记录')

        serializer.save()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_stats(request):
    try:
        # 基础统计数据
        total_students = Student.objects.count()
        total_courses = Course.objects.count()
        total_classes = Class.objects.count()
        average_score = Score.objects.aggregate(Avg('score'))['score__avg'] or 0

        # 班级分布
        class_distribution = Class.objects.annotate(
            value=Count('student')
        ).values('name', 'value')

        # 成绩分布
        score_ranges = [
            {'min': 0, 'max': 60, 'label': '0-60'},
            {'min': 60, 'max': 70, 'label': '60-70'},
            {'min': 70, 'max': 80, 'label': '70-80'},
            {'min': 80, 'max': 90, 'label': '80-90'},
            {'min': 90, 'max': 100, 'label': '90-100'},
        ]
        
        score_distribution = []
        for range_info in score_ranges:
            count = Score.objects.filter(
                score__gte=range_info['min'],
                score__lt=range_info['max']
            ).count()
            score_distribution.append({
                'name': range_info['label'],
                'value': count
            })

        # 课程平均分
        course_averages = Course.objects.annotate(
            average=Avg('score__score')
        ).values('name', 'average')

        # 性别比例
        gender_ratio = Student.objects.values('gender').annotate(
            value=Count('id')
        ).values('gender', 'value')

        return Response({
            'overview': {
                'totalStudents': total_students,
                'totalCourses': total_courses,
                'totalClasses': total_classes,
                'averageScore': round(float(average_score), 1) if average_score else 0
            },
            'classDistribution': list(class_distribution),
            'scoreDistribution': list(score_distribution),
            'courseAverage': list(course_averages),
            'genderRatio': list(gender_ratio)
        })
    except Exception as e:
        print(f"Stats error: {str(e)}")  # 添加调试日志
        return Response({'error': str(e)}, status=500)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class UserViewSet(viewsets.ModelViewSet):
    """
    用户管理视图集
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        queryset = User.objects.all().order_by('-date_joined')
        search = self.request.query_params.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) |
                Q(email__icontains=search)
            )
        return queryset

    def perform_create(self, serializer):
        # 创建用户时设置密码和默认角色
        password = self.request.data.get('password')
        role = self.request.data.get('role', 'student')  # 默认为学生角色
        user = serializer.save(role=role)
        if password:
            user.set_password(password)
            user.save()

    def perform_update(self, serializer):
        # 更新用户时处理密码
        password = self.request.data.get('password')
        user = serializer.save()
        if password:
            user.set_password(password)
            user.save()
