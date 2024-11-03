import re
from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsPriceCorrect(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        match = re.match(r"^(-?\d+(\.\d+)?)[ ](-?\d+(\.\d+)?)$", message.text)

        if match:
            first_number = float(match.group(1))
            second_number = float(match.group(3))
            return first_number < second_number
        return False


class IsCityNameCorrect(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if bool(re.fullmatch(r"[a-zA-Z\s-]+|[а-яА-ЯёЁ\s-]+", message.text)):
            return True
        return False


class IsDigitCorrectFilter(BaseFilter):
    """
     проверка message.text на числа и значение в диапозоне от 1 до 25
    """

    def __init__(self, num1, num2):
        super().__init__()
        self.num1 = num1
        self.num2 = num2

    async def __call__(self, message: Message) -> bool:
        if re.fullmatch(r'\d+', message.text):
            number = int(message.text)
            return self.num1 <= number <= self.num2
        return False
