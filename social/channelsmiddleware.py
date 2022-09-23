from django.db import close_old_connections
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from jwt import decode as jwt_decode

from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from channels.auth import AuthMiddlewareStack

from urllib.parse import parse_qs

User = get_user_model()

@database_sync_to_async
def get_user(validated_token):
    try:
        user = User.objects.get(id=validated_token['user_id'])
        # print(user)
        return user
    
    except User.DoesNotExist:
        return AnonymousUser()


class JWTAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):

        self.inner = inner

    async def __call__(self, scope, receive, send):
        
        # Close old database connections
        close_old_connections()

        token = parse_qs(scope['query_string'].decode('utf-8'))['token'][0]

        # Authenticate user
        try:
            # Check and validate token
            UntypedToken(token)

        except (InvalidToken, TokenError) as e:
            # Token is invalid
            return None

        else:
            # Token is valid
            decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            scope['user'] = await get_user(validated_token=decoded_data)

        return await super().__call__(scope, receive, send)


def JWTAuthMiddlewareStack(inner):
    return JWTAuthMiddleware(AuthMiddlewareStack(inner))