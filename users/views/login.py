from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from users.models import User
from users.serializers import MeSerializer


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"code": 1, "message": "Username and password required"}, status=400)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"code": 1, "message": "Account does not exist"}, status=400)

        if not user.check_password(password):
            return Response({"code": 1, "message": "Password incorrect"}, status=400)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "code": 0,
            "message": "success",
            "data": {
                "token": token.key,
                "role": user.role,
                "is_staff": user.is_staff
            }
        })


