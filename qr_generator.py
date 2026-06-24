# Логика генерации и сохранения QR-кода

"""
Модуль для генерации и сохранения QR-кодов.
"""
from __future__ import annotations

import qrcode
from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H
from datetime import datetime
import os
from logger import log_action
from config import (
    DEFAULT_VERSION,
    DEFAULT_ERROR_CORRECTION,
    DEFAULT_BOX_SIZE,
    DEFAULT_BORDER,
    DEFAULT_FILL_COLOR,
    DEFAULT_BACK_COLOR
)

# Сопоставление уровней коррекции с константами библиотеки
ERROR_CORRECTION_MAP = {
    'L': ERROR_CORRECT_L,
    'M': ERROR_CORRECT_M,
    'Q': ERROR_CORRECT_Q,
    'H': ERROR_CORRECT_H,
}


def generate_qr_code(
    data: str,
    version: int = DEFAULT_VERSION,
    error_correction: str = DEFAULT_ERROR_CORRECTION,
    box_size: int = DEFAULT_BOX_SIZE,
    border: int = DEFAULT_BORDER,
    fill_color: str = DEFAULT_FILL_COLOR,
    back_color: str = DEFAULT_BACK_COLOR
) -> qrcode.image.pil.PilImage:
    """
    Генерирует QR-код на основе переданных данных и параметров.
    
    Args:
        data: Текст или URL для кодирования
        version: Версия QR-кода (1-40)
        error_correction: Уровень коррекции (L, M, Q, H)
        box_size: Размер модуля в пикселях
        border: Толщина рамки
        fill_color: Цвет кода
        back_color: Цвет фона
        
    Returns:
        Объект изображения QR-кода
    """
    # Получаем константу уровня коррекции
    ec_level = ERROR_CORRECTION_MAP.get(error_correction.upper(), ERROR_CORRECT_M)
    
    # Создаём объект QR-кода
    qr = qrcode.QRCode(
        version=version,
        error_correction=ec_level,
        box_size=box_size,
        border=border,
    )
    
    # Добавляем данные
    qr.add_data(data)
    qr.make(fit=True)
    
    # Создаём изображение
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    
    return img


def get_unique_filename(base_name: str = "qr_code", extension: str = ".png") -> str:
    """
    Генерирует уникальное имя файла с временной меткой.
    При конфликте добавляет индекс.
    
    Args:
        base_name: Базовое имя файла
        extension: Расширение файла
        
    Returns:
        Уникальное имя файла
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{base_name}_{timestamp}{extension}"
    
    # Проверяем, существует ли файл, и добавляем индекс при необходимости
    counter = 1
    while os.path.exists(filename):
        filename = f"{base_name}_{timestamp}_{counter}{extension}"
        counter += 1
    
    return filename


def save_qr_code(img: qrcode.image.pil.PilImage, filename: str) -> bool:
    """
    Сохраняет QR-код в файл.
    
    Args:
        img: Объект изображения QR-кода
        filename: Имя файла для сохранения
        
    Returns:
        True если сохранение успешно, иначе False
    """
    try:
        img.save(filename)
        log_action(f"QR-код сохранён в файл: {filename}")
        return True
    except Exception as e:
        error_msg = f"Ошибка при сохранении файла {filename}: {e}"
        log_action(error_msg)
        print(f"❌ {error_msg}")
        return False