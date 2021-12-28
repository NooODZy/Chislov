import numpy as np
from sympy import *
from scipy.integrate import odeint
import pandas as pd
import time
import matplotlib.pyplot as plt
from matplotlib import rcParams
import webbrowser
import random
import copy
import csv
import time


def coeff_vect(mtx):
    """Входные данные: mtx
        Выходныее данные: mtx1
        Функция выполняет ... действиия
    """
    mtx1 = []
    for i in range(len(mtx)):
        mtx1.append(mtx[i][-1])
    return mtx1

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
    return coeff_vect(mtx)

def quadratic_function(X,Y):
    sumX4 = sum([X[i] * X[i] * X[i] * X[i] for i in range(len(X))])
    sumX3 = sum([X[i] * X[i] * X[i] for i in range(len(X))])
    sumX2 = sum([X[i] * X[i] for i in range(len(X))])
    sumXY = sum([X[i] * Y[i] for i in range(len(X))])
    sumX2Y = sum([X[i] * X[i] * Y[i] for i in range(len(X))])
    
    matrix = [[sumX4, sumX3, sumX2, sumX2Y], [sumX3, sumX2, sum(X), sumXY], [sumX2, sum(X), len(X), sum(Y)]]
    
    GJ_method_abc = GJ_method_2(matrix)
    a = GJ_method_abc[0]
    b = GJ_method_abc[1]
    c = GJ_method_abc[2]
    
    x = Symbol('x')
    result = (eval('x')**2)*a + b*eval('x') + c
    
    return(result)

def newton1_function(X,Y):
    h=X[1]-X[0]
    
    # Найдем конечные разности
    y = copy.deepcopy(Y)
    deltay = [y[0]]
    while len(y) != 1:
        y = [y[i]-y[i-1] for i in range(1,len(y))]
        deltay.append(y[0])

    result=deltay[0]
    
    x = Symbol('x')
    deltax = [eval('x')-X[0]]
    for i in range(1,len(deltay)-1):
        deltax.append(deltax[i-1]*(eval('x') - X[i]))

    for i in range(1,len(deltax)+1):
        deltay[i] /= h**(i) * factorial(i)
        result+=(deltay[i]*deltax[i-1])
    return result

def function(x,y,z,col):
    if col == 1:
        f = [eval(input("y' = "))]
    elif col == 2:
        f1 = eval(input("y' = "))
        f2 = eval(input("z' = "))
        f = [f1,f2]
    return f

def diff_my(y1, y0, dx):
    y = (y1 - y0) / dx 
    return y

def iteration():
    
    x = Symbol('x')
    y = Symbol('y')
    z = Symbol('z')
    
    system = input('Хотите ли вы ввести систему из двух уравнений? (Да/Нет):')
    
    if system.lower() == 'нет':
        func = function(x,y,z,1)
        z0 = '-'
        try:
            x0y0 = list(map(float,input('Введите начальные условия [x0,y0]: ').split()))
            x0 = x0y0[0]
            y0 = x0y0[1]
        except ValueError:
            print('Ошибка ввода. Попробуйте ещё раз.')
            return iteration()
        except IndexError:
            print('Введено слишком мало чисел. Попробуйте ещё раз.')
            return iteration()
        
        try:
            ab = list(map(int,input('Введите желаемый интервал [a,b]: ').split()))
            a = ab[0]
            b = ab[1]
        except ValueError:
            print('Ошибка ввода. Попробуйте ещё раз.')
            return iteration()
        except IndexError:
            print('Введено слишком мало чисел. Попробуйте ещё раз.')
            return iteration()
        
        if a > b:
            print(f'Ошибка в вводе интервала! ({a}!>{b})!!')
            return iteration()
    
    elif system.lower() == 'да':
        func = function(x,y,z,2)
        
        try:
            x0y0 = list(map(float,input('Введите начальные условия [x0,y0,z0]: ').split()))
            x0 = x0y0[0]
            y0 = x0y0[1]
            z0 = x0y0[2]
        except ValueError:
            print('Ошибка ввода. Попробуйте ещё раз.')
            return iteration()
        except IndexError:
            print('Введено слишком мало чисел. Попробуйте ещё раз.')
            return iteration()
    
        try:
            ab = list(map(int,input('Введите желаемый интервал [a,b]: ').split()))
            a = ab[0]
            b = ab[1]
        except ValueError:
            print('Ошибка ввода. Попробуйте ещё раз.')
            return iteration()
        except IndexError:
            print('Введено слишком мало чисел. Попробуйте ещё раз.')
            return iteration()
        if a > b:
            print(f'Ошибка в вводе интервала! ({a}!>{b})!!')
            return iteration()
        
    n = int(input('Введите количество точек (n): '))
    
    return(func,x0,y0,z0,a,b,n)

