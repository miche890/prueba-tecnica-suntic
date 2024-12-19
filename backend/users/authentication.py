from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
import jwt
from users.models import User  # Cambia esto según el modelo de usuario que estés usando


class CookieJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            return None  # No autenticar si no hay token

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.exceptions.ExpiredSignatureError:
            raise AuthenticationFailed('Token expirado')
        except jwt.exceptions.InvalidTokenError:
            raise AuthenticationFailed('Token inválido')

        try:
            user = User.objects.get(id=payload['id'])
        except User.DoesNotExist:
            raise AuthenticationFailed('Usuario no encontrado')

        return (user, None)
