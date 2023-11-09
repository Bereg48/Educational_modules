from rest_framework.exceptions import ValidationError
from main.validators import TitleValidator, validator_description_words
import unittest


class TestTitleValidator(unittest.TestCase):
    """Класс TestTitleValidator тестирует функциональность
    класса TitleValidator, который валидирует значение
    поля title, которое должно состоять только из букв,
    цифр и символов: точка, тире и пробел."""

    def test_valid_title(self):
        validator = TitleValidator(field='title')
        value = {'title': 'Invalid Title!'}
        with self.assertRaises(ValidationError):
            validator(value)

    def test_invalid_title(self):
        validator = TitleValidator(field='title')
        value = {'title': 'invalid_title!@#$'}
        with self.assertRaises(ValidationError):
            validator(value)


class TestDescriptionWordsValidator(unittest.TestCase):
    def test_valid_description(self):
        value = 'This is a valid description'
        self.assertIsNone(validator_description_words(value))

    def test_invalid_description(self):
        value = 'This description contains a scam word: война'
        with self.assertRaises(ValidationError):
            validator_description_words(value)