# Одно уравнение

def iteration_once():
    
    x = Symbol('x')
    y = Symbol('y')
    z = Symbol('z')
    
    func = function(x,y,z,1)
    try:
        x0y0 = list(map(float,input('Введите начальные условия [x0,y0]: ').split()))
        x0 = x0y0[0]
        y0 = x0y0[1]
    except ValueError:
        print('Ошибка ввода. Попробуйте ещё раз.')
        return iteration_once()
    except IndexError:
        print('Введено слишком мало чисел. Попробуйте ещё раз.')
        return iteration_once()

    try:
        ab = list(map(int,input('Введите желаемый интервал [a,b]: ').split()))
        a = ab[0]
        b = ab[1]
    except ValueError:
        print('Ошибка ввода. Попробуйте ещё раз.')
        return iteration_once()
    except IndexError:
        print('Введено слишком мало чисел. Попробуйте ещё раз.')
        return iteration_once()

    if a > b:
        print(f'Ошибка в вводе интервала! ({a}!>{b})!!')
        return iiteration_once()
        
    n = int(input('Введите количество точек (n): '))
    
    return(func,x0,y0,a,b,n)

# Система уравнений

def iteration_system():
    
    x = Symbol('x')
    y = Symbol('y')
    z = Symbol('z')

    func = function(x,y,z,2)

    try:
        x0y0 = list(map(float,input('Введите начальные условия [x0,y0,z0]: ').split()))
        x0 = x0y0[0]
        y0 = x0y0[1]
        z0 = x0y0[2]
    except ValueError:
        print('Ошибка ввода. Попробуйте ещё раз.')
        return iteration_system()
    except IndexError:
        print('Введено слишком мало чисел. Попробуйте ещё раз.')
        return iteration_system()
    
    try:
        ab = list(map(int,input('Введите желаемый интервал [a,b]: ').split()))
        a = ab[0]
        b = ab[1]
    except ValueError:
        print('Ошибка ввода. Попробуйте ещё раз.')
        return iteration_system()
    except IndexError:
        print('Введено слишком мало чисел. Попробуйте ещё раз.')
        return iteration_system()
    if a > b:
        print(f'Ошибка в вводе интервала! ({a}!>{b})!!')
        return iteration_system()
        
    n = int(input('Введите количество точек (n): '))
    
    return(func,x0,y0,z0,a,b,n)

def euler(func, x0, y0, z0, a, b, n):
    h = (b-a)/n
    x = np.arange(x0,x0+(b-a),h)
    X = Symbol('x')
    Y = Symbol('y')
    Z = Symbol('z')
    if type(z0) == type(''):
        res = [[i, x[i], 0] for i in range(n)]
        res[0][2] = y0
        for i in range(1,n):
            res[i][0] = i
            res[i][1] = x[i]
            res[i][2] = res[i-1][2] + (h*func[0].subs([(X,res[i-1][1]),(Y,res[i-1][2])]))
    
    else:
        res = [[i, x[i], 0, 0] for i in range(n)]
        res[0][2] = y0
        res[0][3] = z0
        for i in range(1,n):
            res[i][0] = i
            res[i][1] = x[i]
            res[i][2] = res[i-1][2] + (h*func[0].subs([(X,res[i-1][1]),(Y,res[i-1][2]),(Z,res[i-1][3])]))
            res[i][3] = res[i-1][3] + (h*func[1].subs([(X,res[i-1][1]),(Y,res[i-1][2]),(Z,res[i-1][3])]))
    return res

# Одно уравнение

def euler_once(func, x0, y0, a, b, n):
    h = (b-a)/n
    x = np.arange(x0,x0+(b-a),h)
    X = Symbol('x')
    Y = Symbol('y')
    Z = Symbol('z')
    res = [[i, x[i], 0] for i in range(n)]
    res[0][2] = y0
    for i in range(1,n):
        res[i][0] = i
        res[i][1] = x[i]
        res[i][2] = res[i-1][2] + (h*func[0].subs([(X,res[i-1][1]),(Y,res[i-1][2])]))
    return res

# Система уравнений

