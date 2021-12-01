import datetime

from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import User, UserToken
from .authentication import JWTAuthentication
from .serializers import UserSerializer


class RegisterAPIView(APIView):
    def post(self, request):
        data = request.data

        if data['password'] != data['password_confirm']:
            raise exceptions.APIException('Passwords do not match!')

        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginAPIView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        scope = request.data['scope']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise exceptions.AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('Incorrect Password!')

        if user.is_ambassador and scope == 'admin':
            raise exceptions.AuthenticationFailed('Unauthorized')

        token = JWTAuthentication.generate_jwt(user.id, scope)

        UserToken.objects.create(
            user_id=user.id,
            token=token,
            created=datetime.datetime.utcnow(),
            expired_at=datetime.datetime.utcnow() + datetime.timedelta(days=1)
        )

        return Response({'jwt': token})


class UserAPIView(APIView):
    def get(self, request, scope=''):
        token = request.COOKIES.get('jwt')

        if not token:
            raise exceptions.AuthenticationFailed('Unauthorized')

        payload = JWTAuthentication.get_payload(token)
        user = User.objects.get(pk=payload['user_id'])

        if user is None:
            raise exceptions.AuthenticationFailed('User not found!')

        if not UserToken.objects.filter(user_id=user.id,
                                        token=token,
                                        expired_at__gt=datetime.datetime.utcnow()).exists():
            raise exceptions.AuthenticationFailed('Invalid Scope!')

        scope_admin_user_ambassador = user.is_ambassador and payload['scope'] != 'ambassador'
        scope_ambassador_user_admin = not user.is_ambassador and payload['scope'] != 'admin'
        scope_path_different = payload['scope'] != scope

        if scope_admin_user_ambassador or scope_ambassador_user_admin or scope_path_different:
            raise exceptions.AuthenticationFailed('Unauthorized')

        return Response(UserSerializer(user).data)


class LogoutAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        UserToken.objects.filter(user_id=request.user.id).delete()
        response = Response()
        response.data = {
            'message': 'success'
        }
        return response


class ProfileInfoAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk=None):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ProfilePasswordAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk=None):
        user = request.user
        data = request.data

        if data['password'] != data['password_confirm']:
            raise exceptions.APIException('Passwords do not match!')

        user.set_password(data['password'])
        user.save()
        return Response(UserSerializer(user).data)


class UsersAPIView(APIView):
    def get(self, _, pk=None):
        if pk is None:
            return Response(UserSerializer(User.objects.all(), many=True).data)

        return Response(UserSerializer(User.objects.get(pk=pk)).data)
