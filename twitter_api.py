import tweepy
import os
from dotenv import load_dotenv
from tweepy.errors import TweepyException

#Load env variables
load_dotenv()

class TwitterAPI:
    def __init__(self):
        self.bearer_token = os.getenv("BEARER_TOKEN")
        self.api_key = os.getenv("API_KEY")
        self.api_secret_key = os.getenv("API_SECRET_KEY")
        self.access_token = os.getenv("ACCESS_TOKEN")
        self.access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
        self.client = self.authenticate()

    def authenticate(self):
        """Autentica con la API v2 de Twitter usando el Bearer Token y devuelve un cliente de API de Tweepy."""
        try:
            client = tweepy.Client(
                bearer_token=self.bearer_token,
                consumer_key=self.api_key,
                consumer_secret=self.api_secret_key,
                access_token=self.access_token,
                access_token_secret=self.access_token_secret
            )
            print("Autenticación exitosa")
            return client
        except TweepyException as e:
            print(f"Error en la autenticación: {e}")
            return None

    def get_user_by_username(self, username):
        """Obtiene información de un usuario específico por nombre de usuario."""
        if not self.client:
            print("API no autenticada")
            return None

        try:
            user = self.client.get_user(username=username, user_fields=["username", "name", "description", "public_metrics"])
            if user and user.data:
                # Extract relevant fields of a dictionary
                user_data = {
                    "username": user.data.username,
                    "name": user.data.name,
                    "description": user.data.description,
                    "public_metrics": user.data.public_metrics
                }
                return user_data
            else:
                return None
        except TweepyException as e:
            print(f"Error al obtener el usuario: {e}")
            return None

    def get_authenticated_user(self):
        """Obtiene información sobre el usuario autenticado."""
        if not self.client:
            print("API no autenticada")
            return None

        try:
            user = self.client.get_me(user_fields=["username", "name", "description", "public_metrics"])
            if user and user.data:
                # Extract relevant fields of a dictionary
                user_data = {
                    "username": user.data.username,
                    "name": user.data.name,
                    "description": user.data.description,
                    "public_metrics": user.data.public_metrics
                }
                return user_data
            else:
                return None
        except TweepyException as e:
            print(f"Error al obtener el usuario autenticado: {e}")
            return None
