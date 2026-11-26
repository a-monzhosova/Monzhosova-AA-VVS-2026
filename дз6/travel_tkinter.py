import tkinter as tk
from tkinter import messagebox, ttk
import database
database.init_db()  

# Главное окно
window = tk.Tk()
window.title("TravelCalc - Путешествия")
window.geometry("500x750")

price = 0


# Заголовок
title = tk.Label(
    window,
    text="TRAVELCALC",
    font=("Arial", 22, "bold")
)
title.pack(pady=10)

description = tk.Label(
    window,
    text="Калькулятор стоимости путешествий"
)
description.pack(pady=5)

# Имя клиента
name_label = tk.Label(window, text="Имя клиента:")
name_label.pack()

name_entry = tk.Entry(window)
name_entry.pack(pady=5)

# Выбор страны
country_label = tk.Label(window, text="Выберите страну:")
country_label.pack()

country = ttk.Combobox(
    window,
    values=["Франция", "Италия", "Испания", "Турция", "Япония"],
    state="readonly"
)
country.current(0)
country.pack(pady=5)


# Количество туристов
people_label = tk.Label(window, text="Количество туристов:")
people_label.pack()

people = tk.Entry(window)
people.pack(pady=5)


# Количество дней
days_label = tk.Label(window, text="Количество дней:")
days_label.pack()

days = tk.Entry(window)
days.pack(pady=5)


# Выбор транспорта
transport_label = tk.Label(window, text="Выберите транспорт:")
transport_label.pack()

transport = ttk.Combobox(
    window,
    values=["Самолет", "Поезд", "Автомобиль"],
    state="readonly"
)
transport.current(0)
transport.pack(pady=5)


# Выбор отеля
hotel_label = tk.Label(window, text="Выберите отель:")
hotel_label.pack()

hotel = ttk.Combobox(
    window,
    values=["2 звезды", "3 звезды", "4 звезды", "5 звезд"],
    state="readonly"
)
hotel.current(0)
hotel.pack(pady=5)


# Выбор питания
food_label = tk.Label(window, text="Выберите питание:")
food_label.pack()

food = ttk.Combobox(
    window,
    values=["Без питания", "Завтраки", "Полный пансион"],
    state="readonly"
)
food.current(0)
food.pack(pady=5)


# Поле для результатов
result_label = tk.Label(
    window,
    text="Результат:",
    font=("Arial", 12, "bold")
)
result_label.pack(pady=5)

result = tk.Text(window, height=7, width=48)
result.pack(pady=5)


# Функция расчета
def calculate():

    global price

    try:
        people_count = int(people.get())
        days_count = int(days.get())

        if people_count <= 0 or days_count <= 0:
            raise ValueError

        if people_count > 20 or days_count > 90:
            raise ValueError

    except ValueError:
        messagebox.showwarning(
            "Ошибка",
            "Введите корректное количество туристов и дней!"
        )
        return

    # Цены стран
    country_prices = {
        "Франция": 100,
        "Италия": 120,
        "Испания": 110,
        "Турция": 90,
        "Япония": 250
    }

    # Цены транспорта
    transport_prices = {
        "Самолет": 250,
        "Поезд": 120,
        "Автомобиль": 80
    }

    # Цены отелей
    hotel_prices = {
        "2 звезды": 45,
        "3 звезды": 70,
        "4 звезды": 110,
        "5 звезд": 170
    }

    # Цены питания
    food_prices = {
        "Без питания": 0,
        "Завтраки": 15,
        "Полный пансион": 35
    }

    selected_country = country.get()
    selected_transport = transport.get()
    selected_hotel = hotel.get()
    selected_food = food.get()

    # Расчет стоимости одного человека
    one_person = (
        country_prices[selected_country]
        + transport_prices[selected_transport]
        + (hotel_prices[selected_hotel]
           + food_prices[selected_food]) * days_count
    )

    # Общая стоимость
    price = one_person * people_count

    result.delete("1.0", tk.END)

    result.insert(
        tk.END,
        f"Страна: {selected_country}\n"
        f"Туристов: {people_count}\n"
        f"Количество дней: {days_count}\n"
        f"Транспорт: {selected_transport}\n"
        f"Отель: {selected_hotel}\n"
        f"Питание: {selected_food}\n\n"
        f"Стоимость поездки: {price} евро"
    )


# Функция оплаты
def payment():
    if price == 0:
        messagebox.showwarning(
            "Ошибка", "Сначала рассчитайте стоимость путешествия!"
        )
        return

    customer_name = name_entry.get().strip()
    if not customer_name:
        messagebox.showwarning("Ошибка", "Введите имя клиента перед оплатой!")
        return

    answer = messagebox.askyesno(
        "Оплата", f"Оплатить путешествие на имя {customer_name} за {price} евро?"
    )

    if answer:
        database.save_booking(
            customer_name=customer_name,
            country=country.get(),
            people_count=int(people.get()),
            days_count=int(days.get()),
            transport=transport.get(),
            hotel=hotel.get(),
            food=food.get(),
            total_price=price,
        )

        messagebox.showinfo(
            "Оплата",
            "Оплата успешно выполнена!\nКлиент и заказ сохранены в базу данных.",
        )


# Функция очистки
def clear():

    global price

    name_entry.delete(0, tk.END)
    people.delete(0, tk.END)
    days.delete(0, tk.END)

    country.current(0)
    transport.current(0)
    hotel.current(0)
    food.current(0)

    result.delete("1.0", tk.END)

    price = 0

    #Функция просмотра истории заказов из БД
def show_history():
    history_win = tk.Toplevel(window)
    history_win.title("История оплаченных туров")
    history_win.geometry("880x300")

    columns = ("id", "customer", "country", "people", "days", "transport", "hotel", "food", "price")
    tree = ttk.Treeview(history_win, columns=columns, show="headings")

    headings = {
        "id": "№",
        "customer": "Клиент",
        "country": "Страна",
        "people": "Туристы",
        "days": "Дни",
        "transport": "Транспорт",
        "hotel": "Отель",
        "food": "Питание",
        "price": "Цена (€)"
    }

    for col, text in headings.items():
        tree.heading(col, text=text)
        tree.column(col, width=90, anchor="center")
    tree.column("id", width=40)
    tree.column("customer", width=130)

    for row in database.get_all_bookings():
        tree.insert("", tk.END, values=row)

    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)


# Кнопки
calculate_button = tk.Button(
    window,
    text="Рассчитать",
    width=20,
    command=calculate
)
calculate_button.pack(pady=5)

pay_button = tk.Button(
    window,
    text="Оплатить",
    width=20,
    command=payment
)
pay_button.pack(pady=5)

clear_button = tk.Button(
    window,
    text="Очистить",
    width=20,
    command=clear
)
clear_button.pack(pady=5)

history_button = tk.Button(
    window,
    text="История заказов",
    width=20,
    command=show_history
)
history_button.pack(pady=5)

# Запуск приложения
window.mainloop()