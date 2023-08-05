from app.decorators.generic import handle_exceptions

from datetime import datetime, timedelta
from jose import jwt


class JWT:
    def __init__(
            self,
            secret_key: str = 'NotSecret',
            algorithm: str = 'HS256',
            access_expires_minutes: int = 1440,
            refresh_expires_minutes: int = 10080
    ):
        self.__secret_key = secret_key
        self.__algorithm = algorithm
        self.__access_expires_minutes = access_expires_minutes
        self.__refresh_expires_minutes = refresh_expires_minutes

    def __jwt_token_generator(self, token_type: str, expires_minutes: int, payload: dict = None) -> str:
        data = payload.copy() if payload is not None else {}
        data.update({
            'iat': datetime.now(),
            'exp': datetime.now() + timedelta(minutes=expires_minutes),
            'type': token_type
        })
        return jwt.encode(data, self.__secret_key, algorithm=self.__algorithm)

    def __generate_access_token(self, payload: dict = None) -> str:
        return self.__jwt_token_generator('access', self.__access_expires_minutes, payload)

    def __generate_refresh_token(self, payload: dict = None) -> str:
        return self.__jwt_token_generator('refresh', self.__refresh_expires_minutes, payload)

    @handle_exceptions(jwt.JWTError)
    def jwt_token_validator(self, token: str) -> dict:
        return jwt.decode(token, self.__secret_key, algorithms=[self.__algorithm])

    def get_token(self, payload: dict = None) -> dict:
        access_token = self.__generate_access_token(payload)
        refresh_token = self.__generate_refresh_token(payload)
        return {'access': access_token, 'refresh': refresh_token, 'token_type': 'bearer'}

    def refresh_token(self, refresh_token: str) -> dict:
        refresh_token_payload = self.jwt_token_validator(refresh_token)
        if refresh_token_payload.get('type') != 'refresh':
            raise jwt.JWTError('Invalid Token')
        else:
            access_token = self.__generate_access_token(refresh_token_payload)
            return {'access': access_token, 'refresh': refresh_token, 'token_type': 'bearer'}
