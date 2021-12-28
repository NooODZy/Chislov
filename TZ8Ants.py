import copy
import random
import time
import matplotlib.pyplot as plt

def interfacer():
    """
    Функция на вход получает значение и заполняет ключевые переменные
    """
    print("введите Вершины")
    n = int(input())
    Q = 4  # константа 
    a = 1  # константа 
    b = 4  # константа 
    Mnojest = {1}
    Inters = []
    Inters.append(1)
    Countries = {}  # Множество городов
    MAtrizaPheromonov = {}  # матрица феромончиков
    Xsheeesh = []  # x координаты городов
    Ysheeesh = []  # y координаты городов
    Xsheeesh.append(1)  # Начинаем с 0, а не с 1
    Ysheeesh.append(1)  # Начинаем с 0, а не с 1
    for i in range(2, n + 1):
        Mnojest.add(i)




    for i in range(1, n + 1):
        Xsheeesh.append(random.randint(200, 1500))
        Ysheeesh.append(random.randint(200, 900))


    def GeneratorRex():    
        """ 
        Функция рандомно генерирует пути для муравьев, и заполняет матрицу
        """
        Wow = []
        Wow1 = []
        for i in range(1, n + 1):
            for x in range(1, n + 1):
                Countries[int(str(i) + str(x))] = int(random.randint(100, 1710))
                if x == i:
                    Countries[int(str(i) + str(x))] = "a"
                q = 0
                if q == 1:
                    Countries[int(str(i) + str(x))] = "a"
                Wow.append(Countries[int(str(i) + str(x))])
            Wow1.append(Wow)
            Wow = []
        for i in Wow1:
            print(i)
            
    def MatrizaPher():
        """
        Функция заполняет матрицу феромонов
        """
        Wow = []
        Wow1 = []
        for i in range(1, n + 1):
            for x in range(1, n + 1):
                MAtrizaPheromonov[int(str(i) + str(x))] = 3
                if x == i:
                    MAtrizaPheromonov[int(str(i) + str(x))] = "b"
                q = random.randint(1, 5)
                if Countries[int(str(i) + str(x))] == "a":
                    MAtrizaPheromonov[int(str(i) + str(x))] = "b"
                Wow.append(MAtrizaPheromonov[int(str(i) + str(x))])
            Wow1.append(Wow)
            Wow = []
        for i in Wow1:
            print(i)

    def GeneratorRex2():
        """
        Функция выбирает конкретный путь для муравья
        """
        Wow = []
        Wow1 = []

        for i in range(1, n + 1):
            for x in range(1, n + 1):
                print(i, x, "введите:")
                Countries[int(str(i) + str(x))] = input()
                if x == i:
                    Countries[int(str(i) + str(x))] = "a"
                Wow.append(Countries[int(str(i) + str(x))])
            Wow1.append(Wow)
            Wow = []
        for i in Wow1:
            print(i)


    print("Авто или ручками (1 или 2)?")
    Turn = int(input())
    if Turn == 1:
        GeneratorRex()
    if Turn == 2:
        GeneratorRex2()
    print()
    print("МАТРИЦА ФЕРОМОНчиков")
    print()
    MatrizaPher()
#interfacer()