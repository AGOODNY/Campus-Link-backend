from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from users.models import User
from users.serializers import MeSerializer


class LoginView(APIView):
    def post(self, request):
        openid = request.data.get('openid')
        role = request.data.get('role')

        if not openid:
            return Response({'code': 1, 'message': 'openid is required'}, status=400)

        if role not in ['student', 'staff']:
            return Response({'code': 1, 'message': 'role must be student or staff'}, status=400)

        user, created = User.objects.get_or_create(
            openid=openid,
            defaults={
                'username': f'user_{openid[-6:]}',
                'role': role
            }
        )

        # 已存在用户，更新角色
        if not created and user.role != role:
            user.role = role
            user.save()

        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            'code': 0,
            'message': 'success',
            'data': {
                'token': token.key,
                'role': user.role,
                'is_staff': user.is_staff
            }
        })

