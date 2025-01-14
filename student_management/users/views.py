from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    try:
        user = authenticate(username=username, password=password)
        
        if user is not None and user.is_active:
            refresh = RefreshToken.for_user(user)
            return Response({
                'token': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': getattr(user, 'role', 'student')
                }
            })
        else:
            return Response({
                'error': '用户名或密码错误'
            }, status=401)
    except Exception as e:
        print(f"Login error: {str(e)}")  # 添加调试日志
        return Response({
            'error': '登录失败，请稍后重试'
        }, status=500) 