import math
import numpy as np
import matplotlib.pyplot as plt
import time

# переводит из еклидовой СК в поляруную, х - может быть и 3х-мерным   
def to_polar2(x):
    r = (x[0]**2+x[1]**2)**0.5
    f = math.atan2(x[1],x[0])
    return [r,f]

# переводит из полярной СК в евклидову, r - может быть и 3х-мерным   
def to_rect2 (r):
    x = r[0]*math.cos(r[1])
    y = r[0]*math.sin(r[1])
    return [x,y]

# переводит двумерный вектор скорости из еклидовой СК в поляруную
def v_2pol(v,x):
    r = to_polar2(x)
    vr = v[0]*math.cos(r[1]) + v[1]*math.sin(r[1])
    vf = (v[1]*math.cos(r[1]) - v[0]*math.sin(r[1]))/r[0]
    return [vr,vf]


# класс, содержащий все параметры дрона
class copter():
    
    # "сигнал" от человека
    hum_vel = np.array([0,0,0],dtype = float)
    
    # position - вектор координат
    pose = np.array([0,0,0],dtype = float)
    
    # вектор скорости
    vel = np.array([0,0,0],dtype = float)
    
    # метка времени (time_prev)
    time = time.time()
    
    # destination - координата точки назначения
    dest = np.array([0,0,0],dtype = float)
    
    # конструктор класса
    def __init__(self,pose,vel):
        self.pose = np.array([pose[0],pose[1],pose[2]])
        self.vel = np.array([vel[0],vel[1],vel[2]])
        self.hum_vel = np.array([0.,0.,0.])
        self.time = time.time()
    
    # возвращает расстояние до препятствия
    def r(self):
        return to_polar2(self.pose)[0]
    
    # возвращает угол
    def fi(self):
        return to_polar2(self.pose)[1]
    
    # возвращает расстояние до точки назначения
    def d(self):
        d = 0
        for i in range(2):
            d += (self.pose[i]-self.dest[i])**2
        return math.sqrt(d)
    
    # возвращает углы на точку назначения: [cos,sin,0], двумерная
    def angle_2d_cos(self):
        xa = self.dest[0]-self.pose[0]
        ya = self.dest[1]-self.pose[1]
        ra = math.sqrt(xa**2+ya**2)
        return np.array([xa/ra,ya/ra,0])


# класс, описывающий сами линии на графике, нужен для сокращения кода    
class path2():
    x = np.array([])
    y = np.array([])
    name = 'sample text'
    
    def __init__(self,name):
        self.name = name
    
    # добавляет к кривой еще одну точку    
    def add(self,x,y):
        self.x = np.append(self.x,x)
        self.y = np.append(self.y,y)
    
    # строит кривую    
    def plot(self):
        plt.plot(self.x,self.y, label = self.name)
        
    def len(self):
        return max(len(self.x),len(self.y))
    
def line(p1,p2,name):
    plt.scatter(p2[0],p2[1],marker = '*')
    plt.plot([p1[0],p2[0]],[p1[1],p2[1]],label = name)
    
    
    
    
    
    