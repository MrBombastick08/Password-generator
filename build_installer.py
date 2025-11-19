"""
Скрипт для сборки Windows установщика с помощью PyInstaller и NSIS.
Создает exe файл и установщик с ярлыком на рабочем столе.
"""

import os
import sys
import subprocess
import shutil


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


def build_exe():
    """Сборка exe файла с помощью PyInstaller."""
    command = (
        "pyinstaller --onefile --windowed --name PasswordGenerator "
        "--icon=icon.ico --add-data password_generator.py:. "
        "main.py"
    )
    return run_command(command, "Сборка exe файла")


def create_installer_script():
    """Создание NSIS скрипта для установщика."""
    nsis_script = """
; NSIS Installer Script for Password Generator
; Скрипт установщика для Генератора Паролей

!include "MUI2.nsh"
!include "x64.nsh"

; Основные параметры
Name "Генератор Паролей"
OutFile "PasswordGeneratorSetup.exe"
InstallDir "$PROGRAMFILES\\PasswordGenerator"
InstallDirRegKey HKCU "Software\\PasswordGenerator" "Install_Dir"

; MUI Settings
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_LANGUAGE "Russian"

; Секция установки
Section "Install"
    SetOutPath "$INSTDIR"
    
    ; Копируем exe файл
    File "dist\\PasswordGenerator.exe"
    
    ; Создаем ярлык на рабочем столе
    CreateShortCut "$DESKTOP\\Генератор Паролей.lnk" "$INSTDIR\\PasswordGenerator.exe"
    
    ; Создаем ярлык в меню Пуск
    CreateDirectory "$SMPROGRAMS\\PasswordGenerator"
    CreateShortCut "$SMPROGRAMS\\PasswordGenerator\\Генератор Паролей.lnk" "$INSTDIR\\PasswordGenerator.exe"
    CreateShortCut "$SMPROGRAMS\\PasswordGenerator\\Удалить.lnk" "$INSTDIR\\uninstall.exe"
    
    ; Сохраняем путь установки в реестр
    WriteRegStr HKCU "Software\\PasswordGenerator" "Install_Dir" "$INSTDIR"
    
    ; Создаем uninstall exe
    WriteUninstaller "$INSTDIR\\uninstall.exe"
SectionEnd

; Секция удаления
Section "Uninstall"
    ; Удаляем exe файл
    Delete "$INSTDIR\\PasswordGenerator.exe"
    Delete "$INSTDIR\\uninstall.exe"
    RMDir "$INSTDIR"
    
    ; Удаляем ярлыки
    Delete "$DESKTOP\\Генератор Паролей.lnk"
    Delete "$SMPROGRAMS\\PasswordGenerator\\Генератор Паролей.lnk"
    Delete "$SMPROGRAMS\\PasswordGenerator\\Удалить.lnk"
    RMDir "$SMPROGRAMS\\PasswordGenerator"
    
    ; Удаляем ключ реестра
    DeleteRegKey HKCU "Software\\PasswordGenerator"
SectionEnd
"""
    
    with open("installer.nsi", "w", encoding="utf-8") as f:
        f.write(nsis_script)
    
    print("✓ NSIS скрипт создан: installer.nsi")


def main():
    """Главная функция сборки."""
    print("\n" + "="*60)
    print("Сборка установщика для Генератора Паролей")
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
    
    # Создание NSIS скрипта
    create_installer_script()
    
    print("\n" + "="*60)
    print("✓ Подготовка завершена!")
    print("="*60)
    print("\nДля создания установщика (.exe):")
    print("1. Установите NSIS: https://nsis.sourceforge.io/")
    print("2. Запустите: makensis installer.nsi")
    print("\nРезультаты:")
    print("- dist/PasswordGenerator.exe - портативное приложение")
    print("- PasswordGeneratorSetup.exe - установщик (после NSIS)")


if __name__ == "__main__":
    main()
