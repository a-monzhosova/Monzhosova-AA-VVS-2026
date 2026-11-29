import pandas as pd
import numpy as np

#Загрузка и первичный анализ данных

# 6. Загружаем файл
df = pd.read_csv(r"C:\Users\алина\Downloads\test.csv")

# 7. Первые n строк
n = int(input("Сколько строк показать? "))
print("\n--- 7. Первые", n, "строк ---")
print(df.head(n))

# 8. Последние 5 строк
print("\n--- 8. Последние 5 строк ---")
print(df.tail(5))

# 9. Сколько строк и столбцов
print("\n--- 9. Размер таблицы ---")
print("Строк:", df.shape[0])
print("Столбцов:", df.shape[1])

# 10. Названия столбцов
print("\n--- 10. Столбцы ---")
print(list(df.columns))

# 11. Типы данных
print("\n--- 11. Типы данных ---")
print(df.dtypes)

# 12. Числовые и категориальные признаки (по смыслу)
print("\n--- 12. Признаки ---")
print("Числовые: Age, SibSp, Parch, Fare")
print("Категориальные: Survived, Pclass, Sex, Embarked, Cabin")

# 13. Статистика числовых признаков
print("\n--- 13. Статистика ---")
print(df[["Age", "SibSp", "Parch", "Fare"]].describe())
print("Медиана:")
print(df[["Age", "SibSp", "Parch", "Fare"]].median())

# 14. Пассажиры по классам
print("\n--- 14. Пассажиры по классам ---")
print(df["Pclass"].value_counts())

# 15. Уникальные значения в Embarked
print("\n--- 15. Уникальные значения Embarked ---")
print(df["Embarked"].nunique(), "->", df["Embarked"].unique())

#Обработка пропущенных значений

# 16. Количество пропусков
print("\n--- 16. Пропуски по столбцам ---")
print(df.isna().sum())

# 17. Процент пропусков
print("\n--- 17. Процент пропусков ---")
print(df.isna().sum() / len(df) * 100)

# 18. Столбец с наибольшим числом пропусков
print("\n--- 18. Больше всего пропусков ---")
print(df.isna().sum().idxmax())

# Запоминаем размер до обработки
rows_before = df.shape[0]
cols_before = df.shape[1]

# 19. Статистика Age ДО заполнения
age_mean_before = df["Age"].mean()
age_median_before = df["Age"].median()
age_min_before = df["Age"].min()
age_max_before = df["Age"].max()
age_std_before = df["Age"].std()
age_count_before = df["Age"].count()   # count считает только известные значения

print("\n--- 19. Age до заполнения ---")
print("Среднее:", age_mean_before)
print("Медиана:", age_median_before)
print("Минимум:", age_min_before)
print("Максимум:", age_max_before)
print("Станд. отклонение:", age_std_before)
print("Известных значений:", age_count_before)

# 20. Заполняем пропуски в Age медианой
df["Age"] = df["Age"].fillna(age_median_before)
print("\n--- 20. Пропусков в Age после заполнения:", df["Age"].isna().sum())

# 21. Статистика Age ПОСЛЕ заполнения
age_mean_after = df["Age"].mean()
age_median_after = df["Age"].median()
age_min_after = df["Age"].min()
age_max_after = df["Age"].max()
age_std_after = df["Age"].std()
age_count_after = df["Age"].count()

# 22. Таблица «до / после»
table = pd.DataFrame({
    "Показатель": ["Среднее", "Медиана", "Минимум", "Максимум",
                   "Станд. отклонение", "Известных значений"],
    "До обработки": [age_mean_before, age_median_before, age_min_before,
                     age_max_before, age_std_before, age_count_before],
    "После обработки": [age_mean_after, age_median_after, age_min_after,
                        age_max_after, age_std_after, age_count_after],
})
print("\n--- 22. Сравнение до / после ---")
print(table.round(2))
table.to_csv("age_before_after.csv", index=False)

# 23. Удаляем строки, где не указан Embarked
df = df.dropna(subset=["Embarked"])
print("\n--- 23. Строк после удаления пропусков Embarked:", len(df))

# 24. Доля пропусков в Cabin; если больше 50% - удаляем столбец
cabin_share = df["Cabin"].isna().mean() * 100
print("\n--- 24. Пропусков в Cabin: ", round(cabin_share, 2), "%")
if cabin_share > 50:
    df = df.drop(columns="Cabin")
    print("Больше 50% - столбец Cabin удалён")

# 25. Какие пропуски остались
print("\n--- 25. Оставшиеся пропуски ---")
print(df.isna().sum())

# 26. Размер до и после
print("\n--- 26. Размер таблицы ---")
print("До:    ", rows_before, "строк,", cols_before, "столбцов")
print("После: ", df.shape[0], "строк,", df.shape[1], "столбцов")

#NumPy

# Превращаем столбцы в массивы NumPy
survived = df["Survived"].to_numpy()
age = df["Age"].to_numpy()
fare = df["Fare"].to_numpy()
sex = df["Sex"].to_numpy()

