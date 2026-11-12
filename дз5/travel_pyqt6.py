
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QComboBox, QTextEdit,
    QVBoxLayout, QHBoxLayout, QMessageBox
)
import sys


class TravelApp(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("TravelCalc - Путешествия")
        self.setGeometry(300, 150, 500, 600)

        self.price = 0

        # Заголовок
        title = QLabel("TRAVELCALC")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")

        description = QLabel("Калькулятор стоимости путешествий")

        # Выбор страны
        country_label = QLabel("Выберите страну:")
        self.country = QComboBox()
        self.country.addItems([
            "Франция", "Италия", "Испания",
            "Турция", "Япония"
        ])

        # Количество туристов
        people_label = QLabel("Количество туристов:")
        self.people = QLineEdit()
        self.people.setPlaceholderText("Введите количество")

        # Количество дней
        days_label = QLabel("Количество дней:")
        self.days = QLineEdit()
        self.days.setPlaceholderText("Введите количество дней")

        # Выбор транспорта
        transport_label = QLabel("Выберите транспорт:")
        self.transport = QComboBox()
        self.transport.addItems([
            "Самолет", "Поезд", "Автомобиль"
        ])

        # Выбор отеля
        hotel_label = QLabel("Выберите отель:")
        self.hotel = QComboBox()
        self.hotel.addItems([
            "2 звезды", "3 звезды",
            "4 звезды", "5 звезд"
        ])

        # Выбор питания
        food_label = QLabel("Выберите питание:")
        self.food = QComboBox()
        self.food.addItems([
            "Без питания", "Завтраки", "Полный пансион"
        ])

        # Кнопки
        self.calculate_button = QPushButton("Рассчитать")
        self.calculate_button.clicked.connect(self.calculate)

        self.pay_button = QPushButton("Оплатить")
        self.pay_button.clicked.connect(self.payment)

        self.clear_button = QPushButton("Очистить")
        self.clear_button.clicked.connect(self.clear)

        # Поле результатов
        result_label = QLabel("Результат:")
        self.result = QTextEdit()
        self.result.setReadOnly(True)

        # Компоновка элементов
        layout = QVBoxLayout()

        layout.addWidget(title)
        layout.addWidget(description)

        layout.addWidget(country_label)
        layout.addWidget(self.country)

        layout.addWidget(people_label)
        layout.addWidget(self.people)

        layout.addWidget(days_label)
        layout.addWidget(self.days)

        layout.addWidget(transport_label)
        layout.addWidget(self.transport)

        layout.addWidget(hotel_label)
        layout.addWidget(self.hotel)

        layout.addWidget(food_label)
        layout.addWidget(self.food)

        layout.addWidget(self.calculate_button)
        layout.addWidget(self.pay_button)
        layout.addWidget(self.clear_button)

        layout.addWidget(result_label)
        layout.addWidget(self.result)

        self.setLayout(layout)

    # Расчет стоимости путешествия
    def calculate(self):

        try:
            people = int(self.people.text())
            days = int(self.days.text())

            if people <= 0 or days <= 0:
                raise ValueError

            if people > 20 or days > 90:
                raise ValueError

        except ValueError:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Введите корректное количество туристов и дней!"
            )
            return

        # Стоимость путешествия по странам
        country_prices = {
            "Франция": 100,
            "Италия": 120,
            "Испания": 110,
            "Турция": 90,
            "Япония": 250
        }

        # Стоимость транспорта
        transport_prices = {
            "Самолет": 250,
            "Поезд": 120,
            "Автомобиль": 80
        }

        # Стоимость отеля за сутки
        hotel_prices = {
            "2 звезды": 45,
            "3 звезды": 70,
            "4 звезды": 110,
            "5 звезд": 170
        }

        # Стоимость питания за сутки
        food_prices = {
            "Без питания": 0,
            "Завтраки": 15,
            "Полный пансион": 35
        }

        country = self.country.currentText()
        transport = self.transport.currentText()
        hotel = self.hotel.currentText()
        food = self.food.currentText()

        # Расчет общей стоимости
        one_person = (
            country_prices[country]
            + transport_prices[transport]
            + (hotel_prices[hotel] + food_prices[food]) * days
        )

        self.price = one_person * people

        self.result.setText(
            f"Страна: {country}\n"
            f"Туристов: {people}\n"
            f"Количество дней: {days}\n"
            f"Транспорт: {transport}\n"
            f"Отель: {hotel}\n"
            f"Питание: {food}\n\n"
            f"Стоимость поездки: {self.price} евро"
        )

    # Имитация оплаты
    def payment(self):

        if self.price == 0:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Сначала рассчитайте стоимость путешествия!"
            )
            return

        answer = QMessageBox.question(
            self,
            "Оплата",
            f"Оплатить путешествие за {self.price} евро?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )

        if answer == QMessageBox.StandardButton.Yes:
            QMessageBox.information(
                self,
                "Оплата",
                "Оплата успешно выполнена!\n"
                "Это демонстрационная операция."
            )

    # Очистка полей
    def clear(self):

        self.people.clear()
        self.days.clear()
        self.country.setCurrentIndex(0)
        self.transport.setCurrentIndex(0)
        self.hotel.setCurrentIndex(0)
        self.food.setCurrentIndex(0)

        self.result.clear()
        self.price = 0


app = QApplication(sys.argv)

window = TravelApp()
window.show()

sys.exit(app.exec())
