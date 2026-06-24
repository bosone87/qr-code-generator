# Валидация ввода (сгенерирована с помощью ИИ)

"""
Модуль валидации пользовательского ввода.
Сгенерирован с использованием ChatGPT.
"""

import re
from datetime import datetime
from config import MAX_TEXT_LENGTH


def validate_text(text: str) -> tuple[bool, str]:
    """
    Проверяет, что текст не пустой и не превышает максимальную длину.
    
    Args:
        text: Введённый текст
        
    Returns:
        (True, "") если валидация пройдена, иначе (False, сообщение об ошибке)
    """
    if not text or not text.strip():
        return False, "Ошибка: текст не может быть пустым."
    
    if len(text) > MAX_TEXT_LENGTH:
        return False, f"Ошибка: текст слишком длинный (максимум {MAX_TEXT_LENGTH} символов)."
    
    return True, ""


def validate_version(version: str) -> tuple[bool, int, str]:
    """
    Проверяет, что версия QR-кода — целое число от 1 до 40.
    
    Args:
        version: Строка с номером версии
        
    Returns:
        (True, version_int, "") если валидация пройдена,
        иначе (False, 0, сообщение об ошибке)
    """
    try:
        v = int(version)
        if 1 <= v <= 40:
            return True, v, ""
        else:
            return False, 0, "Ошибка: версия должна быть от 1 до 40."
    except ValueError:
        return False, 0, "Ошибка: версия должна быть целым числом."


def validate_error_correction(level: str) -> tuple[bool, str, str]:
    """
    Проверяет уровень коррекции ошибок.
    
    Args:
        level: Строка с уровнем (L, M, Q, H)
        
    Returns:
        (True, level_upper, "") если валидация пройдена,
        иначе (False, "", сообщение об ошибке)
    """
    valid_levels = {'L', 'M', 'Q', 'H'}
    level_upper = level.strip().upper()
    
    if level_upper in valid_levels:
        return True, level_upper, ""
    else:
        return False, "", f"Ошибка: допустимые уровни: {', '.join(valid_levels)}."


def validate_color(color: str) -> tuple[bool, str, str]:
    """
    Проверяет, что цвет задан корректно (название цвета или HEX).
    
    Args:
        color: Название цвета или HEX-код
        
    Returns:
        (True, color, "") если валидация пройдена,
        иначе (False, "", сообщение об ошибке)
    """
    if not color or not color.strip():
        return False, "", "Ошибка: цвет не может быть пустым."
    
    color_clean = color.strip()
    
    # Проверка на название цвета (только буквы)
    if re.match(r'^[a-zA-Z]+$', color_clean):
        return True, color_clean, ""
    
    # Проверка на HEX-код (#RGB или #RRGGBB)
    if re.match(r'^#[0-9a-fA-F]{3}$|^#[0-9a-fA-F]{6}$', color_clean):
        return True, color_clean, ""
    
    return False, "", "Ошибка: цвет должен быть названием (например, red) или HEX-кодом (например, #FF0000)."


def validate_filename(filename: str) -> tuple[bool, str, str]:
    """
    Проверяет, что имя файла корректно и не содержит недопустимых символов.
    
    Args:
        filename: Предлагаемое имя файла
        
    Returns:
        (True, filename, "") если валидация пройдена,
        иначе (False, "", сообщение об ошибке)
    """
    if not filename or not filename.strip():
        return False, "", "Ошибка: имя файла не может быть пустым."
    
    # Разрешённые символы: буквы, цифры, точка, дефис, подчёркивание
    if re.match(r'^[a-zA-Z0-9._-]+$', filename.strip()):
        return True, filename.strip(), ""
    else:
        return False, "", "Ошибка: имя файла содержит недопустимые символы."