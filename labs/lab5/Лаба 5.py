def Lab5Zad1():
    lst=[12,34,56,3,902,5,3,8,111,3]
    print(lst)
    NewLst = []
    for i in lst:
        if i != 3:
            NewLst.append(i)
        if i == 3:
            NewLst.append(30)
    print(NewLst)
# Lab5Zad1()

def Lab5Zad2():
    lst0 = [12,2,4,5,7]
    print(lst0)
    Nlst = [i**2 for i in lst0]
    print(Nlst)
# Lab5Zad2()


import random
def Lab5Zad3():
    lst0 = [random.randint(1,100) for i in range(5)]
    print(lst0)
    print((max(lst0))/len(lst0))

# Lab5Zad3()

def Lab5Zad4():
    typl = (12,7,3,1334,89,1)
    # typl = (12, 7, 3, 1334, "AAAAA", 1)
    TypeTupl = [type(i) for i in typl]
    # print(TypeTupl)
    FlagLog = [True if i==int else False for i in TypeTupl]
    # print(FlagLog)
    if all(FlagLog):
        typl=tuple(sorted(typl))
    print(typl)

# Lab5Zad4()



def Lab5Zad5():
    dic0 = {"Пипидастр":1123,"Свиная голова":8923,"Фурункул":4,"Веревка":134}
    price0 = list(dic0.values())
    MinPrice = min(price0)
    MaxPrice = max(price0)
    # print(price0)
    for i,j in dic0.items():
        # print(i,j)
        if j==MinPrice:
            print(f"Самы дешевый товар: {i}")
        if j==MaxPrice:
            print(f"Самый дорогой товар: {i}")

# Lab5Zad5()

def Lab5Zad6():
    lst0 = ["12","Hu","12890", "*_*"]
    dict0 = {}
    for i in lst0:
        dict0[i]=i
    print(dict0)
# Lab5Zad6()

def Lab5Zad7():
    dict0 = {"Blood":"кровь",
             "aplle":"яблочко",
             "Science":"наука"}
    inp0 = input("Vod: ").lower()
    for i,j in dict0.items():
        if j==inp0:
            print(i)

# Lab5Zad7()

def Lab5Zad8():
    personLST = ["Камень",
                 "Ножницы",
                 "Бумага",
                 "Ящерица",
                 "Спок"]
    perRand = personLST[random.randint(0,4)]
    inp0 = input("Vod: ")
    print(f"{inp0} vs {perRand}")
    if inp0 == "Ножницы" and perRand == "Бумага":
        print("Победил ты!")
    elif inp0 == "Бумага" and perRand == "Камень":
        print("Победил ты!")
    elif inp0 == "Камень" and perRand == "Ящерица":
        print("Победил ты!")
    elif inp0 == "Ящерица" and perRand == "Спок":
        print("Победил ты!")
    elif inp0 == "Спок" and perRand == "Ножницы":
        print("Победил ты!")
    elif inp0 == "Ножницы" and perRand == "Ящерица":
        print("Победил ты!")
    elif inp0 == "Ящерица" and perRand == "Бумага":
        print("Победил ты!")
    elif inp0 == "Бумага" and perRand == "Спок":
        print("Победил ты!")
    elif inp0 == "Спок" and perRand == "Камень":
        print("Победил ты!")
    elif inp0 == "Камень" and perRand == "Ножницы":
        print("Победил ты!")
    else:
        print("Ты проиграл!")

# Lab5Zad8()


# def Lab5Zad9():
#     lst0 = ["яблоко", "груша",
#             "банан", "киви",
#             "апельсин", "ананас"]
#     lst0Words = [i[0] for i in lst0] #['я', 'г', 'б', 'к', 'а', 'а']
#     dict0 = {}
#     # print(lst0Words)
#     while len(dict0) < len(set(lst0Words)):
#         for i in lst0:
#             for j in lst0Words:
#                 if i[0] == j:
#                     dict0[i]=j
#     print(dict0)
# Lab5Zad9()


# def Lab5Zad9():
#     lst0 = ["яблоко", "груша",
#             "банан", "киви",
#             "апельсин", "ананас"]
#     lst0Words = [i[0] for i in lst0] #['я', 'г', 'б', 'к', 'а', 'а']
#     dict0 = {}
#     unicumLst0words = set(lst0Words)
#     flag1UniqueValues = True if len(unicumLst0words) == len(lst0Words) else False
#     # print(lst0Words)
#     # while len(dict0) < len(set(lst0Words)):
#     #     for i in lst0:
#     #         for j in lst0Words:
#     #             if i[0] == j:
#     #                 dict0[j]=i
#     # print(dict0)
#     print(flag1UniqueValues)
#
# Lab5Zad9()



def Lab5Zad9():
    lst0 = ["яблоко", "груша",
            "банан", "киви",
            "апельсин", "ананас"]
    lst0Words = [i[0] for i in lst0] #['я', 'г', 'б', 'к', 'а', 'а']
    dict0 = {}
    # print(lst0Words)
    while len(dict0) < len(set(lst0Words)):
        for i in lst0:
            for j in lst0Words:
                if i[0] == j:
                    dict0[i]=j
    print(dict0)
# Lab5Zad9()

def Lab5Zad10():
    # lst00 = [("Анна", [5, 4, 5]),
    #          ("Иван", [3, 4, 4]),
    #          ("Мария", [5, 5, 5])]
    lst00 = [("Анна", [5, 4, 5]),
             ("Иван", [3, 4, 4]),
             ("Рэйнер", [100, 100, 99]),
             ("Мария", [5, 5, 5])]
    def midVal(n):
        return (sum(n))/(len(n))
    maxValStud = 0
    dictNew = {}
    NameStud = ''
    for i in lst00:
        # print(i[0],"       ",i[1])
        # print(midVal(i[1]))
        dictNew[i[0]]=midVal(i[1])
        if midVal(i[1]) > maxValStud:
            maxValStud = midVal(i[1])
            NameStud = i[0]
    print(dictNew)
    print(F"{NameStud} имеет наивысший бал: {maxValStud}")
Lab5Zad10()

