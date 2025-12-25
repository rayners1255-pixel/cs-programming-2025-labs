def Lab6Zad1():
    def Zad(time0,ed0,ed2):
        time0 = int(time0)
        ed0,ed2 = str(ed0).lower(),str(ed2).lower()
        if ed0 == "h" and ed2 == "m":
            return F"{time0}H == {time0*60}M"
        elif ed2 == "h" and ed0 == "m":
            return F"{time0}M == {time0/60}H"
        else:
            return time0,ed0
    print(Zad(12,"H","m"))

# Lab6Zad1()




# def Lab6Zad2():
#     def Zad(SumNak,years): #Сумма вклада и колличество лет
#         ch = SumNak
#         flagMinSum = True if SumNak >= 30_000 else False
#         # print(flagMinSum)
#         procient = 0
#         if flagMinSum == True:
#             if years <= 3:
#                 procient += 3
#             elif 4 <= years <=6:
#                 procient += 5
#             elif years>6:
#                 procient += 2
#
#             if SumNak>=170_000:
#                 procient += 5
#             elif SumNak < 40_000:
#                 pass
#             else:
#                 procient += (((SumNak)//10_000)*0.3)
#         print(procient)
#         for j in range(years):
#
#             ch+=ch*procient
#         print(ch-SumNak)
#
#
#
#
#     Zad(30000,3)
# Lab6Zad2()


def Lab6Zad2():
    def Zad(SumNak, years):
        # Проверка минимальной суммы
        if SumNak < 30000:
            print("Ошибка: минимальный вклад 30 000 рублей")
            return

        # 1. Процент за срок
        if years <= 3:
            procient = 3
        elif years >= 4 and years <= 6:
            procient = 5
        else:  # больше 6 лет
            procient = 2

        # 2. Процент за сумму
        # Сколько полных 10 тысяч в сумме
        kol_10k = SumNak // 10000
        dobavka = kol_10k * 0.3

        # Проверяем максимум 5%
        if dobavka > 5:
            dobavka = 5

        # Итоговая ставка
        procient += dobavka

        # 3. Считаем прибыль со сложным процентом
        # Формула: сумма * (1 + процент/100)^годы
        itog_summa = SumNak

        # Начисляем проценты каждый год
        for god in range(years):
            itog_summa = itog_summa * (1 + procient / 100)

        # Прибыль = итоговая сумма - начальная сумма
        pribyl = itog_summa - SumNak

        # Округляем до 2 знаков (копеек)
        pribyl = round(pribyl, 2)

        print(f"Вклад: {SumNak} руб, срок: {years} лет")
        print(f"Процентная ставка: {procient}% годовых")
        print(f"Прибыль: {pribyl} руб")
        print("-" * 40)

        return pribyl

    # Тестируем примеры из задачи
    print("РАСЧЕТ ПРИБЫЛИ ПО ВКЛАДУ")
    print("=" * 40)

    # Пример 1
    Zad(30000, 3)

    # Пример 2
    Zad(100000, 5)

    # Пример 3
    Zad(200000, 8)

    # Можно проверить другие значения
    print("\nДополнительные примеры:")
    Zad(50000, 4)  # 50к на 4 года
    Zad(150000, 2)  # 150к на 2 года
# Lab6Zad2()


def Lab6Zad3():
    def SimpleNumber(A,B):
        Kop = []
        if A<B:
            for i in range(A,B+1):
                if i>1:
                    flagSimple = True
                    for j in range(2,B):
                        if i%j==0 and j!=i:
                            flagSimple = False
                            break
                    if flagSimple:
                        Kop.append(i)
        if len(Kop)!=0:
            print(*Kop)
        else:
            print("Error")

    SimpleNumber(2,13)
    SimpleNumber(1,10)
    SimpleNumber(15, 120)
    SimpleNumber(0,1)


# Lab6Zad3()


# def Lab6Zad4():
#     def SumMatrix(n,lstM1,lstM2):
#         print(n,lstM1,lstM2)
#         if len(lstM1)!=len(lstM2):
#             print("Ошибка матрицы разного рамера")
#         else:
#
#
#
#     SumMatrix(2,[2,5,5,3],[5,2,4,1])
# Lab6Zad4()


def Lab6Zad4():
    def SumMatrix():
        # Читаем размер матрицы
        n_str = input()

        # Пробуем преобразовать в число
        try:
            n = int(n_str)
        except:
            print("Error!")
            return

        # Проверяем размер
        if n <= 2:
            print("Error!")
            return

        # Читаем первую матрицу
        matrix1 = []
        i = 0
        while i < n:
            try:
                row_str = input()
            except:
                print("Error!")
                return

            parts = row_str.split()

            # Проверяем количество чисел
            if len(parts) != n:
                print("Error!")
                return

            # Пробуем сделать числа из строк
            ch2 = []
            j = 0
            while j < n:
                try:
                    num = int(parts[j])
                except:
                    print("Error!")
                    return
                ch2.append(num)
                j += 1

            matrix1.append(ch2)
            i += 1

        # Читаем вторую матрицу
        matrix2 = []
        i = 0
        while i < n:
            try:
                row_str = input()
            except:
                print("Error!")
                return

            parts = row_str.split()

            # Проверяем количество чисел
            if len(parts) != n:
                print("Error!")
                return

            # Пробуем сделать числа из строк
            ch2 = []
            j = 0
            while j < n:
                try:
                    num = int(parts[j])
                except:
                    print("Error!")
                    return
                ch2.append(num)
                j += 1

            matrix2.append(ch2)
            i += 1

        # Складываем матрицы
        result = []
        i = 0
        while i < n:
            result_row = []
            j = 0
            while j < n:
                # Складываем элементы
                sum_element = matrix1[i][j] + matrix2[i][j]
                result_row.append(sum_element)
                j += 1
            result.append(result_row)
            i += 1

        # Выводим результат
        i = 0
        while i < n:
            # Делаем строку из чисел
            output_parts = []
            j = 0
            while j < n:
                output_parts.append(str(result[i][j]))
                j += 1

            # Печатаем строку
            print(" ".join(output_parts))
            i += 1

    # Вызываем функцию
    SumMatrix()


# 3
# 2 4 5
# 5 6 7
# 3 0 1
# 1 1 1
# 1 1 1
# 1 1 1
# Lab6Zad4()

def Lab6Zad5():
    def palindrome():
        # Получаем строку
        text = input()

        # Приводим к нижнему регистру
        text = text.lower()

        # Удаляем все не-буквы (пробелы, знаки препинания)
        letters = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz0123456789"
        clean_text = ""

        for char in text:
            if char in letters:
                clean_text += char

        # Проверяем палиндром
        n = len(clean_text)
        is_pal = True

        for i in range(n // 2):
            if clean_text[i] != clean_text[n - i - 1]:
                is_pal = False
                break

        if is_pal:
            print("Да")
        else:
            print("Нет")

    palindrome()

# Borrow or rob	Да
# Алфавитный порядок	Нет
# Lab6Zad5()
