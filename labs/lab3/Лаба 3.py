def Zad1Lab3():
    NameUs = input("Vod Name: ")
    Old = input("Vod Old: ")
    Mystr = F"Меня зовут {NameUs} и мне {Old} лет"
    for i in range(10):
        print(Mystr)
# Zad1Lab3()

def Zad2Lab3():
    Vod0 = int(input("Vod: "))
    for i in range(1,10+1):
        print(F"{Vod0} * {i} = {Vod0*i}")
# Zad2Lab3()

def Zad3Lab3():
    for i in range(0,100+1,3):
        print(i)
# Zad3Lab3()


def Zad4Lab3():
    inp0 = int(input("Vod: "))
    ch0 = 1
    for i in range(1,inp0+1):
        ch0*=i
    print(ch0)
# Zad4Lab3()

def Zad5Lab3():
    ch0 = 20
    while ch0>=0:
        print(ch0)
        ch0-=1
# Zad5Lab3()


# def Zad6Lab3():
#     inp0 = int(input("Vod: "))
#     zn1 = 0
#     zn2 = 1
#     lst0 = [zn2]
#     while zn1<=inp0:
#         print(zn1)
#         zn1=zn2
#         zn2=zn1+zn2


# Zad6Lab3()



def Zad7Lab3():
    inp0 = input("Vod: ")
    str0 = ""
    for i in range(len(inp0)):
        str0 = str0 + str(inp0[i])
        str0 = str0 + str(i+1)
    print(str0)
# Zad7Lab3()



def Zad8Lab3():
    while True:
        inp0 = sum([int(i) for i in input("Vod with space: ").split()])
        print(inp0)

Zad8Lab3()