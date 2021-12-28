
import numpy as np
from sympy import *
from numpy import transpose
from numpy import linalg as LA
from fractions import Fraction
import time
import matplotlib.pyplot as plt
from matplotlib import rcParams
import random
import copy
import csv


def number(str_input, str_error, str_error2, type_num): # str_input - строка выводимая пользователю при вводе 
                                                        # str_error - ошибка: число не является числом ('строка')
                                                        # str_error2 - число не соответсвует указаным требованиям
                                                        # type_num - все допустимые типы чисел
    """
    Принимает значение вводимые с клавиатуры
    Производит проверку
    Выводит название ошибок\число
    """
    print(str_input)
    num = input()
    if 'i' in num:
        num = itojnum(num)
    num.replace(" ", "")
    try:
        check = complex(num) # Проверка: является ли числом (комплексное можем взять от любого числа)
    except ValueError:
        print(str_error)
        return number(str_input, str_error, str_error2, type_num)
    
    if (complex in type_num) and check.imag != 0: # Проверки для комплексных чисел
        return jtoinum(num)
    elif (complex in type_num) and check.imag == 0:
        if (int in type_num):
            if check.real == round(check.real):
                return str(int(check.real))
        if (float in type_num):
            if check.real != round(check.real):
                return str(float(check.real))
        else:
            print(str_error2)
            return number(str_input, str_error, str_error2, type_num)

    elif (float in type_num): # Проверки для вещественных чисел
        if check.imag != 0:
            print(str_error2)
            return number(str_input, str_error, str_error2, type_num)
        if (int in type_num):
            if check.real == round(check.real):
                return str(int(check.real))
        else:
            return str(float(check.real))

    else: # Проверки для целых чисел
        if check.imag != 0:
            print(str_error2)
            return number(str_input, str_error, str_error2, type_num)
        elif check.real != round(check.real):
            print(str_error2)
            return number(str_input, str_error, str_error2, type_num)
        return str(int(check.real))
    
# Функция генерации рандомных чисел для CSV-файла и python.
    
def random_numbers(row,minim,maxi):
    complex_numb=[]
    for i in range(row**3):
        floatnump=random.randint(1,6)
        numb_of_list=random.randint(1,2)
        if numb_of_list==1:
            a=random.randint(minim,maxi)
        else:
            a=round(random.uniform(minim,maxi),floatnump)
        numb_of_list=random.randint(1,2)
        if numb_of_list==1:
            b=random.randint(minim,maxi)
        else:
            b=round(random.uniform(minim,maxi),floatnump)
        complex_numb.append(complex(a,b))
    
    result=[0]*row
    for i in range(row):
        floatnump=random.randint(1,6)
        numb_of_list=random.randint(1,3)
        if numb_of_list==1:
            result[i]=str(random.randint(minim,maxi))
        if numb_of_list==2:
            result[i]=str(round(random.uniform(minim,maxi),floatnump))
        if numb_of_list==3:
            result[i]=str(random.choice(complex_numb))
    
    return result

# Функция ввода матрицы через клавиатуру
    
def default_matrix(): # N - кол-во строк, M - кол-во столбцов
    """
    На вход принимает значение матрицы
    ЗАпоминает индекс
    Возвращает значения
    """
    try:
        rowcol = list(map(int,input('Введите количество строк и столбцов: ').split()))
        N = rowcol[0]
        M = rowcol[1]
        if len(rowcol) > 2:
            print('Введено слишком много значений. Попробуйте ещё раз.')
            return default_matrix()
    except ValueError:
        print('Введено не целое значение строки и/или столбца. Попробуйте ещё раз.')
        return default_matrix()
    except IndexError:
        print('Введено слишком мало чисел. Попробуйте ещё раз.')
        return default_matrix()
    if N == 0 or M == 0:
        print('Введено нулевое значение! Количество строк и столбцов должно быть минимум 1!!')
        return default_matrix()
    mtx = [[0] * M for i in range(N)]
    for n in range(N):
        for m in range(M):
            mtx[n][m] = number(f'Введите значение для элемента матрицы a[{n + 1}][{m + 1}]: ',
                              'Введено неверное выражение. Попробуйте ещё раз', 
                              'Введено число в неверном формате. Попробуйте ещё раз.',
                              [complex, float, int])
            
    for n in range(len(mtx)):
        #mtx[n].append('|')
        mtx[n].append(number(f'Введите значение для свободного члена {n + 1} строки: ',
                              'Введено неверное выражение. Попробуйте ещё раз',
                              'Введено число в неверном формате. Попробуйте ещё раз.',
                              [complex, float, int]))
    return mtx