def euler_system(func, x0, y0, z0, a, b, n):
    h = (b-a)/n
    x = np.arange(x0,x0+(b-a),h)
    X = Symbol('x')
    Y = Symbol('y')
    Z = Symbol('z')
    res = [[i, x[i], 0, 0] for i in range(n)]
    res[0][2] = y0
    res[0][3] = z0
    for i in range(1,n):
        res[i][0] = i
        res[i][1] = x[i]
        res[i][2] = res[i-1][2] + (h*func[0].subs([(X,res[i-1][1]),(Y,res[i-1][2]),(Z,res[i-1][3])]))
        res[i][3] = res[i-1][3] + (h*func[1].subs([(X,res[i-1][1]),(Y,res[i-1][2]),(Z,res[i-1][3])]))
    return res

def eulercauchy(func, x0, y0, z0, a, b, n):
    h = (b-a)/n
    x = np.arange(x0,x0+(b-a),h)
    X = Symbol('x')
    Y = Symbol('y')
    Z = Symbol('z')
    if type(z0) == type(''):
        _y = [0]*n
        _y[0] = y0
        for i in range(1,n):
            _y[i] = _y[i-1] + (h*func[0].subs([(X,x[i-1]),(Y,_y[i-1])]))
        res = [[i, x[i], 0] for i in range(n)]
        res[0][2] = y0
        for i in range(1,n):
            res[i][2] = res[i-1][2] + (h/2) * ((func[0].subs([(X,x[i-1]),(Y,res[i-1][2])]))+(func[0].subs([(X,x[i]),(Y,_y[i])])))
    
    else:
        _y = [0]*n
        _z = [0]*n
        _y[0] = y0
        _z[0] = z0
        for i in range(1,n):
            _y[i] = _y[i-1] + (h*func[0].subs([(X,x[i-1]),(Y,_y[i-1]),(Z,_z[i-1])]))
            _z[i] = _z[i-1] + (h*func[1].subs([(X,x[i-1]),(Y,_y[i-1]),(Z,_z[i-1])]))
        res = [[i, x[i], 0, 0] for i in range(n)]
        res[0][2] = y0
        res[0][3] = z0
        for i in range(1,n):
            res[i][2] = res[i-1][2] + (h/2) * ((func[0].subs([(X,x[i-1]),(Y,res[i-1][2]),(Z,res[i-1][3])]))+(func[0].subs([(X,x[i]),(Y,_y[i]),(Z,_z[i])])))
            res[i][3] = res[i-1][3] + (h/2) * ((func[1].subs([(X,x[i-1]),(Y,res[i-1][2]),(Z,res[i-1][3])]))+(func[1].subs([(X,x[i]),(Y,_y[i]),(Z,_z[i])])))
    return res

# Одно уравнение

def eulercauchy_once(func, x0, y0, a, b, n):
    h = (b-a)/n
    x = np.arange(x0,x0+(b-a),h)
    X = Symbol('x')
    Y = Symbol('y')
    Z = Symbol('z')
    _y = [0]*n
    _y[0] = y0
    for i in range(1,n):
        _y[i] = _y[i-1] + (h*func[0].subs([(X,x[i-1]),(Y,_y[i-1])]))
    res = [[i, x[i], 0] for i in range(n)]
    res[0][2] = y0
    for i in range(1,n):
        res[i][2] = res[i-1][2] + (h/2) * ((func[0].subs([(X,x[i-1]),(Y,res[i-1][2])]))+(func[0].subs([(X,x[i]),(Y,_y[i])])))
    return res

# Система уравнений

def eulercauchy_system(func, x0, y0, z0, a, b, n):
    h = (b-a)/n
    x = np.arange(x0,x0+(b-a),h)
    X = Symbol('x')
    Y = Symbol('y')
    Z = Symbol('z')
    _y = [0]*n
    _z = [0]*n
    _y[0] = y0
    _z[0] = z0
    for i in range(1,n):
        _y[i] = _y[i-1] + (h*func[0].subs([(X,x[i-1]),(Y,_y[i-1]),(Z,_z[i-1])]))
        _z[i] = _z[i-1] + (h*func[1].subs([(X,x[i-1]),(Y,_y[i-1]),(Z,_z[i-1])]))
    res = [[i, x[i], 0, 0] for i in range(n)]
    res[0][2] = y0
    res[0][3] = z0
    for i in range(1,n):
        res[i][2] = res[i-1][2] + (h/2) * ((func[0].subs([(X,x[i-1]),(Y,res[i-1][2]),(Z,res[i-1][3])]))+(func[0].subs([(X,x[i]),(Y,_y[i]),(Z,_z[i])])))
        res[i][3] = res[i-1][3] + (h/2) * ((func[1].subs([(X,x[i-1]),(Y,res[i-1][2]),(Z,res[i-1][3])]))+(func[1].subs([(X,x[i]),(Y,_y[i]),(Z,_z[i])])))
    return res

