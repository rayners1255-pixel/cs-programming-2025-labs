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




def Lab6Zad2():
    def Zad(SumNak,years):
        flagMinSum = True if SumNak >= 30_000 else False
        # print(flagMinSum)
        procient = 0
        if flagMinSum == True:
            if years <= 3:
                procient=3
            elif 4 <= years <=6:
                procient=5
            elif years>6:
                procient = 2




    Zad(51456,2)
Lab6Zad2()