# Функция ввода матрицы через радомную генерацию python.

def python_generator():
    """
    Значение кол-во строк и столбцов
    Создает матрицу
    Выводит матрциу
    """
    try:
        rowcol = list(map(int,input('Введите количество строк и столбцов (N M): ').split()))
        N = rowcol[0]
        M = rowcol[1]
        if len(rowcol) > 2:
            print('Введено слишком много значений. Попробуйте ещё раз.')
            return python_generator()
    except ValueError:
        print('Введено не целое значение строки и/или столбца. Попробуйте ещё раз.')
        return python_generator()
    except IndexError:
        print('Введено слишком мало чисел. Попробуйте ещё раз.')
        return python_generator()
    if N == 0 or M == 0:
        print('Введено нулевое значение! Количество строк и столбцов должно быть минимум 1!!')
        return python_generator()

    try:
        minmax = list(map(int,input('Введите минимальное и максимальное значене для элемента матрицы (также для мнимой части комплексного числа) (min max): ').split()))
        mini = minmax[0]
        maxi = minmax[1]
    except ValueError:
        print('Ошибка ввода. Попробуйте ещё раз.')
        return python_generator()
    except IndexError:
        print('Введено слишком мало чисел. Попробуйте ещё раз.')
        return python_generator()
    if mini > maxi:
        print(f'Минимальное число не может быть больше максимального ({mini}!>{maxi})!!')
        return python_generator()
    
    result=[]
    for i in range(M):
        result.append(random_numbers(N,mini,maxi))
    
    for row in range(len(result)):
        #result[row].append('|')
        result[row].append(random_numbers(1,mini,maxi))
        result[row][-1]=str(result[row][-1][0])
        
    result=jtoi(result)
    result=del_bracket(result)
        
    return result

# Функция ввода матрицы через CSV-файл.

def csv_generator():
    """
    На вход принимается кол-во столбцов и строк
    Считывается файл csv 
    Выводит значения
    """
    try:
        rowcol = list(map(int,input('Введите количество строк и столбцов (N M): ').split()))
        N = rowcol[0]
        M = rowcol[1]
        if len(rowcol) > 2:
            print('Введено слишком много значений. Попробуйте ещё раз.')
            return csv_generator()
    except ValueError:
        print('Введено не целое значение строки и/или столбца. Попробуйте ещё раз.')
        return csv_generator()
    except IndexError:
        print('Введено слишком мало чисел. Попробуйте ещё раз.')
        return csv_generator()
    if N == 0 or M == 0:
        print('Введено нулевое значение! Количество строк и столбцов должно быть минимум 1!!')
        return csv_generator()

    try:
        minmax = list(map(int,input('Введите минимальное и максимальное значене для элемента матрицы (также для мнимой части комплексного числа) (min max): ').split()))
        mini = minmax[0]
        maxi = minmax[1]
    except ValueError:
        print('Ошибка ввода. Попробуйте ещё раз.')
        return csv_generator()
    except IndexError:
        print('Введено слишком мало чисел. Попробуйте ещё раз.')
        return csv_generator()
    if mini > maxi:
        print(f'Минимальное число не может быть больше максимального ({mini}!>{maxi})!!')
        return csv_generator()
    
    result=[]
    for i in range(M):
        result.append(random_numbers(N,mini,maxi))
        
    for row in range(len(result)):
        #result[row].append('|')
        result[row].append(random_numbers(1,mini,maxi))
        result[row][-1]=str(result[row][-1][0])
        
    result=jtoi(result)
    result=del_bracket(result)
    
    with open('Answer_file.csv','w',newline='') as csvfile:
        writer=csv.writer(csvfile,delimiter=';')
        for row in result:
            writer.writerow(row)

    Matrix_in=[]
    with open('Answer_file.csv',newline='') as csvfile:
        reader = csv.reader(csvfile,delimiter=';')
        Matrix_in=[]
        for row in reader:
            Matrix_in.append(list(row))
    return Matrix_in

