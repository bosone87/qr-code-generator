# Логирование действий и ошибок

"""
Модуль для логирования действий и ошибок.
"""

from datetime import datetime
from config import LOG_FILE


def log_action(message: str) -> None:
    """
    Записывает сообщение в лог-файл с временной меткой.
    
    Args:
        message: Текст сообщения
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception as e:
        # Если не удалось записать в лог, выводим ошибку в консоль
        print(f"⚠️ Не удалось записать в лог: {e}")


def read_logs() -> str:
    """
    Читает содержимое лог-файла.
    
    Returns:
        Содержимое лог-файла в виде строки
    """
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Лог-файл пока пуст."
    except Exception as e:
        return f"Ошибка при чтении лога: {e}"