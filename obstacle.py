# рабочая функция для обхода препятствия

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint

def func(y,x,a,deg,k,y0):
    return -np.sign(y0)*a*k**(deg-1)*x*np.exp(-x**2/k)

a = 1.4
deg = 0.5

x = np.linspace(-5,5,100)
y0 = 0.5
k = 9

#for y0 in np.arange(-1.1,1.1,0.3):
for k in range(3,11,2):
    y = odeint(func,y0,x,args=(a-abs(y0),deg,k,y0))
    s = 'k='+str(k)
    plt.plot(x,y,label=s)

cx = np.linspace(0,2*np.pi,40)
plt.plot(np.cos(cx),np.sin(cx))
R =4
plt.plot(R*np.cos(cx),R*np.sin(cx))

plt.grid()
plt.axis('equal')
#plt.legend()
plt.show()