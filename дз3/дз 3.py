lab = [
    [".", "C", ".", "M", "."],
    ["M", ".", "K", ".", "C"],
    [".", "C", ".", "M", "."],
    [".", ".", ".", ".", "P"],
    [".", "M", ".", "C", "."],
]

rooms = {
    ".": "пустая комната",
    "C": "комната с сундуком",
    "M": "комната с монстром",
    "K": "комната с ключом",
    "P": "комната с порталом",
}

hp = 100                
x, y = 0, 0             
has_key = False         

inventory = []
journal = []

def show_map():
    print("\n Карта лабиринта:")
    print("   " + " ".join(str(i) for i in range(5)))
    for row in range(5):
        line = f"{row} "
        for col in range(5):
            if row == y and col == x:
                line += " ! "
            else:
                line += " . "
        print(line)
    print(" (! - это ты) \n")

print("ЛАБИРИНТ")
print("Управление: w — вверх, s — вниз, a — влево, d — вправо")
print("Цель: найти ключ и уйти через портал.\n")

while True:
    show_map()
    cell = lab[y][x]

    print(f"\n Вы попали в {rooms[cell]} ")
    print(f"HP: {hp}   Позиция: ({x}, {y})")
    print(f"Инвентарь: {inventory}")

    if cell == "C":
        choice = input("Открыть сундук? (д/н): ")
        if choice == "д":
            item = {"name": "зелье", "power": 10}
            inventory.append(item)          
            print(f"Вы взяли: {item['name']}")

    elif cell == "M":
        print("Монстр атакует! Вы теряете 20 HP.")
        hp -= 20
        if hp <= 0:
            print("Вы погибли... Игра окончена.")
            break

    elif cell == "K":
        if not has_key:
            print("Тут лежит ключ от выхода!")
            has_key = True
            inventory.append({"name": "ключ", "power": 0})
            print("Ключ добавлен в инвентарь.")
        else:
            print("Ключ уже забрали.")

    elif cell == "P":
        if has_key:
            print("У вас есть ключ — вы прошли лабиринт! Победа!")
            break
        else:
            print("Портал закрыт. Сначала найдите ключ.")

    journal.append(rooms[cell])

    print("\n1 — идти")
    print("2 — выбросить предмет (pop)")
    print("3 — изменить свойства предмета")
    print("4 — добавить предметы (extend)")
    print("5 — отсортировать инвентарь (sort)")
    print("6 — развернуть инвентарь (reverse)")
    print("7 — проверить наличие предмета (in / index)")
    print("8 — показать журнал")
    print("q — выйти")

    action = input("Выбор: ")

    if action == "1":
        move = input("Куда (w/a/s/d): ")
        if move == "w" and y > 0:
            y -= 1
        elif move == "s" and y < 4:
            y += 1
        elif move == "a" and x > 0:
            x -= 1
        elif move == "d" and x < 4:
            x += 1
        else:
            print("Туда нельзя идти!")

    elif action == "2":
        if inventory:
            item = inventory.pop()          
            print(f"Вы выбросили: {item['name']}")
        else:
            print("Инвентарь пуст.")

    elif action == "3":
        if not inventory:
            print("Инвентарь пуст.")
            continue
        for i, item in enumerate(inventory):
            print(f"{i}: {item['name']} (сила = {item['power']})")
        idx = int(input("Какой предмет изменить? Номер: "))
        if 0 <= idx < len(inventory):
            new_power = int(input("Новое значение силы: "))
            inventory[idx]["power"] = new_power     
            print("Свойство изменено!")
        else:
            print("Нет такого номера.")

    elif action == "4":
        inventory.extend([
            {"name": "верёвка", "power": 1},
            {"name": "факел", "power": 2},
        ])
        print("Добавлены: верёвка, факел")

    elif action == "5":
        inventory.sort(key=lambda it: it["name"])
        print(f"Отсортировано: {[it['name'] for it in inventory]}")

    elif action == "6":
        inventory.reverse()
        print(f"Развёрнуто: {[it['name'] for it in inventory]}")

    elif action == "7":
        name = input("Какой предмет искать? ")
        if name in [it["name"] for it in inventory]:
            print(f"Да, {name} есть в инвентаре.")
            for i, it in enumerate(inventory):
                if it["name"] == name:
                    print(f"Он лежит под номером {i}")
                    break
        else:
            print("Такого предмета нет.")

    elif action == "8":
        print(f"Журнал посещений: {journal}")

    elif action == "q":
        print("Игра окончена!")
        break
    else:
        print("Неизвестная команда.")

