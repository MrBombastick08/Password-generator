"""
Генератор Паролей - Десктопное приложение на PyQt6.

Приложение демонстрирует принципы чистого кода:
- KISS: Простой и понятный интерфейс
- YAGNI: Только необходимые функции
- Выразительный нейминг: Понятные имена переменных и методов
- Разбитие на компоненты: Отдельные методы для каждой части
- Условия раннего выхода: Валидация входных данных
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QSpinBox, QCheckBox, QPushButton, QLineEdit, QMessageBox
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon, QClipboard, QColor, QPalette
from password_generator import generate_password


class PasswordGeneratorApp(QMainWindow):
    """
    Главное окно приложения генератора паролей.
    Соблюдает принципы чистого кода через разбитие на методы.
    """
    
    def __init__(self):
        """Инициализация главного окна."""
        super().__init__()
        self.setWindowTitle("Генератор Паролей")
        self.setGeometry(100, 100, 600, 500)
        self.setMinimumSize(QSize(500, 400))
        self.setMaximumSize(QSize(700, 650))  # Максимальный размер окна
        
        # Создание интерфейса
        self.create_widgets()
        self.setup_styles()
        
    def create_widgets(self):
        """
        Создание и размещение всех виджетов.
        Разбитие на методы для улучшения читаемости.
        """
        # Главный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Главный layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Заголовок
        title = QLabel("Генератор Паролей")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        main_layout.addWidget(title)
        
        # Подзаголовок
        subtitle = QLabel("Создайте надежный пароль за несколько кликов")
        subtitle_font = QFont()
        subtitle_font.setPointSize(10)
        subtitle.setFont(subtitle_font)
        subtitle.setStyleSheet("color: #666;")
        main_layout.addWidget(subtitle)
        
        # Разделитель
        main_layout.addSpacing(10)
        
        # Секция длины пароля
        length_layout = QHBoxLayout()
        length_label = QLabel("Длина пароля:")
        length_label.setMinimumWidth(150)
        self.length_spinbox = QSpinBox()
        self.length_spinbox.setMinimum(4)
        self.length_spinbox.setMaximum(128)
        self.length_spinbox.setValue(12)
        self.length_spinbox.setMinimumWidth(80)
        self.length_spinbox.setMaximumWidth(120)
        length_layout.addWidget(length_label)
        length_layout.addWidget(self.length_spinbox)
        length_layout.addStretch()
        main_layout.addLayout(length_layout)
        
        # Секция выбора типов символов
        charset_label = QLabel("Набор символов:")
        charset_label_font = QFont()
        charset_label_font.setBold(True)
        charset_label.setFont(charset_label_font)
        main_layout.addWidget(charset_label)
        
        # Чекбоксы для типов символов
        self.lower_checkbox = QCheckBox("Строчные буквы (a-z)")
        self.lower_checkbox.setChecked(True)
        main_layout.addWidget(self.lower_checkbox)
        
        self.upper_checkbox = QCheckBox("Заглавные буквы (A-Z)")
        self.upper_checkbox.setChecked(True)
        main_layout.addWidget(self.upper_checkbox)
        
        self.digits_checkbox = QCheckBox("Цифры (0-9)")
        self.digits_checkbox.setChecked(True)
        main_layout.addWidget(self.digits_checkbox)
        
        self.punct_checkbox = QCheckBox("Спецсимволы (!@#$%...)")
        self.punct_checkbox.setChecked(False)
        main_layout.addWidget(self.punct_checkbox)
        
        # Кнопка генерации
        main_layout.addSpacing(10)
        self.generate_button = QPushButton("Сгенерировать Пароль")
        self.generate_button.setMinimumHeight(40)
        self.generate_button.clicked.connect(self.handle_generate_button)
        button_font = QFont()
        button_font.setPointSize(11)
        button_font.setBold(True)
        self.generate_button.setFont(button_font)
        main_layout.addWidget(self.generate_button)
        
        # Поле для отображения результата
        main_layout.addSpacing(10)
        result_label = QLabel("Сгенерированный пароль:")
        result_label_font = QFont()
        result_label_font.setBold(True)
        result_label.setFont(result_label_font)
        main_layout.addWidget(result_label)
        
        # Layout для пароля и кнопки копирования
        password_layout = QHBoxLayout()
        self.password_field = QLineEdit()
        self.password_field.setReadOnly(True)
        self.password_field.setMinimumHeight(40)
        self.password_field.setPlaceholderText("Пароль будет отображаться здесь")
        password_layout.addWidget(self.password_field)
        
        self.copy_button = QPushButton("Копировать")
        self.copy_button.setMaximumWidth(120)
        self.copy_button.setMinimumHeight(40)
        self.copy_button.clicked.connect(self.handle_copy_button)
        password_layout.addWidget(self.copy_button)
        
        main_layout.addLayout(password_layout)
        
        # Сообщение об успехе
        self.success_message = QLabel()
        self.success_message.setStyleSheet(
            "background-color: #d4edda; color: #155724; padding: 10px; "
            "border: 1px solid #c3e6cb; border-radius: 4px; font-weight: bold;"
        )
        self.success_message.setVisible(False)
        self.success_message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.success_message)
        
        # Растягиваемый элемент для заполнения оставшегося пространства
        main_layout.addStretch()
        
        central_widget.setLayout(main_layout)
    
    def setup_styles(self):
        """
        Установка стилей приложения.
        Создает красивый и современный внешний вид.
        """
        style = """
            QMainWindow {
                background-color: #f5f5f5;
            }
            
            QLabel {
                color: #333;
            }
            
            QSpinBox {
                padding: 5px 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
                color: #333;
                min-width: 80px;
                max-width: 120px;
            }
            
            QSpinBox::up-button, QSpinBox::down-button {
                width: 25px;
            }
            
            QCheckBox {
                color: #333;
                spacing: 8px;
            }
            
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            
            QCheckBox::indicator:unchecked {
                background-color: white;
                border: 2px solid #ddd;
                border-radius: 3px;
            }
            
            QCheckBox::indicator:checked {
                background-color: #667eea;
                border: 2px solid #667eea;
                border-radius: 3px;
                image: url(:/check);
            }
            
            QPushButton {
                background-color: #667eea;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                padding: 8px 16px;
            }
            
            QPushButton:hover {
                background-color: #5568d3;
            }
            
            QPushButton:pressed {
                background-color: #4557c0;
            }
            
            QPushButton:disabled {
                background-color: #ccc;
                color: #999;
            }
            
            #copyButton {
                background-color: #f0f0f0;
                color: #333;
                border: 1px solid #ddd;
            }
            
            #copyButton:hover {
                background-color: #e8e8e8;
                border: 1px solid #667eea;
            }
            
            QLineEdit {
                padding: 8px 12px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
                color: #333;
                font-family: "Courier New", monospace;
                font-size: 12px;
            }
            
            QLineEdit:focus {
                border: 2px solid #667eea;
            }
            
            QMessageBox QLabel {
                color: white;
            }
            
            QMessageBox {
                background-color: #333;
            }
        """
        self.setStyleSheet(style)
        self.copy_button.setObjectName("copyButton")
    
    def show_success_message(self, message: str):
        """
        Отображает сообщение об успехе в основном окне.
        """
        self.success_message.setText(message)
        self.success_message.setVisible(True)
    
    def hide_success_message(self):
        """
        Скрывает сообщение об успехе.
        """
        self.success_message.setVisible(False)
    
    def handle_generate_button(self):
        """
        Обработчик нажатия кнопки "Сгенерировать Пароль".
        Использует условие раннего выхода для валидации.
        """
        # Получение параметров из интерфейса
        length = self.length_spinbox.value()
        use_lower = self.lower_checkbox.isChecked()
        use_upper = self.upper_checkbox.isChecked()
        use_digits = self.digits_checkbox.isChecked()
        use_punct = self.punct_checkbox.isChecked()
        
        # Вызов функции генерации пароля
        success, result = generate_password(length, use_lower, use_upper, use_digits, use_punct)
        
        # Условие раннего выхода: Проверка на ошибку
        if not success:
            msg_box = QMessageBox.warning(self, "Ошибка", result)
            self.password_field.clear()
            self.hide_success_message()
            return
        
        # Отображение результата
        self.password_field.setText(result)
        self.show_success_message("✓ Пароль успешно сгенерирован!")
    
    def handle_copy_button(self):
        """
        Обработчик нажатия кнопки "Копировать".
        Копирует пароль в буфер обмена.
        """
        password = self.password_field.text()
        
        # Условие раннего выхода: Проверка наличия пароля
        if not password:
            msg_box = QMessageBox.warning(self, "Ошибка", "Нет пароля для копирования")
            self.hide_success_message()
            return
        
        # Копирование в буфер обмена
        clipboard = QApplication.clipboard()
        clipboard.setText(password)
        
        self.show_success_message("✓ Пароль скопирован в буфер обмена!")


def main():
    """Точка входа приложения."""
    app = QApplication(sys.argv)
    window = PasswordGeneratorApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