def rungekutta(func, x0, y0, z0, a, b, n):
    h = (b-a)/n
    x = np.arange(x0,x0+(b-a),h)
    X = Symbol('x')
    Y = Symbol('y')
    Z = Symbol('z')
    if type(z0) == type(''):
        res = [[i, x[i], 0] for i in range(n)]
        res[0][2] = y0
        for i in range(1,n):
            k1 = h * func[0].subs([(X,res[i-1][1]),(Y,res[i-1][2])])
            k2 = h * func[0].subs([(X,(res[i-1][1])+h/2),(Y,(res[i-1][2])+k1/2)])
            k3 = h * func[0].subs([(X,(res[i-1][1])+h/2),(Y,(res[i-1][2])+k2/2)])
            k4 = h * func[0].subs([(X,(res[i-1][1])+h),(Y,(res[i-1][2])+k3)])
            res[i][2] = res[i-1][2] + 1/6 * (k1 + 2*k2 + 2*k3 + k4)
    
    else:
        res = [[i, x[i], 0, 0] for i in range(n)]
        res[0][2] = y0
        res[0][3] = z0
        for i in range(1,n):
            k1y = h * func[0].subs([(X,res[i-1][1]),(Y,res[i-1][2]), (Z,res[i-1][3])])
            k2y = h * func[0].subs([(X,(res[i-1][1])+h/2),(Y,(res[i-1][2])+k1y/2), (Z,(res[i-1][3])+k1y/2)])
            k3y = h * func[0].subs([(X,(res[i-1][1])+h/2),(Y,(res[i-1][2])+k2y/2), (Z,(res[i-1][3])+k2y/2)])
            k4y = h * func[0].subs([(X,(res[i-1][1])+h),(Y,(res[i-1][2])+k3y),(Z,(res[i-1][3])+k3y)])
            res[i][2] = res[i-1][2] + 1/6 * (k1y + 2*k2y + 2*k3y + k4y)
            
            k1z = h * func[1].subs([(X,res[i-1][1]),(Y,res[i-1][2]), (Z,res[i-1][3])])
            k2z = h * func[1].subs([(X,(res[i-1][1])+h/2),(Y,(res[i-1][2])+k1z/2), (Z,(res[i-1][3])+k1z/2)])
            k3z = h * func[1].subs([(X,(res[i-1][1])+h/2),(Y,(res[i-1][2])+k2z/2), (Z,(res[i-1][3])+k2z/2)])
            k4z = h * func[1].subs([(X,(res[i-1][1])+h),(Y,(res[i-1][2])+k3z),(Z,(res[i-1][3])+k3z)])
            res[i][3] = res[i-1][3] + 1/6 * (k1z + 2*k2z + 2*k3z + k4z)
    return res

def rungekutta_once(func, x0, y0, a, b, n):
    h = (b-a)/n
    x = np.arange(x0,x0+(b-a),h)
    X = Symbol('x')
    Y = Symbol('y')
    Z = Symbol('z')
    res = [[i, x[i], 0] for i in range(n)]
    res[0][2] = y0
    for i in range(1,n):
        k1 = h * func[0].subs([(X,res[i-1][1]),(Y,res[i-1][2])])
        k2 = h * func[0].subs([(X,(res[i-1][1])+h/2),(Y,(res[i-1][2])+k1/2)])
        k3 = h * func[0].subs([(X,(res[i-1][1])+h/2),(Y,(res[i-1][2])+k2/2)])
        k4 = h * func[0].subs([(X,(res[i-1][1])+h),(Y,(res[i-1][2])+k3)])
        res[i][2] = res[i-1][2] + 1/6 * (k1 + 2*k2 + 2*k3 + k4)
    return res


