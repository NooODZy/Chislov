import numpy as np
import copy
import random
from math import exp
import matplotlib.pyplot as plt

def interface():
    """
    Функция получает на вход значения для заполнения словаря и значение для кол-ва вершин
    """
    Countries = {}
    print("введите Вершины")
    n = int(input())

    def gs(way):
        """
        Функция считает сумму пути 
        """
        sum=0
        for i in range(len(way)-1):
            sum+=Countries[int(str(way[i])+str(way[i+1]))]
        return sum
    def Generatorrex():  
        """
        Функция рандомно генерирует пути
        """
        Well = []
        Well1 = []
        for i in range(1, n + 1):
            for x in range(1, n + 1):
                Countries[int(str(i) + str(x))] = int(random.randint(1, 20))
                if x == i:
                    Countries[int(str(i) + str(x))] = "a"
                q = 0
                if q == 1:
                    Countries[int(str(i) + str(x))] = "a"

                Well.append(Countries[int(str(i) + str(x))])
            Well1.append(Well)
            Well = []
        Well = []
        Well1 = []
        for i in range(1, n + 1):
            for x in range(1, n + 1):
                Countries[int(str(i) + str(x))] = Countries[int(str(x) + str(i))]
                Well.append(Countries[int(str(i) + str(x))])
            Well1.append(Well)
            Well = []



    def waydown(way):
        """
        Функция меняет два случайных значения в пути 
        """
        counter=[]
        S=way[1:-1]
        S1=random.sample(S,2)
        for i in range(len(S)):
            if S[i]==S1[0]:
                counter.append(i)
            if S[i]==S1[1]:
                counter.append(i)

        timing = S[counter[0]]
        way[counter[0]+1]=S[counter[1]]
        way[counter[1]+1]=timing
        return way
    def rnd():
        """
        Функция создает случайный путь 
        """
        way=[]
        for i in range(1,n+1):
            way.append(i)
        random.shuffle(way)
        return way
    T=[1000,100,500,50,150]
    for i in range(5):
        Generatorrex()
    x=rnd()
    a=0.91
    Tempreture=T[i]
    TempFor=T[i]
    Ll1=gs(x)
    Counterstrike=0
    Counterstrike2=[]

    while Tempreture>0.01:
        Counterstrike+=1
        way3=waydown(x)
        Ll2=gs(way3)
        Difference=Ll2-Ll1
        Notcons=100*exp(-(Difference)/Tempreture)

        if Difference<0:
            Ll1=Ll2
            Tempreture=Tempreture*0.85
            #Counterstrike2.append(Ll1)
        elif Notcons > random.randint(1,100):
            Ll1 = Ll2
            Tempreture = Tempreture * 0.85
            #Counterstrike2.append(Ll1)
        else:
            Tempreture=Tempreture*0.85
        Counterstrike2.append(Ll1)

    plt.plot(range(1,Counterstrike+1),Counterstrike2)
    plt.title("a={}, T = {}".format(a,TempFor))
    plt.show()
    a=[0.8,0.9,0.85,0.8,0.5]
    print()
    print("Поигрались с температуркой, теперь покажем оптимальный a")
    print()
    for i in range(3):
        Generatorrex()
    x=rnd()
    an=a[i]
    Tempreture=1000
    TempFor=1000
    Ll1=gs(x)
    Counterstrike=0
    Counterstrike2=[]

    while Tempreture>0.01:
        Counterstrike+=1
        way3=waydown(x)
        Ll2=gs(way3)
        Difference=Ll2-Ll1
        Notcons=100*exp(-(Difference)/Tempreture)

        if Difference<0:
            Ll1=Ll2
            Tempreture=Tempreture*an
            #Counterstrike2.append(Ll1)
        elif Notcons > random.randint(1,100):
            Ll1 = Ll2
            Tempreture = Tempreture * an
            #Counterstrike2.append(Ll1)
        else:
            Tempreture=Tempreture*an
        Counterstrike2.append(Ll1)

    plt.plot(range(1,Counterstrike+1),Counterstrike2)
    plt.title("a={}, T = {}".format(a[i],TempFor))
    plt.show()
#interface()
