import re
from rest_framework.serializers import ValidationError

SCAM_WORDS = ['война', 'казино', 'продам']


class TitleValidator:
    """Класс TitleValidator представляет собой валидатор
    для проверки значения поля title которое должно состоять
    только из букв, цифр и символов: точка, тире и пробел."""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        reg = re.compile('^[a-zA-Z0-9\,\-\.\ ]+$')
        tmp_val = value.get(self.field)  # Получение значения поля title из словаря
        if not bool(reg.match(tmp_val)):
            raise ValidationError('Title is not ok')
        return None


def validator_description_words(value):
    if set(value.lower().split()) & set(SCAM_WORDS):
        raise ValidationError('Использованы запрещенные слова!')
    return None