def rungekutta_system(func, x0, y0, z0, a, b, n):
    h = (b-a)/n
    x = np.arange(x0,x0+(b-a),h)
    X = Symbol('x')
    Y = Symbol('y')
    Z = Symbol('z')
    res = [[i, x[i], 0, 0] for i in range(n)]
    res[0][2] = y0
    res[0][3] = z0
    for i in range(1,n):
        k1y = h * func[0].subs([(X,res[i-1][1]),(Y,res[i-1][2]), (Z,res[i-1][3])])
        k2y = h * func[0].subs([(X,(res[i-1][1])+h/2),(Y,(res[i-1][2])+k1y/2), (Z,(res[i-1][3])+k1y/2)])
        k3y = h * func[0].subs([(X,(res[i-1][1])+h/2),(Y,(res[i-1][2])+k2y/2), (Z,(res[i-1][3])+k2y/2)])
        k4y = h * func[0].subs([(X,(res[i-1][1])+h),(Y,(res[i-1][2])+k3y),(Z,(res[i-1][3])+k3y)])
        res[i][2] = res[i-1][2] + 1/6 * (k1y + 2*k2y + 2*k3y + k4y)

        k1z = h * func[1].subs([(X,res[i-1][1]),(Y,res[i-1][2]), (Z,res[i-1][3])])
        k2z = h * func[1].subs([(X,(res[i-1][1])+h/2),(Y,(res[i-1][2])+k1z/2), (Z,(res[i-1][3])+k1z/2)])
        k3z = h * func[1].subs([(X,(res[i-1][1])+h/2),(Y,(res[i-1][2])+k2z/2), (Z,(res[i-1][3])+k2z/2)])
        k4z = h * func[1].subs([(X,(res[i-1][1])+h),(Y,(res[i-1][2])+k3z),(Z,(res[i-1][3])+k3z)])
        res[i][3] = res[i-1][3] + 1/6 * (k1z + 2*k2z + 2*k3z + k4z)
    return res

def odeint_scp(func, x0, y0, a, b, n):
    h = (b-a)/n
    x = np.arange(x0,x0+(b-a),h)
    X = Symbol('x')
    Y = Symbol('y')
    Z = Symbol('z')
    f = lambdify([X,Y],func[0])
    res = [[i, x[i], 0] for i in range(n)]
    y = odeint(f,y0,np.array(x))
    for i in range(n):
        res[i][2] = float(y[i])
    return res


#func, x0, y0, z0, a, b, n = iteration()
#print(func)
#print(x0)
#print(y0)
#print(z0)
#print(a)
#print(b)
#print(n)


# In[11]:


#euler(func, x0, y0, z0, a, b, n)


# In[12]:


#eulercauchy(func, x0, y0, z0, a, b, n)


# In[13]:


#rungekutta(func, x0, y0, z0, a, b, n)


# #### Ввод одного уравнения

# In[27]:


#func, x0, y0, a, b, n = iteration_once()
#print(func)
#print(x0)
#print(y0)
#print(a)
#print(b)
#print(n)


# In[28]:


#euler_once(func, x0, y0, a, b, n)


# In[29]:


#eulercauchy_once(func, x0, y0, a, b, n)


# In[30]:


#rungekutta_once(func, x0, y0, a, b, n)


# In[31]:


##odeint_scp(func, x0, y0, a, b, n)


# #### Ввод системы уравнений




# #### Ввод одного уравнения

# In[12]:

