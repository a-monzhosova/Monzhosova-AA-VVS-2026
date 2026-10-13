import math
class Calculator:
    def add (self, a, b):
        return a + b
        
    def subtract (self, a, b):
        return a - b
        
    def multiply (self, a, b):
        return a * b
    
    def divide (self, a, b):
        if b == 0:
            return "Ошибка: деление на ноль"
        return a / b
        
    def power (self, a, b):
        return a ** b
        
    def square_root(self, a):
        if a < 0:
            return "Ошибка: извлечение корня из отрицательного числа"
        return math.sqrt(a)
        
    def percent (self, a, b):
        return a * b / 100
        
    def sin(self, degrees):
        radians = math.radians(degrees)
        return math.sin(radians)
        
    def cos(self, degrees):
        radians = math.radians(degrees)
        return math.cos(radians)
        
    def tan(self, degrees):
        radians = math.radians(degrees)
        if abs(math.cos(radians)) < 1e-10:
            return "Ошибка:тангенс не определен"
        return math.tan(radians)
        
    def ln(self, a):
        if a <= 0:
            return "Ошибка: число должно быть больше 0"
        return math.ln(a)
        
    def log10(self, a):
        if a <= 0:
            return "Ошибка: число должно быть больше 0"
        return math.log10(a)
        
    def log(self, a, base):
        if a <= 0:
            return "Ошибка: число должно быть больше 0"
        if base <= 0 or base == 1:
            return "Ошибка: основание должно быть > 0 и не равно 1"
        return math.log(a, base)
    
        
calc = Calculator()

print("Выберите операцию:")
print("+ - * /")
print("power - степень")
print("sqrt - квадратный корень")
print("persent - процент")
print("sin - синус")
print("cos - косинус")
print("tan - тангенс")
print("ln - натуральный логарифм")
print("log10 - логарифм по основанию 10")
print("log - логарифм по заданному основанию")

operation = input ("Введите операцию: ")

if operation == "+":
    a = float(input("Введите первое число:"))
    b = float(input("Введите второе число:"))
    result = calc.add(a, b)
    
elif operation == "-":
    a = float(input("Введите первое число:"))
    b = float(input("Введите второе число:"))
    result = calc.subtract(a, b)
    
elif operation == "*":
    a = float(input("Введите первое число:"))
    b = float(input("Введите второе число:"))
    result = calc.multiply(a, b)
    
elif operation == "/":
    a = float(input("Введите первое число:"))
    b = float(input("Введите второе число:"))
    result = calc.divide(a, b)
    
elif operation == "power":
    a = float(input("Введите число:"))
    b = float(input("Введите степень:"))
    result = calc.power(a, b)
    
elif operation == "sqrt":
    a = float(input("Введите число:"))
    result = calc.square_root(a)
    
elif operation == "percent":
    a = float(input("Введите число:"))
    b = float(input("Введите процент:"))
    result = calc.percent(a, b)
    
elif operation == "sin":
    a = float(input("Введите угол в градусах:"))
    result = calc.sin(a)
    
elif operation == "cos":
    a = float(input("Введите угол в градусах:"))
    result = calc.cos(a)
    
elif operation == "tan":
    a = float(input("Введите угол в градусах:"))
    result = calc.tan(a)
    
elif operation == "ln":
    a = float(input("Введите число:"))
    result = calc.ln(a)
    
elif operation == "log10":
    a = float(input("Введите число:"))
    result = calc.log10(a)
    
elif operation == "log":
    a = float(input("Введите число:"))
    base = float(input("Введите основание:"))
    result = calc.log(a, base)
    
else: 
    result = "Неизвестная операция"
    
print("Результат:", result)
