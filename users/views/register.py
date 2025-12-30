from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import User
import uuid

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        role = request.data.get('role')

        if not username or not password or not role:
            return Response({"code": 1, "message": "username, password, role required"}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"code": 1, "message": "Account already exists"}, status=400)

        # 生成唯一 openid
        openid = str(uuid.uuid4())

        user = User(username=username, role=role, openid=openid)
        user.set_password(password)
        user.save()

        return Response({"code": 0, "message": "registered"})