# Функция преобразования "i" в "j" для списка

def itoj(mtx):
    ans = []
    for i in range(len(mtx)):
        temp = []
        y = mtx[i]
        for j in y:
            temp.append(j.replace('i','j'))
        ans.append(temp)
    return ans

# Функция преобразования "j)" в "i" для списка.

def jtoi(mtx):
    ans = []
    for i in range(len(mtx)):
        temp = []
        y = mtx[i]
        for j in y:
            temp.append(j.replace('j)','i'))
        ans.append(temp)
    return ans

# Функция преобразования удаления левой скобки для списка.

def del_bracket(mtx):
    ans = []
    for i in range(len(mtx)):
        temp = []
        y = mtx[i]
        for j in y:
            temp.append(j.replace('(',''))
        ans.append(temp)
    return ans

# Функция преобразования "i" в "j" для строки.

def itojnum(st):
    ans = ''
    for i in st:
        ans += i.replace('i','j')
    return ans

# Функция преобразования "j" в "i" для строки.

def jtoinum(st):
    ans = ''
    for i in st:
        ans += i.replace('j','i')
    return ans

# Функция итерации матрицы всеми способами.
        
def iteration():
    print("Как вы хотите ввести матрицу:\n 1 - С кливаитуры\n 2 - Рандомная генерация в python\n 3 - CSV Файл")
    try:    
        choice = int(input('Вы ввели: '))
        choices_dict = {1: default_matrix, 2: python_generator , 3: csv_generator}
        mtx = choices_dict[choice]()
    except KeyError:
        print('Введено неверное значение ввода матрицы. Попробуйте ещё раз.')
        return iteration()
    except ValueError:
        print('Введено неверное значение ввода матрицы. Попробуйте ещё раз.')
        return iteration()
    return mtx

# Преобразование строковых значений в комплексные

def str_to_complex(mtx1):
    mtx = copy.deepcopy(mtx1)
    for row in mtx:
        for i in range(len(row)):
            row[i]=complex(itojnum(row[i]))
    return(mtx)

# Функция преобразует комплексные числа в другие типы чисел

def complex_to_num(st):
    if st.imag==0:
        if round(st.real)==st.real:
            return int(st.real)
        else:
            return float(st.real)
    else:
        return complex(st.real, st.imag)
    
# Создание из строковых чисел правильные дроби
    
def numbers_to_fractions(mtx):
    for row in range(len(mtx)):
        for col in range(len(mtx[row])):
            if 'i' in mtx[row][col]:
                return 'Функция не работает с комплексными числами'
            mtx[row][col]=Fraction(mtx[row][col])
    return mtx
    
# Нахождение определителя матрицы

def det_my_matrix(mtx):
    
    Lmtx=len(mtx)
    
    if Lmtx==1:
        return mtx[0][0]
    if Lmtx==2:
        return mtx[0][0]*mtx[1][1]-(mtx[0][1]*mtx[1][0])
    
    result=0
    for i in range(Lmtx):
        
        factor=1
        if i % 2:
            factor=-1
            
        mtx2=[]
        for row in range(Lmtx):
            mtx3=[]
            for col in range(Lmtx):
                if row!=0 and col!=i:
                    mtx3.append(mtx[row][col])
            if mtx3:
                mtx2.append(mtx3)
        
        result+=factor*mtx[0][i]*det_my_matrix(mtx2)
    return(result)

# Вычисление обратной матрицы

def inverse_matrix(mtx):
    Lmtx = len(mtx)
    mult = det_my_matrix(mtx)
    if mult == 0:
        return 'Матрица вырожденная'
    ans = [[0] * Lmtx for i in range(Lmtx)]
    for i in range(Lmtx):  
        for j in range(Lmtx):
            factor=1
            if (i+j) % 2:
                factor=-1
            mtx2 = []
            for i1 in range(Lmtx):
                if i1 != i:
                    mtx3 = []
                    for j1 in range(Lmtx):
                        if j1 != j:
                            mtx3.append(mtx[i1][j1])
                    mtx2.append(mtx3)
            ans[j][i] = factor * det_my_matrix(mtx2) / mult
    return ans

