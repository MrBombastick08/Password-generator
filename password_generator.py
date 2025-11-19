"""
Модуль для генерации паролей.
Соблюдает принципы чистого кода: KISS, YAGNI, выразительный нейминг, условия раннего выхода.
"""

import random
import string

# Константы для наборов символов
LOWERCASE_CHARS = string.ascii_lowercase
UPPERCASE_CHARS = string.ascii_uppercase
DIGIT_CHARS = string.digits
PUNCTUATION_CHARS = "!@#$%^&*()_+-=[]{}|;:,.<>?"


def generate_password(
    length: int,
    use_lower: bool,
    use_upper: bool,
    use_digits: bool,
    use_punct: bool
) -> tuple[bool, str]:
    """
    Генерирует пароль на основе заданных параметров.
    
    Использует условие раннего выхода для валидации входных данных.
    
    Args:
        length: Длина пароля
        use_lower: Использовать строчные буквы
        use_upper: Использовать заглавные буквы
        use_digits: Использовать цифры
        use_punct: Использовать спецсимволы
    
    Returns:
        Кортеж (успех, результат), где результат - пароль или сообщение об ошибке
    """
    
    # Условие раннего выхода 1: Некорректная длина
    if length < 4:
        return False, "Ошибка: Длина пароля должна быть не менее 4 символов."
    
    if length > 128:
        return False, "Ошибка: Максимальная длина пароля - 128 символов."
    
    # Собираем набор символов на основе выбора пользователя
    character_set = ""
    if use_lower:
        character_set += LOWERCASE_CHARS
    if use_upper:
        character_set += UPPERCASE_CHARS
    if use_digits:
        character_set += DIGIT_CHARS
    if use_punct:
        character_set += PUNCTUATION_CHARS
    
    # Условие раннего выхода 2: Не выбран ни один тип символов
    if not character_set:
        return False, "Ошибка: Необходимо выбрать хотя бы один тип символов."
    
    # Генерируем пароль
    password = "".join(random.choice(character_set) for _ in range(length))
    
    return True, password
