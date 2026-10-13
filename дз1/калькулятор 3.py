def d(a, b):
    '''сложение'''
    return a + b
def e(a, b):
    '''вычитание'''
    return a - b
def f(a, b):
    '''умножение'''
    return a * b
def g(a, b):
    '''деление'''
    if b == 0:
            return "Ошибка: деление на ноль"
    return a / b

while True:
    a=int(input("введите первое число:"))
    c=str(input("введите знак операции:"))
    b=int(input("введите второе число:"))

    if c == "+":
        print("Результат:", d(a, b))
    elif c == "-":
        print("Результат:", e(a, b))
    elif c == "*":
        print("Результат:", f(a, b))
    elif c == "/":
        if b == 0:
            print("Ошибка: деление на ноль")
        else:
            print("Результат:", g(a, b))
    else:
        print("Ошибка: неизвестная операция")
    break
