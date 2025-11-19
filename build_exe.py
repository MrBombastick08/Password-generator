"""
Простой скрипт для сборки exe файла с помощью PyInstaller.
Создает портативное приложение и ярлык на рабочем столе.
"""

import os
import sys
import subprocess
import json


def run_command(command, description):
    """
    Выполняет команду и выводит результат.
    
    Args:
        command: Команда для выполнения
        description: Описание операции
    """
    print(f"\n{'='*60}")
    print(f"▶ {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, shell=True, check=True)
        print(f"✓ {description} - успешно!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Ошибка при {description}: {e}")
        return False


def create_shortcut_script():
    """Создание скрипта для создания ярлыка на рабочем столе."""
    vbs_script = """
' Скрипт для создания ярлыка на рабочем столе
Set objShell = CreateObject("WScript.Shell")
strDesktop = objShell.SpecialFolders("Desktop")
Set objLink = objShell.CreateShortCut(strDesktop & "\\Генератор Паролей.lnk")
objLink.TargetPath = "PasswordGenerator.exe"
objLink.Description = "Генератор Паролей"
objLink.WorkingDirectory = objShell.CurrentDirectory
objLink.Save
"""
    
    with open("create_shortcut.vbs", "w", encoding="utf-8") as f:
        f.write(vbs_script)
    
    print("✓ Скрипт для создания ярлыка создан: create_shortcut.vbs")


def build_exe():
    """Сборка exe файла с помощью PyInstaller."""
    command = (
        "pyinstaller --onefile --windowed "
        "--name PasswordGenerator "
        "--distpath . "
        "main.py"
    )
    return run_command(command, "Сборка exe файла")


def main():
    """Главная функция сборки."""
    print("\n" + "="*60)
    print("Сборка приложения Генератор Паролей")
    print("="*60)
    
    # Проверяем наличие PyInstaller
    try:
        import PyInstaller
    except ImportError:
        print("✗ PyInstaller не установлен!")
        print("Установите его: pip install pyinstaller")
        sys.exit(1)
    
    # Сборка exe файла
    if not build_exe():
        sys.exit(1)
    
    # Создание скрипта для ярлыка
    create_shortcut_script()
    
    print("\n" + "="*60)
    print("✓ Сборка завершена!")
    print("="*60)
    print("\nРезультаты:")
    print("- PasswordGenerator.exe - готовое приложение")
    print("- create_shortcut.vbs - скрипт для создания ярлыка")
    print("\nДля создания ярлыка на рабочем столе:")
    print("1. Поместите PasswordGenerator.exe в нужную папку")
    print("2. Запустите create_shortcut.vbs")
    print("3. На рабочем столе появится ярлык 'Генератор Паролей'")


if __name__ == "__main__":
    main()