def diag(mtx1):
    mtx = copy.deepcopy(mtx1)
    for row in range(len(mtx)):
        for col in range(len(mtx[row])):
            if row==col:
                mtx[row]=list(np.array(mtx[row])/mtx[row][col])
    return mtx

# Вычисление матрицы коэффициентов

def coeff_mtx(mtx):
    mtx1 = []
    for i in range(len(mtx)):
        mtx1.append(mtx[i][:-1])
    return mtx1

# Вычисление вектора своюодных членов

def coeff_vect(mtx):
    mtx1 = []
    for i in range(len(mtx)):
        mtx1.append(mtx[i][-1])
    return mtx1

# Вычисление матодом простых итераций Якоби

def jacobi(arr,x,acc):
    arr1 = coeff_mtx(arr)
    vect = coeff_vect(arr)
    D = np.diag(arr1)
    R = arr1 - np.diagflat(D)
    x1 = [i for i in x]
    x = (vect - np.dot(R,x)) / D
    fin = abs(x1 - x)
    itr = 0
    while max(fin)>=acc:
        if itr >= 100:
            return 'Матрица расходится'
        itr += 1
        x1 = [i for i in x]
        x = (vect - np.dot(R,x)) / D
        fin = abs(x1 - x)
    return x

# Метод простых итераций Якоби

def jacobian_method(mtx):
    mtx1 = str_to_complex(mtx)
    coeff = coeff_mtx(mtx1)
    vect = coeff_vect(mtx1)
    n = len(mtx)
    print('Прямая матрица коэффициентов:')
    for i in range(n):
        print(coeff[i])
    rev = inverse_matrix(coeff)
    print('Обратная матрица коэффициентов:')
    for i in range(n):
        print(rev[i])
    print('Решение СЛАУ методом простых итераций Якоби:')
    mtx2 = np.array(mtx1)
    x = np.array([0 for i in range(n)])
    acc = 0.001
    sol = jacobi(mtx2, x, acc)
    print(sol)
    print('Число обусловленности Матрицы Коэффициентов A: ')
    conditional_jac = LA.cond(coeff)
    print(conditional_jac)
    return conditional_jac

#Вычилсение методом Гаусаа-Жордана

def GJ_method(mtx1):
    mtx = copy.deepcopy(mtx1)
    n = len(mtx)
    if det_my_matrix(mtx) == 0:
        return 'Вырожденная матрица. Нормально не считается этим методом'
    for itr in range(n):
        mtx[itr] = [mtx[itr][i] / mtx[itr][itr] for i in range(n + 1)]
        for col in range(n):
            if col != itr:
                mtx[col] = [mtx[col][i] - mtx[itr][i] * mtx[col][itr] for i in range(n + 1)]
    for row in mtx:
        for i in range(len(row)):
            row[i] = complex_to_num(row[i])
            if abs(row[i]) < 10 ** -10:
                row[i] = 0
    return coeff_vect(mtx)

# Метод Гаусаа-Жордана  
    
def jordan_method(mtx):
    mtx1 = str_to_complex(mtx)
    coeff = coeff_mtx(mtx1)
    vect = coeff_vect(mtx1)
    n = len(mtx)
    print('Прямая матрица коэффициентов:')
    for i in range(n):
        print(coeff[i])
    rev = inverse_matrix(coeff)
    print('Обратная матрица коэффициентов:')
    for i in range(n):
        print(rev[i])
    print('Решение СЛАУ методом Жордана-Гаусса:')
    sol = GJ_method(mtx1)
    print(sol)
    print('Число обусловленности Матрицы Коэффициентов A: ')
    conditional_gauss = LA.cond(coeff)
    print(conditional_gauss)
    return conditional_gauss

#Вычилсение методом Гаусаа-Жордана для правильных дробей

def GJ_method_2(mtx1):
    mtx = copy.deepcopy(mtx1)
    n = len(mtx)
    if det_my_matrix(mtx) == 0:
        return 'Вырожденная матрица. Нормально не считается этим методом'
    for itr in range(n):
        mtx[itr] = [mtx[itr][i] / mtx[itr][itr] for i in range(n + 1)]
        for col in range(n):
            if col != itr:
                mtx[col] = [mtx[col][i] - mtx[itr][i] * mtx[col][itr] for i in range(n + 1)]
    ans = coeff_vect(mtx)
    return ans

