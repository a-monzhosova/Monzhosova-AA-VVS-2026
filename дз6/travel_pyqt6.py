import sys
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
import database

database.init_db()


class TravelApp(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("TravelCalc - Путешествия")
        self.setGeometry(300, 100, 500, 680)

        self.price = 0

        # Заголовок
        title = QLabel("TRAVELCALC")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")

        description = QLabel("Калькулятор стоимости путешествий")

        # Имя клиента
        name_label = QLabel("Имя клиента:")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите имя клиента")

        # Выбор страны
        country_label = QLabel("Выберите страну:")
        self.country = QComboBox()
        self.country.addItems(
            ["Франция", "Италия", "Испания", "Турция", "Япония"]
        )

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
        self.transport.addItems(["Самолет", "Поезд", "Автомобиль"])

        # Выбор отеля
        hotel_label = QLabel("Выберите отель:")
        self.hotel = QComboBox()
        self.hotel.addItems(["2 звезды", "3 звезды", "4 звезды", "5 звезд"])

        # Выбор питания
        food_label = QLabel("Выберите питание:")
        self.food = QComboBox()
        self.food.addItems(["Без питания", "Завтраки", "Полный пансион"])

        # Кнопки
        self.calculate_button = QPushButton("Рассчитать")
        self.calculate_button.clicked.connect(self.calculate)

        self.pay_button = QPushButton("Оплатить")
        self.pay_button.clicked.connect(self.payment)

        self.clear_button = QPushButton("Очистить")
        self.clear_button.clicked.connect(self.clear)

        self.history_button = QPushButton("История заказов")
        self.history_button.clicked.connect(self.show_history)

        # Поле результатов
        result_label = QLabel("Результат:")
        self.result = QTextEdit()
        self.result.setReadOnly(True)

        # Компоновка элементов
        layout = QVBoxLayout()

        layout.addWidget(title)
        layout.addWidget(description)

        layout.addWidget(name_label)
        layout.addWidget(self.name_input)

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
        layout.addWidget(self.history_button)

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
            QMessageBox.warning(self, "Ошибка", "Введите корректное количество туристов и дней!"
            )
            return

        # Стоимость путешествия по странам
        country_prices = {
            "Франция": 100,
            "Италия": 120,
            "Испания": 110,
            "Турция": 90,
            "Япония": 250,
        }

        # Стоимость транспорта
        transport_prices = {"Самолет": 250, "Поезд": 120, "Автомобиль": 80}

        # Стоимость отеля за сутки
        hotel_prices = {
            "2 звезды": 45,
            "3 звезды": 70,
            "4 звезды": 110,
            "5 звезд": 170,
        }

        # Стоимость питания за сутки
        food_prices = {"Без питания": 0, "Завтраки": 15, "Полный пансион": 35}

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

    # Оплата и сохранение в БД
    def payment(self):
        if self.price == 0:
            QMessageBox.warning(
                self, "Ошибка", "Сначала рассчитайте стоимость путешествия!"
            )
            return

        customer_name = self.name_input.text().strip()
        if not customer_name:
            QMessageBox.warning(
                self, "Ошибка", "Введите имя клиента перед оплатой!"
            )
            return

        answer = QMessageBox.question(
            self,
            "Оплата",
            f"Оплатить путешествие на имя {customer_name} за {self.price} евро?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if answer == QMessageBox.StandardButton.Yes:
            database.save_booking(
                customer_name=customer_name,
                country=self.country.currentText(),
                people_count=int(self.people.text()),
                days_count=int(self.days.text()),
                transport=self.transport.currentText(),
                hotel=self.hotel.currentText(),
                food=self.food.currentText(),
                total_price=self.price,
            )

            QMessageBox.information(
                self,
                "Оплата",
                "Оплата успешно выполнена!\nКлиент и заказ сохранены в базу данных.",
            )

    # Очистка полей
    def clear(self):
        self.name_input.clear()
        self.people.clear()
        self.days.clear()
        self.country.setCurrentIndex(0)
        self.transport.setCurrentIndex(0)
        self.hotel.setCurrentIndex(0)
        self.food.setCurrentIndex(0)

        self.result.clear()
        self.price = 0

    # Просмотр истории заказов из БД
    def show_history(self):
        self.history_win = QWidget()
        self.history_win.setWindowTitle("История оплаченных туров")
        self.history_win.resize(880, 320)

        bookings = database.get_all_bookings()

        table = QTableWidget(len(bookings), 9)
        table.setHorizontalHeaderLabels([
            "№",
            "Клиент",
            "Страна",
            "Туристы",
            "Дни",
            "Транспорт",
            "Отель",
            "Питание",
            "Цена (€)",
        ])

        for row_idx, row_data in enumerate(bookings):
            for col_idx, value in enumerate(row_data):
                table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

        table.resizeColumnsToContents()
        history_layout = QVBoxLayout()
        history_layout.addWidget(table)
        self.history_win.setLayout(history_layout)
        self.history_win.show()


app = QApplication(sys.argv)

window = TravelApp()
window.show()

sys.exit(app.exec())