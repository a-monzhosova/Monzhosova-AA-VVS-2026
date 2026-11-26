import sqlite3

DB_NAME = "travel.db"

def init_db():
    """Создаёт две связанные таблицы: customers и bookings."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Включаем проверку внешних ключей
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 1. Таблица клиентов
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL UNIQUE
        );
    """)

    # 2. Таблица бронирований (связана с customers через FOREIGN KEY)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            country TEXT NOT NULL,
            people_count INTEGER NOT NULL CHECK (people_count > 0),
            days_count INTEGER NOT NULL CHECK (days_count > 0),
            transport TEXT NOT NULL,
            hotel TEXT NOT NULL,
            food TEXT NOT NULL,
            total_price INTEGER NOT NULL CHECK (total_price > 0),
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        );
    """)

    conn.commit()
    conn.close()

def save_booking(
    customer_name,
    country,
    people_count,
    days_count,
    transport,
    hotel,
    food,
    total_price,
):
    """Сохраняет клиента (если его ещё нет) и записывает заказ в таблицу bookings."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Проверяем, есть ли уже такой клиент в таблице customers
    cursor.execute(
        "SELECT id FROM customers WHERE full_name = ?", (customer_name,)
    )
    row = cursor.fetchone()

    if row:
        customer_id = row[0]  # Берём ID существующего клиента
    else:
        cursor.execute(
            "INSERT INTO customers (full_name) VALUES (?)", (customer_name,)
        )
        customer_id = (
            cursor.lastrowid
        )  # Получаем ID только что добавленного клиента

    # Сохраняем бронирование с привязкой к customer_id
    cursor.execute(
        """
        INSERT INTO bookings (customer_id, country, people_count, days_count, transport, hotel, food, total_price)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            customer_id,
            country,
            people_count,
            days_count,
            transport,
            hotel,
            food,
            total_price,
        ),
    )

    conn.commit()
    conn.close()

def get_all_bookings():
    """Объединяет таблицы bookings и customers через JOIN для вывода в историю."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            bookings.id,
            customers.full_name,
            bookings.country,
            bookings.people_count,
            bookings.days_count,
            bookings.transport,
            bookings.hotel,
            bookings.food,
            bookings.total_price
        FROM bookings
        JOIN customers ON bookings.customer_id = customers.id
        ORDER BY bookings.id DESC
    """)
    rows = cursor.fetchall()

    conn.close()
    return rows