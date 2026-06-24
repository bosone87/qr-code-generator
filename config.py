# Настройки по умолчанию

"""
Конфигурационные параметры генератора QR-кодов.
"""

# Параметры QR-кода по умолчанию
DEFAULT_VERSION = 1          # Размер QR-кода (1-40)
DEFAULT_ERROR_CORRECTION = 'M'  # Уровень коррекции: L, M, Q, H
DEFAULT_BOX_SIZE = 10        # Размер одного модуля в пикселях
DEFAULT_BORDER = 4           # Толщина белой рамки

# Цвета по умолчанию
DEFAULT_FILL_COLOR = 'black'
DEFAULT_BACK_COLOR = 'white'

# Максимальная длина текста для QR-кода (версия 40)
MAX_TEXT_LENGTH = 4296

# Имя файла лога
LOG_FILE = 'qr_generator.log'