# Метод Гаусаа-Жордана для правильных дробей
    
def jordan_method_2(mtx):
    mtx1 = numbers_to_fractions(mtx)
    coeff = coeff_mtx(mtx1)
    vect = coeff_vect(mtx1)
    n = len(mtx)
    print('Прямая матрица коэффициентов:')
    for i in range(n):
        print(coeff[i])
    rev = inverse_matrix(coeff)
    print('Обратная матрица коэффициентов:')
    for i in range(n):
        print(rev[i])
    print('Решение СЛАУ методом Жордана-Гаусса для Дробей:')
    sol = GJ_method_2(mtx1)
    for i in range(len(sol)):
        print(f'Значение x[{i + 1}] = {sol[i]}')
    for i in range(len(coeff)):
        for j in range(len(coeff[i])):
            coeff[i][j] = float(coeff[i][j])
    conditional_gauss2 = LA.cond(coeff)
    print('Число обусловленности Матрицы Коэффициентов A: ')
    print(conditional_gauss2)
    return conditional_gauss2

# Основное тело программы

def main():
    """
    Принимает матрицу 
    ДЕалет рассчеты по формуле
    Выводит итоговую матрицу
    """
    matrix=iteration()
    print('Введённая матрица:')
    print(matrix)
    print('Матрица коэфициентов:(Будет выводиться М а если матрица вырожденная)')
    print(coeff_mtx(matrix))
    print('Вектор свободных значений:')
    print(coeff_vect(matrix))
    jac = jacobian_method(matrix)
    if jac > 100:
        return 'Программа завершилась.'
    gauss = jordan_method(matrix)
    if gauss > 100:
        return 'Программа завершилась.'
    for row in matrix:
        for col in row:
            if 'i' in col:
                print('Нельзя считать дроби с комплексными числами.')
                print('Хотите ли попробовать ввести матрицу ещё раз? \n 1 - да \n 2 - нет')
                try:    
                    choice = int(input())
                    ext = lambda: 'Программа завершилась.'
                    choices_dict = {1: main, 2: ext}
                    mtx = choices_dict[choice]()
                except KeyError:
                    print('Введено неверное значение для ответа на вопрос. Запущен повторный ввод матрицы')
                    return main()
                except ValueError:
                    print('Введено неверное значение для ответа на вопрос. Запущен повторный ввод матрицы')
                    return main()
                return mtx
    try:
        gauss2 = jordan_method_2(matrix)
    except np.linalg.LinAlgError as err:
        print('Ошибка вычислений. Введена вырожденная матрица для которой не считается число обусловленности')
        print('Хотите ли попробовать ввести матрицу ещё раз? \n 1 - да \n 2 - нет')
        try:    
            choice = int(input())
            ext = lambda: 'Программа завершилась.'
            choices_dict = {1: main, 2: ext}
            mtx = choices_dict[choice]()
        except KeyError:
            print('Введено неверное значение для ответа на вопрос. Запущен повторный ввод матрицы')
            return main()
        except ValueError:
            print('Введено неверное значение для ответа на вопрос. Запущен повторный ввод матрицы')
            return main()
        return mtx


# In[3]:


#matrix=iteration()
#print('Введённая матрица:')
#print(matrix)
#print('Матрица коэфициентов:(Будет выводиться М а если матрица вырожденная)')
#print(coeff_mtx(matrix))
#print('Вектор свободных значений:')
#print(coeff_vect(matrix))


# #### Метод простых итераций Якоби

# In[4]:


#jacobi_matrix=copy.deepcopy(matrix)
#jacobian_method(jacobi_matrix)


# ### Прямой алгоритм Гаусса-Жордана

# In[5]:


#Gauss_Jordan_matrix = copy.deepcopy(matrix)
#jordan_method(Gauss_Jordan_matrix)


# ### Прямой алгоритм Гаусса Жордана, с вычислениями правильных дробей

# In[6]:


#Gauss_Jordan_matrix_2 = copy.deepcopy(matrix)
#jordan_method_2(Gauss_Jordan_matrix_2)


# In[7]:


#main()


# In[ ]:




