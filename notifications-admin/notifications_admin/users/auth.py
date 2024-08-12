from typing import Any

import http
import json
import logging

from enum import StrEnum, auto

import requests

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.http import HttpRequest

User = get_user_model()


class Roles(StrEnum):
    def _generate_next_value_(name: str, start: int, count: int, last_values: list[Any]) -> Any:
        return name.lower()

    SUPERUSER = auto()
    ADMIN = auto()
    PREMIUM = auto()
    USER = auto()
    INCOGNITO = auto()


class AuthBackend(BaseBackend):
    def authenticate(
        self, request: HttpRequest, username: str | None = None, password: str | None = None
    ) -> Any:
        url_login = f"{settings.AUTH_API_LOGIN_URL}/auth/login"
        url_user = f"{settings.AUTH_API_LOGIN_URL}/users/"

        payload = {"login": username, "password": password}

        try:
            response = requests.post(url_login, data=json.dumps(payload), timeout=60)
        except requests.ConnectionError:
            return None

        if response.status_code != http.HTTPStatus.ACCEPTED:
            return None

        data_login = response.json()
        token = {"Authorization": f"Bearer {data_login['access_token']}"}

        resp_user_info = requests.get(url_user, headers=token, timeout=60)

        if resp_user_info.status_code != http.HTTPStatus.OK:
            return None

        data = resp_user_info.json()

        try:
            user, created = User.objects.get_or_create(id=data["id"])
            user.email = data.get("login")
            user.first_name = data.get("first_name")
            user.last_name = data.get("last_name")

            if data.get("is_active"):
                user.is_active = data.get("is_active")
            else:
                user.is_active = True

            if Roles.SUPERUSER in data.get("roles"):
                user.is_admin = True
                user.is_staff = True
            elif Roles.ADMIN in data.get("roles"):
                user.is_admin = False
                user.is_staff = True
            else:
                user.is_admin = False
                user.is_staff = False

            user.save()
        except Exception as err:
            logging.exception(err)
            return None

        return user

    def get_user(self, user_id: str) -> Any:
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
