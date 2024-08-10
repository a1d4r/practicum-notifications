from faker import Faker
from polyfactory.factories.pydantic_factory import ModelFactory

from profiles_api.schemas import UserProfile


class UserProfileFactory(ModelFactory[UserProfile]):
    __faker__ = Faker(locale="es_ES")
    __random__seed__ = 1

    @classmethod
    def first_name(cls) -> str:
        return cls.__faker__.first_name()

    @classmethod
    def last_name(cls) -> str:
        return cls.__faker__.last_name()

    @classmethod
    def email(cls) -> str:
        return cls.__faker__.email()

    @classmethod
    def timezone(cls) -> str:
        return cls.__faker__.timezone()