# Маски: True там, где пассажир - мужчина (или женщина)
is_male = (sex == "male")
is_female = (sex == "female")

# 31. Общий процент выживших (среднее из 0 и 1 = доля единиц)
print("\n--- 31. Процент выживших ---")
print(np.mean(survived) * 100)

# 32. Процент выживших среди мужчин и женщин
print("\n--- 32. Выжившие по полу ---")
print("Мужчины:", np.mean(survived[is_male]) * 100)
print("Женщины:", np.mean(survived[is_female]) * 100)

# 33. Средний возраст мужчин и женщин
print("\n--- 33. Средний возраст ---")
print("Мужчины:", np.mean(age[is_male]))
print("Женщины:", np.mean(age[is_female]))

# 34. Средний возраст выживших и погибших по полу
# Здесь удобнее groupby. Если какой-то группы нет в данных
# (например, выживших мужчин), она просто не появится в результате.
print("\n--- 34. Средний возраст по полу и выживаемости ---")
print(df.groupby(["Sex", "Survived"])["Age"].mean())

# 35. Стоимость билета (в Fare есть один пропуск, поэтому nan-функции)
print("\n--- 35. Стоимость билета ---")
print("Минимум:", np.nanmin(fare))
print("Максимум:", np.nanmax(fare))
print("Среднее:", np.nanmean(fare))

# 36. Стандартное отклонение возраста
print("\n--- 36. Станд. отклонение возраста ---")
print(np.std(age, ddof=1))

# Сравнительная таблица
compare = pd.DataFrame({
    "Пол": ["Мужчины", "Женщины"],
    "Выжившие, %": [np.mean(survived[is_male]) * 100,
                    np.mean(survived[is_female]) * 100],
    "Средний возраст": [np.mean(age[is_male]), np.mean(age[is_female])],
    "Средняя цена билета": [np.nanmean(fare[is_male]), np.nanmean(fare[is_female])],
})
print("\n--- Сравнительная таблица ---")
print(compare.round(2))

#Фильтрация данных

# Задание 1: мужчины старше 30 из первого класса
task1 = df[(df["Sex"] == "male") & (df["Age"] > 30) & (df["Pclass"] == 1)]
print("\n--- Задание 1 ---")
print("Количество:", len(task1))
print(task1.head(10))

# Задание 2: моложе 18 ИЛИ (женщина И выжила)
task2 = df[(df["Age"] < 18) | ((df["Sex"] == "female") & (df["Survived"] == 1))]
print("\n--- Задание 2 ---")
print("Количество:", len(task2))

# Задание 3: 3 класс, билет дороже среднего в этом классе
class3 = df[df["Pclass"] == 3]
mean_fare_class3 = class3["Fare"].mean()
task3 = class3[class3["Fare"] > mean_fare_class3]
print("\n--- Задание 3 ---")
print("Средний билет в 3 классе:", round(mean_fare_class3, 2))
print("Количество:", len(task3))
print(task3.head(10))

# Задание 4: возраст от 20 до 40 включительно, порт S
task4 = df[(df["Age"] >= 20) & (df["Age"] <= 40) & (df["Embarked"] == "S")]
print("\n--- Задание 4 ---")
print("Количество:", len(task4))
print(task4.head(10))

#Группировка и агрегирование

# Чтобы посчитать % выживших, добавим столбец Survived * 100:
# тогда среднее по нему сразу даст проценты.
df["SurvivedPct"] = df["Survived"] * 100

# 37. Группировка по классу и полу
stats = df.groupby(["Pclass", "Sex"]).agg(
    Passengers=("Survived", "count"),
    MeanAge=("Age", "mean"),
    SurvivedPct=("SurvivedPct", "mean"),
    MeanFare=("Fare", "mean"),
)
stats = stats.round(2).reset_index()
print("\n--- 37. Группировка по классу и полу ---")
print(stats)

# 38. Группировка по порту
ports = df.groupby("Embarked").agg(
    Passengers=("Survived", "count"),
    SurvivedPct=("SurvivedPct", "mean"),
)
print("\n--- 38. Группировка по порту ---")
print(ports.round(2))

# 39. Класс с наибольшей долей выживших
by_class = df.groupby("Pclass")["SurvivedPct"].mean()
print("\n--- 39. Доля выживших по классам ---")
print(by_class.round(2))
print("Лучший класс:", by_class.idxmax())

#Сохранение

df = df.drop(columns="SurvivedPct")      

# 40. Сохраняем обработанные данные
df.to_csv("titanic_processed.csv", index=False)

# 41. Сохраняем статистику
stats.to_csv("titanic_statistics.csv", index=False)

# 42. Загружаем обратно и проверяем
check = pd.read_csv("titanic_processed.csv")
print("\n--- 42. Проверка ---")
print("Размер совпадает:", check.shape == df.shape)
print(check.head())