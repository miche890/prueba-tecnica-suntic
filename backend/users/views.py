import datetime
import jwt
import pyotp
import qrcode
import base64

from django.http import HttpResponse

from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from backend import settings
from .models import User
from .serializers import UserSerializer

from io import BytesIO


# Create your views here.
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generar una clave secreta para 2FA
        user.mfa_secret = pyotp.random_base32()
        user.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class Enable2FAView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        if not user.mfa_enabled:
            if not user.mfa_secret:
                user.mfa_secret = pyotp.random_base32()
                user.save()

            # Generar una URL para Google Authenticator
            totp = pyotp.TOTP(user.mfa_secret)
            otpauth_url = totp.provisioning_uri(name=user.email, issuer_name="PruebaSUNTIC")

            # Generar el código QR
            qr = qrcode.make(otpauth_url)
            buffer = BytesIO()
            qr.save(buffer, format="PNG")
            buffer.seek(0)

            # Convertir el código QR en base64
            qr_base64 = base64.b64encode(buffer.getvalue()).decode()

            user.mfa_enabled = True
            user.save()

            return Response({'qr_url': f"data:image/png;base64,{qr_base64}"}, status=status.HTTP_200_OK)

        return Response({'detail': '2FA ya está habilitado'}, status=status.HTTP_400_BAD_REQUEST)


class Verify2FAView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        code = request.data.get('code')
        user = request.user

        if not user.mfa_enabled:
            return Response({'detail': '2FA no está habilitado para este usuario'}, status=status.HTTP_400_BAD_REQUEST)

        if not code:
            return Response({'detail': 'El código es obligatorio'}, status=status.HTTP_400_BAD_REQUEST)

        totp = pyotp.TOTP(user.mfa_secret)

        if not totp.verify(code):
            return Response({'detail': 'El código es inválido'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': '2FA verificado exitosamente'}, status=status.HTTP_200_OK)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        token = request.data.get('token')  # Token del 2FA

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        if user.mfa_enabled:
            if not token:
                raise AuthenticationFailed('2FA Token is required')

            totp = pyotp.TOTP(user.mfa_secret)
            if not totp.verify(token):
                raise AuthenticationFailed('2FA Token is invalid')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.now(datetime.UTC),
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True, expires=payload.get('exp'))
        response.data = {'jwt': token}
        response.status = status.HTTP_200_OK

        return response


class Disable2FAView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        user.mfa_enabled = False
        user.mfa_secret = None
        user.save()
        return Response({'detail': '2FA has been disabled'}, status=status.HTTP_200_OK)


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        serializer = UserSerializer(user)

        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {'message': 'Logged out success'}

        return response
