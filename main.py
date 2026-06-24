# Точка входа, консольное меню

"""
Главный модуль программы — консольный интерфейс генератора QR-кодов.
"""

import os
import sys
from validator import (
    validate_text,
    validate_version,
    validate_error_correction,
    validate_color,
    validate_filename,
)
from qr_generator import generate_qr_code, save_qr_code, get_unique_filename
from logger import log_action, read_logs
from config import (
    DEFAULT_VERSION,
    DEFAULT_ERROR_CORRECTION,
    DEFAULT_BOX_SIZE,
    DEFAULT_BORDER,
    DEFAULT_FILL_COLOR,
    DEFAULT_BACK_COLOR,
)


def clear_screen():
    """Очищает экран консоли."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_menu():
    """Выводит главное меню."""
    print("\n" + "=" * 50)
    print("          ГЕНЕРАТОР QR-КОДОВ")
    print("=" * 50)
    print("1. Ввести данные для кодирования")
    print("2. Настроить параметры генерации")
    print("3. Сгенерировать и сохранить QR-код")
    print("4. Просмотреть историю (лог)")
    print("5. Выйти")
    print("=" * 50)


def main():
    """Основной цикл программы."""
    # Инициализация переменных
    data = ""
    version = DEFAULT_VERSION
    error_correction = DEFAULT_ERROR_CORRECTION
    box_size = DEFAULT_BOX_SIZE
    border = DEFAULT_BORDER
    fill_color = DEFAULT_FILL_COLOR
    back_color = DEFAULT_BACK_COLOR
    data_set = False
    
    log_action("Программа запущена")
    
    while True:
        clear_screen()
        print_menu()
        
        # Отображаем текущие параметры
        print(f"\n📌 Текущие параметры:")
        print(f"   Данные: {'✅ заданы' if data_set else '❌ не заданы'}")
        print(f"   Версия: {version}")
        print(f"   Уровень коррекции: {error_correction}")
        print(f"   Размер модуля: {box_size}")
        print(f"   Цвет кода: {fill_color}")
        print(f"   Цвет фона: {back_color}")
        
        choice = input("\nВыберите пункт меню: ").strip()
        
        # === Пункт 1: Ввод данных ===
        if choice == "1":
            print("\n--- Ввод данных для QR-кода ---")
            text = input("Введите текст или URL: ").strip()
            
            is_valid, error_msg = validate_text(text)
            if is_valid:
                data = text
                data_set = True
                log_action(f"Введены данные: {data[:50]}..." if len(data) > 50 else f"Введены данные: {data}")
                print(f"✅ Данные сохранены: {data}")
            else:
                print(f"❌ {error_msg}")
                log_action(f"Ошибка валидации данных: {error_msg}")
            
            input("\nНажмите Enter для продолжения...")
        
        # === Пункт 2: Настройка параметров ===
        elif choice == "2":
            print("\n--- Настройка параметров генерации ---")
            
            # Версия
            v_input = input(f"Введите версию (1-40, текущая: {version}): ").strip()
            if v_input:
                is_valid, v, error_msg = validate_version(v_input)
                if is_valid:
                    version = v
                    log_action(f"Установлена версия: {version}")
                else:
                    print(f"❌ {error_msg}")
            
            # Уровень коррекции
            ec_input = input(f"Введите уровень коррекции (L, M, Q, H, текущий: {error_correction}): ").strip()
            if ec_input:
                is_valid, ec, error_msg = validate_error_correction(ec_input)
                if is_valid:
                    error_correction = ec
                    log_action(f"Установлен уровень коррекции: {error_correction}")
                else:
                    print(f"❌ {error_msg}")
            
            # Размер модуля
            bs_input = input(f"Введите размер модуля (целое число, текущий: {box_size}): ").strip()
            if bs_input:
                try:
                    bs = int(bs_input)
                    if bs > 0:
                        box_size = bs
                        log_action(f"Установлен размер модуля: {box_size}")
                    else:
                        print("❌ Размер должен быть положительным числом.")
                except ValueError:
                    print("❌ Размер должен быть целым числом.")
            
            # Цвет кода
            fc_input = input(f"Введите цвет кода (текущий: {fill_color}): ").strip()
            if fc_input:
                is_valid, fc, error_msg = validate_color(fc_input)
                if is_valid:
                    fill_color = fc
                    log_action(f"Установлен цвет кода: {fill_color}")
                else:
                    print(f"❌ {error_msg}")
            
            # Цвет фона
            bc_input = input(f"Введите цвет фона (текущий: {back_color}): ").strip()
            if bc_input:
                is_valid, bc, error_msg = validate_color(bc_input)
                if is_valid:
                    back_color = bc
                    log_action(f"Установлен цвет фона: {back_color}")
                else:
                    print(f"❌ {error_msg}")
            
            input("\nНажмите Enter для продолжения...")
        
        # === Пункт 3: Генерация и сохранение ===
        elif choice == "3":
            print("\n--- Генерация QR-кода ---")
            
            if not data_set:
                print("❌ Сначала введите данные для кодирования (пункт 1).")
                input("\nНажмите Enter для продолжения...")
                continue
            
            print(f"📝 Данные для кодирования: {data}")
            print(f"⚙️  Параметры: версия={version}, коррекция={error_correction}, размер={box_size}")
            
            # Генерируем QR-код
            try:
                img = generate_qr_code(
                    data=data,
                    version=version,
                    error_correction=error_correction,
                    box_size=box_size,
                    border=border,
                    fill_color=fill_color,
                    back_color=back_color,
                )
                log_action(f"QR-код сгенерирован для данных: {data[:50]}..." if len(data) > 50 else f"QR-код сгенерирован для данных: {data}")
                print("✅ QR-код успешно сгенерирован!")
            except Exception as e:
                error_msg = f"Ошибка при генерации QR-кода: {e}"
                log_action(error_msg)
                print(f"❌ {error_msg}")
                input("\nНажмите Enter для продолжения...")
                continue
            
            # Сохраняем в файл
            filename = get_unique_filename()
            print(f"\n💾 Будет создан файл: {filename}")
            
            if save_qr_code(img, filename):
                print(f"✅ QR-код сохранён в файл: {filename}")
                log_action(f"Файл сохранён: {filename}")
            else:
                print("❌ Не удалось сохранить файл.")
            
            input("\nНажмите Enter для продолжения...")
        
        # === Пункт 4: Просмотр истории ===
        elif choice == "4":
            print("\n--- История операций ---")
            logs = read_logs()
            print(logs)
            input("\nНажмите Enter для продолжения...")
        
        # === Пункт 5: Выход ===
        elif choice == "5":
            log_action("Программа завершена")
            print("\n👋 До свидания!")
            sys.exit(0)
        
        # === Неверный выбор ===
        else:
            print("❌ Неверный пункт меню. Попробуйте снова.")
            log_action(f"Неверный выбор меню: {choice}")
            input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    main()