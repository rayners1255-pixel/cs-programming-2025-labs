def Lab4Zad1():
    inp0 = int(input("Введите температуру: "))
    if inp0 >= 20:
        print("Кондишка выключается")
    else:
        print("Кондишка включается")
# Lab4Zad1()


def Lab4Zad2():
    inp0 = int(input("Номер месяца: "))
    if inp0 == 12 or inp0 == 1 or inp0 == 2:
        print("ЗИМА!!!")
    elif inp0 == 3 or inp0 == 4 or inp0 == 5:
        print("Весна!!")
    elif inp0 == 6 or inp0 == 7 or inp0 == 8:
        print("Лето!!")
    elif inp0 == 9 or inp0 == 10 or inp0 == 11:
        print("Осень!!")
# Lab4Zad2()

def Lab4Zad3():
    inp0 = int(input("Введите возраст собачки: "))
    ch = 0
    if 23 > inp0 > 0:
        for i in range(1,inp0+1):
            if i == 1 or i == 2:
                ch+=10.5
            elif i>2:
                ch+=4
    if ch!=0:
        print(ch)
    else:
        print("Ой-ой-ой! Опять ошибка! Значения нужны больше 0 и меньше 23")
# Lab4Zad3()



def Lab4Zad4():
    inp0 = int(input("Vod: "))
    lst0 = sum([int(i) for i in str(inp0)])

    if lst0%3==0 and (inp0%10)%2==0:
        print(f"Да число {inp0} реально делится на 6!")
    else:
        print("НЕ-не-не-не")
# Lab4Zad4()

def Lab4Zad5():
    inp0 = input("Введите пароль: ")
    latBigStr = ("A B C D E F G H I J K "
                 "L M N O P Q R S T U V "
                 "W X Y Z")
    latBigW_lst = latBigStr.split(" ")
    # print(latBigW_lst)
    latSmallW_lst = (latBigStr.lower()).split(" ")
    # print(latSmallW_lst)
    Digit_lst = [str(i) for i in range(1,10)]
    specialSimv_lst = [",",".","!","_","?","-"]
    # FlagLatBig = False
    # for w in latBigW_lst:
    #     if w in inp0:
    #         FlagLatBig = True
    FlagLen = True if len(inp0)>=8 else False
    # print(FlagLen)
    FlagLatBig = any(w in inp0 for w in latBigW_lst)
    # print(FlagLatBig)
    FlagLatSmall = any(w in inp0 for w in latSmallW_lst)
    # print(FlagLatSmall)
    FlagDigit = any(w in inp0 for w in Digit_lst)
    # print(FlagDigit)
    FlagSpecial = any(w in inp0 for w in specialSimv_lst)
    # print(FlagSpecial)
    if FlagLatBig and FlagLatSmall and FlagDigit and FlagSpecial and FlagLen:
        print("Пароль - шикарен!!!")
    else:
        if FlagLen == False:
            print("Пароль должен быть минимум из 8 символов, дружище!")
        if FlagLatBig == False:
            print("Пароль должен включать латинские заглавные буквы")
        if FlagLatSmall == False:
            print("Пароль должен включать латинские маленькие буквы")
        if FlagDigit == False:
            print("Пароль должен включать цифры")
        if FlagSpecial == False:
            print("Пароль должен включать специальные символы")


# Lab4Zad5()


def Lab4Zad6():
    inp0 = int(input("Vod: "))
    if ((inp0 % 4 == 0) and (not(inp0 % 100 == 0))) or (inp0 % 400 == 0):
        print(F"{inp0} - високосный год")
    else:
        print(F"{inp0} - не високосный")

# Lab4Zad6()


def Lab4Zad7():
    inp0 = [int(i) for i in (input("Vod: ").split(" "))]
    inpSrt = sorted(inp0)
    print(F"Min - {inpSrt[0]}")

# Lab4Zad7()


def Lab4Zad8():
    inpSumPrice = float(input("Введите сумму покупки: "))
    if inpSumPrice < 1000:
        print("Скидка 0%")
        print(F"К оплате {inpSumPrice}")
    elif 1000 <= inpSumPrice < 5000:
        print("Скидка 5%")
        print(F"К оплате {inpSumPrice - (inpSumPrice*0.05)}")
    elif 5000 <= inpSumPrice < 10_000:
        print("Скидка 10%")
        print(F"К оплате {inpSumPrice - (inpSumPrice * 0.1)}")
    elif 10_000 <= inpSumPrice:
        print("Скидка 15%")
        print(F"К оплате {inpSumPrice - (inpSumPrice * 0.15)}")

# Lab4Zad8()


def Lab4Zad9():
    inp0 = int(input("Введите час(0-23): "))
    if 0 <= inp0 <= 23:
        if 0 <= inp0 <= 5:
            print("Ночь")
        elif 6 <= inp0 <= 11:
            print("Утро")
        elif 12 <= inp0 <= 17:
            print("День")
        elif 18 <= inp0 <= 23:
            print("Вечер")

    else:
        print("Ошибка! Будь внимательнее!")

# Lab4Zad9()


Lab4Zad10()





