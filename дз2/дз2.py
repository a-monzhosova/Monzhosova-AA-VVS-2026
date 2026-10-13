def level_1():
    print("\nВыберите операцию: upper(), lower(), capitalize()")
    text = input("Введите ваш текст: ")
    app = input("Введите операцию: ")

    if app == "upper()":
        return text.upper()
    elif app == "lower()":
        return text.lower()
    elif app == "capitalize()":
        return text.capitalize()
    else:
        return "Неверный метод"

def level_2():
    print("\nВыберите операцию: find(), replace(), count(), index()")
    text = input("Введите ваш текст: ")
    app = input("Введите операцию: ")

    if app == "find()":
        search = input("Что искать? ")
        return text.find(search)
    elif app == "replace()":
        old = input("Что заменить? ")
        new = input("На что заменить? ")
        return text.replace(old, new)
    elif app == "count()":
        search = input("Что посчитать? ")
        return text.count(search)
    elif app == "index()":
        search = input("Что найти? ")
        return text.index(search)
    else:
        return "Неверный метод"

def level_3():
    print("\nВыберите операцию: split(), join()")
    text = input("Введите ваш текст: ")
    app = input("Введите операцию: ")

    if app == "split()":
        sep = input("Введите разделитель (если пробел, нажмите Enter): ")
        if sep == "":
            return text.split()  
        else:
            return text.split(sep)
    elif app == "join()":
        sep = input("Введите разделитель для склейки (например, пробел): ")
        words = text.split()  
        return sep.join(words) 
    else:
        return "Неверный метод"

def level_4():
    print("\nВыберите операцию: isdigit(), isalpha(), strip(), format(), reverse(r), lower(l), upper(f)")
    text = input("Введите ваш текст: ")
    app = input("Введите операцию: ")

    if app == "isdigit()":
        return text.isdigit()
    elif app == "isalpha()":
        return text.isalpha()
    elif app == "strip()":
        return text.strip()
    elif app == "format()":
        return text.format()
    elif app == "r":  
        return text[::-1] 
    elif app == "l":
        return text.lower()
    elif app == "f":
        return text.upper()
    else:
        return "Неверный метод"

def level_5():
    print("\nКомплексное преобразование строки")
    text = input("Введите ваш текст: ")
    
    text = text.strip().capitalize()
    text = text.replace(';', ' ')
    text = text.replace('-', ' ')
    text = text.replace('+', ' ')
    words = text.split()
    
    return ' '.join(words)

x = int(input("Выберите уровень от 1 до 5: "))

if x == 1:
    result = level_1()
elif x == 2:
    result = level_2()
elif x == 3:
    result = level_3()
elif x == 4:
    result = level_4()
elif x == 5:
    result = level_5()
else:
    result = "Неверный уровень"

print("\nРезультат:", result)
