from faker import Faker
from faker.providers.python import Provider

from app.configs.note_config import NoteConfig

ISO_8601_REGEX = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'

provider = Provider(Faker())


def generate_string(min_length, max_length=None):
    return provider.pystr(
        min_length, max_length if max_length is not None else min_length
    )


class ValidJSON:
    @staticmethod
    def min_title():
        return {'title': generate_string(NoteConfig.title_min_length)}

    @staticmethod
    def max_values():
        return {
            'title': generate_string(NoteConfig.title_min_length),
            'body': generate_string(NoteConfig.body_max_length),
        }


class InvalidJSON:
    @staticmethod
    def too_short_title():
        return {'title': generate_string(NoteConfig.title_min_length - 1)}

    @staticmethod
    def too_long_title():
        return {'title': generate_string(NoteConfig.body_max_length + 1)}

    @staticmethod
    def too_long_body():
        return {
            'title': generate_string(NoteConfig.title_max_length),
            'body': generate_string(NoteConfig.body_max_length + 1),
        }

    @staticmethod
    def invalid_title_type():
        return {'title': 0}

    @staticmethod
    def invalid_body_type():
        return {
            'title': generate_string(NoteConfig.title_min_length),
            'body': 0,
        }