def obertka():
    """
    Данная функция оборачивает код ниже для возможности избежания конфликта с константами, для возможности считывания кода библиотекой
    """
    func, x0, y0, a, b, n = iteration_once()

    t0 = time.time()
    result_euler = euler_once(func, x0, y0, a, b, n)
    t1_euler = time.time()
    t1_euler -= t0

    t0 = time.time()
    result_eulercauchy = eulercauchy_once(func, x0, y0, a, b, n)
    t1_eulercauchy = time.time()
    t1_eulercauchy -= t0

    t0 = time.time()
    result_rungekutta = rungekutta_once(func, x0, y0, a, b, n)
    t1_rungekutta = time.time()
    t1_rungekutta -= t0

    t0 = time.time()
    result_odeint_scp = odeint_scp(func, x0, y0, a, b, n)
    t1_odeint_scp = time.time()
    t1_odeint_scp -= t0

    xd = [result_euler[i][1] for i in range(n)]
    yd_euler = [result_euler[i][2] for i in range(n)]
    yd_eulercauchy = [result_eulercauchy[i][2] for i in range(n)]
    yd_rungekutta = [result_rungekutta[i][2] for i in range(n)]
    yd_odeint_scp = [result_odeint_scp[i][2] for i in range(n)]

    # Эйлер
    df_euler = pd.DataFrame({'xi':xd,'yi':yd_euler})
        
    print('--------------------------------------------------------------')
    print('Решение ОДУ методом Эйлера') 
    print(df_euler)

    # Эйлер-Коши
    df_eulercauchy = pd.DataFrame({'xi':xd,'yi':yd_eulercauchy})
        
    print('--------------------------------------------------------------')
    print('Решение ОДУ методом Эйлера-Коши') 
    print(df_eulercauchy)

    # Рунге-Кутта
    df_rungekutta = pd.DataFrame({'xi':xd,'yi':yd_rungekutta})
        
    print('--------------------------------------------------------------')
    print('Решение ОДУ методом Рунге-Кутты') 
    print(df_rungekutta)

    # scipy.integrate odeint
    df_odeint_scp = pd.DataFrame({'xi':xd,'yi':yd_odeint_scp})
        
    print('--------------------------------------------------------------')
    print('Решение ОДУ scipy.integrate odeint') 
    print(df_odeint_scp)

    dxa = xd[1] - xd[0]
    ymydiff = []
    for i in range(len(yd_odeint_scp) - 1):
        ansi = diff_my(yd_odeint_scp[1],yd_odeint_scp[0],dxa)
        ymydiff.append(ansi)

    df_ymydiff = pd.DataFrame({'xi':xd,'deltai':yd_odeint_scp})
    print('--------------------------------------------------------------')
    print('Разность между yi и y' + "'" + 'i') 
    print(df_ymydiff)       
        
    deltai = [(yd_odeint_scp[i] - ymydiff[i]) for i in range(len(ymydiff))]
    sumx = sum([abs(t) for t in deltai])
    rcParams['figure.figsize'] = (30, 20)
    rcParams['figure.dpi'] = 300
    fig = plt.figure()
    fig,ax = plt.subplots()

    plt.tick_params(labelsize = 40)
    plt.grid(b=True, color='DarkTurquoise', alpha=0.75, linestyle=':', linewidth=1)
    ax.plot(xd[:-1],deltai,color='blue',lw=2,label='Y - Y' + "'")
    ax.plot(xd[:-1],deltai,color='blue',lw=0,label=f'Сумма отклонений = {sumx}')
    ax.legend(loc='lower right',title='Легенда',title_fontsize=25,fontsize=20)
    plt.show()


    # In[36]:


    rcParams['figure.figsize'] = (30, 20)
    rcParams['figure.dpi'] = 300

    fig,ax=plt.subplots()

    plt.tick_params(labelsize = 40)
    plt.grid(b=True, color='DarkTurquoise', alpha=0.75, linestyle=':', linewidth=1)

    ax.plot(xd,yd_euler,color='blue',lw=2,label='Решение ОДУ методом Эйлера')
    ax.plot(xd,yd_eulercauchy,color='red',lw=2,label='Решение ОДУ методом Эйлера-Коши')
    ax.plot(xd,yd_rungekutta,color='green',lw=2,label='Решение ОДУ методом Рунге-Кутты')
    ax.plot(xd,yd_odeint_scp,color='black',lw=2,label='Решение ОДУ scipy.integrate odeint')

    ax.set_title('Решение ОДУ')
    ax.legend(loc='lower right',title='Легенда',title_fontsize=25,fontsize=15)

    plt.xlabel('X',fontsize=25)
    plt.ylabel('Y',fontsize=25)

    print(f'Аппроксимация МНК для метода Эйлера (XY): \n {quadratic_function(xd,yd_euler)}')
    print(f'Интерполяция через первую формулу Ньютона для метода Эйлера (XY): \n {expand(newton1_function(xd,yd_euler))}')
    print('-----------------------------------------------------------------------------------')
    print(f'Аппроксимация МНК для метода Эйлера-Коши (XY): \n {quadratic_function(xd,yd_eulercauchy)}')
    print(f'Интерполяция через первую формулу Ньютона для метода Эйлера-Коши (XY): \n {expand(newton1_function(xd,yd_eulercauchy))}')
    print('-----------------------------------------------------------------------------------')
    print(f'Аппроксимация МНК для метода Рунге-Кутты (XY): \n {quadratic_function(xd,yd_rungekutta)}')
    print(f'Интерполяция через первую формулу Ньютона для метода Рунге-Кутты (XY): \n {expand(newton1_function(xd,yd_rungekutta))}')
    print('-----------------------------------------------------------------------------------')
    print(f'Аппроксимация МНК для метода Рунге-Кутты (XY): \n {quadratic_function(xd,yd_odeint_scp)}')
    print(f'Интерполяция через первую формулу Ньютона для метода Рунге-Кутты (XY): \n {expand(newton1_function(xd,yd_odeint_scp))}')

    t=[]
    print(f'Время работы метода Эйлера: {t1_euler}.')
    t.append(t1_euler)
    print(f'Время работы метода Эйлера-Коши: {t1_eulercauchy}.')
    t.append(t1_eulercauchy)
    print(f'Время работы метода Рунге-Кутты: {t1_rungekutta}.')
    t.append(t1_rungekutta)
    print(f'Время работы метода из библиотеки: {t1_odeint_scp}.')
    t.append(t1_odeint_scp)


    # In[14]:


    rcParams['figure.figsize'] = (30, 20)
    rcParams['figure.dpi'] = 300

    fig,ax=plt.subplots()

    plt.tick_params(labelsize = 40)
    plt.grid(b=True, color='DarkTurquoise', alpha=0.75, linestyle=':', linewidth=1)

    plt.bar(0, t[0], color = 'purple', label = 'Время работы метода Эйлера') 
    plt.bar(1, t[1], color = 'yellow', label = 'Время работы метода Эйлера-Коши') 
    plt.bar(2, t[2], color = 'lime', label = 'Время работы метода Рунге-Кутты')
    plt.bar(3, t[3], color = 'red', label = 'Время работы метода из библиотеки') 

    ax.set_title('Анализ времени работы программ', loc = 'center')
    ax.legend(loc='lower right',title='Легенда',title_fontsize=25,fontsize=15)

    plt.ylabel('Время (cек.)',fontsize=25)

    plt.show()


    # #### Ввод системы уравнений

    # In[15]:


    func, x0, y0, z0, a, b, n = iteration_system()

    t0 = time.time()
    result_euler = euler_system(func, x0, y0, z0, a, b, n)
    t1_euler = time.time()
    t1_euler -= t0

    t0 = time.time()
    result_eulercauchy = eulercauchy_system(func, x0, y0, z0, a, b, n)
    t1_eulercauchy = time.time()
    t1_eulercauchy -= t0

    t0 = time.time()
    result_rungekutta = rungekutta_system(func, x0, y0, z0, a, b, n)
    t1_rungekutta = time.time()
    t1_rungekutta -= t0

    xd = [result_euler[i][1] for i in range(n)]
    yd_euler = [result_euler[i][2] for i in range(n)]
    yd_eulercauchy = [result_eulercauchy[i][2] for i in range(n)]
    yd_rungekutta = [result_rungekutta[i][2] for i in range(n)]

    # Эйлер
    zd_euler = [result_euler[i][3] for i in range(n)]
    df_euler = pd.DataFrame({'xi':xd,'yi':yd_euler,'zi':zd_euler})
        
    print('--------------------------------------------------------------')
    print('Решение ОДУ методом Эйлера') 
    print(df_euler)

    # Эйлер-Коши
    zd_eulercauchy = [result_eulercauchy[i][3] for i in range(n)]
    df_eulercauchy = pd.DataFrame({'xi':xd,'yi':yd_eulercauchy,'zi':zd_eulercauchy})
        
    print('--------------------------------------------------------------')
    print('Решение ОДУ методом Эйлера-Коши') 
    print(df_eulercauchy)

    # Рунге-Кутта
    zd_rungekutta = [result_rungekutta[i][3] for i in range(n)]
    df_rungekutta = pd.DataFrame({'xi':xd,'yi':yd_rungekutta,'zi':zd_rungekutta})
        
    print('--------------------------------------------------------------')
    print('Решение ОДУ методом Рунге-Кутты') 
    print(df_rungekutta)


    # In[16]:


    fig = plt.figure()

    rcParams['figure.figsize'] = (30, 20)
    rcParams['figure.dpi'] = 300

    axes = fig.subplots(nrows=2, ncols=1)

    axes[0].plot(xd,yd_euler,color='blue',lw=2,label='Решение ОДУ методом Эйлера')
    axes[0].plot(xd,yd_eulercauchy,color='red',lw=2,label='Решение ОДУ методом Эйлера-Коши')
    axes[0].plot(xd,yd_rungekutta,color='green',lw=2,label='Решение ОДУ методом Рунге-Кутты')
    axes[0].grid(b=True, color='DarkTurquoise', alpha=0.75, linestyle=':', linewidth=1)
    axes[0].set_title('XY',fontfamily = 'fantasy', loc = 'left')
    axes[0].set_xlabel('X')
    axes[0].set_ylabel('Y')

    axes[1].plot(xd,zd_euler,color='blue',lw=2)
    axes[1].plot(xd,zd_eulercauchy,color='red',lw=2)
    axes[1].plot(xd,zd_rungekutta,color='green',lw=2)
    axes[1].grid(b=True, color='DarkTurquoise', alpha=0.75, linestyle=':', linewidth=1)
    axes[1].set_title('XZ',fontfamily = 'fantasy',loc = 'left')
    axes[1].set_xlabel('X')
    axes[1].set_ylabel('Z')

    lines = []
    labels = []

    for ax in fig.axes:
        axLine, axLabel = ax.get_legend_handles_labels()
        lines.extend(axLine)
        labels.extend(axLabel)

    fig.legend(lines, labels,           
            loc = 'upper right',
            fontsize=30)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    plt.tick_params(labelsize = 40)
    plt.grid(b=True, color='DarkTurquoise', alpha=0.75, linestyle=':', linewidth=1)

    ax.plot(xd,yd_euler,zd_euler,color='blue',lw=2,label='Решение ОДУ методом Эйлера')
    ax.plot(xd,yd_eulercauchy,zd_eulercauchy,color='red',lw=2,label='Решение ОДУ методом Эйлера-Коши')
    ax.plot(xd,yd_rungekutta,zd_rungekutta,color='green',lw=2,label='Решение ОДУ методом Рунге-Кутты')

    ax.set_title('Решение ОДУ')
    ax.legend(loc='lower right',title='Легенда',title_fontsize=25,fontsize=15)

    plt.xlabel('X',fontsize=25)
    plt.ylabel('Y',fontsize=25)

    print(f'Аппроксимация МНК для метода Эйлера (XY): \n {quadratic_function(xd,yd_euler)}')
    print(f'Интерполяция через первую формулу Ньютона для метода Эйлера (XY): \n {expand(newton1_function(xd,yd_euler))}')
    print('-----------------------------------------------------------------------------------')
    print(f'Аппроксимация МНК для метода Эйлера-Коши (XY): \n {quadratic_function(xd,yd_eulercauchy)}')
    print(f'Интерполяция через первую формулу Ньютона для метода Эйлера-Коши (XY): \n {expand(newton1_function(xd,yd_eulercauchy))}')
    print('-----------------------------------------------------------------------------------')
    print(f'Аппроксимация МНК для метода Рунге-Кутты (XY): \n {quadratic_function(xd,yd_rungekutta)}')
    print(f'Интерполяция через первую формулу Ньютона для метода Рунге-Кутты (XY): \n {expand(newton1_function(xd,yd_rungekutta))}')
    print('-----------------------------------------------------------------------------------')

    print(f'Аппроксимация МНК для метода Эйлера (XZ): \n {quadratic_function(xd,zd_euler)}')
    print(f'Интерполяция через первую формулу Ньютона для метода Эйлера (XZ): \n {expand(newton1_function(xd,zd_euler))}')
    print('-----------------------------------------------------------------------------------')
    print(f'Аппроксимация МНК для метода Эйлера-Коши (XZ): \n {quadratic_function(xd,zd_eulercauchy)}')
    print(f'Интерполяция через первую формулу Ньютона для метода Эйлера-Коши (XZ): \n {expand(newton1_function(xd,zd_eulercauchy))}')
    print('-----------------------------------------------------------------------------------')
    print(f'Аппроксимация МНК для метода Рунге-Кутты (XZ): \n {quadratic_function(xd,zd_rungekutta)}')
    print(f'Интерполяция через первую формулу Ньютона для метода Рунге-Кутты (XZ): \n {expand(newton1_function(xd,zd_rungekutta))}')

    plt.show()

    t=[]
    print(f'Время работы метода Эйлера: {t1_euler}.')
    t.append(t1_euler)
    print(f'Время работы метода Эйлера-Коши: {t1_eulercauchy}.')
    t.append(t1_eulercauchy)
    print(f'Время работы метода Рунге-Кутты: {t1_rungekutta}.')
    t.append(t1_rungekutta)


    # In[17]:


    rcParams['figure.figsize'] = (30, 20)
    rcParams['figure.dpi'] = 300

    fig,ax=plt.subplots()

    plt.tick_params(labelsize = 40)
    plt.grid(b=True, color='DarkTurquoise', alpha=0.75, linestyle=':', linewidth=1)

    plt.bar(0, t[0], color = 'purple', label = 'Время работы метода Эйлера') 
    plt.bar(1, t[1], color = 'yellow', label = 'Время работы метода Эйлера-Коши') 
    plt.bar(2, t[2], color = 'lime', label = 'Время работы метода Рунге-Кутты')

    ax.set_title('Анализ времени работы программ', loc = 'center')
    ax.legend(loc='lower right',title='Легенда',title_fontsize=25,fontsize=15)

    plt.ylabel('Время (cек.)',fontsize=25)

    plt.show()
#obertka()

# In[ ]:




