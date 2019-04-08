import time
import math
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
import classes as cl
        
# par = [m,b,k] - параметр, содержит характеристики пружины
# eq - координата положения равновесия

# HUMAN IMPEDANCE
def Spring(state,t,F,eq,par):
    x = state[0]
    xd = state[1]
    m = par[0]
    b = par[1]
    k = par[2]
    xdd = -(b/m)*xd - (k/m)*(x-eq) + F/m
    return [xd, xdd]

# диффур, описывающий движение по прямой, использую, как
# внешнюю функцию
def straight_line(state,t):
    return [state[1],0]
           
# функция условия 
def func_ext_cond(pose1,pose2,distance):
    d = 0
    for i in range(3):
        d += (pose1[i]-pose2[i])**2
    return math.sqrt(d)>distance

def func_int_cond(pose1,pose2,distance):
    d = 0
    for i in range(3):
        d += (pose1[i]-pose2[i])**2
    return math.sqrt(d)<=distance

#--------------------------------------------------------------------

def func_str_l(cond_func,drone,obstacle_pose,R,path):
    
    while cond_func(drone.pose,obstacle_pose,R):
                
        time_step = time.time() - drone.time
        drone.time = time.time()
        t = [0. , time_step]
    
        state0_x = [drone.pose[0], drone.vel[0]]
        state0_y = [drone.pose[1], drone.vel[1]]
        state0_z = [drone.pose[2], drone.vel[2]]
        
        state_x = odeint(straight_line, state0_x, t)
        state_y = odeint(straight_line, state0_y, t)
        state_z = odeint(straight_line, state0_z, t)
        
        state_x = state_x[1]    
        state_y = state_y[1]    
        state_z = state_z[1]
        
        drone.pose = np.array( [state_x[0], state_y[0], state_z[0]] )
        drone.vel  = np.array( [state_x[1], state_y[1], state_z[1]] )
        
        path.add(drone.pose[0],
                 drone.pose[1])
        if path.len()>50000: break

#---------------------------------------------------------------------

# основная функция, которая выполняет весь код
        
def func_spring(cond_f,drone,obs,par,f_ext,F_par,R,traj):

    param = 1 # r = R/param - радиус "равновесия", при param=1 => R=r
    df = 1e-2    
        
    eq = cl.to_rect2([R/param,drone.fi()]) 
    pose_eq = [eq[0],eq[1],0]
    
    #plt.figure(1,figsize=(6,6),dpi = 200)
    plt.scatter(drone.pose[0],drone.pose[1]) # ставлю начальную точку
    plt.scatter(obs[0],obs[1])                         # ставлю препятствие
    
    # создаю радиус притяжения, равновесия и саму траекторию
    c = cl.path2('range')
    equ = cl.path2('equilibrium')
    traj.add(drone.pose[0],
             drone.pose[1])
    
    t = np.array([drone.time])
        
    while cond_f(drone.pose,obs,R):         
        time_step = time.time() - drone.time
        drone.time = time.time()
        t = [0. , time_step]
        
        F = drone.angle_2d_cos()*F_par
    
        state0_x = [drone.pose[0], drone.vel[0]]
        state0_y = [drone.pose[1], drone.vel[1]]
        state0_z = [drone.pose[2], drone.vel[2]]
        
        state_x = odeint(f_ext, state0_x, t, args=(F[0],pose_eq[0],par))
        state_y = odeint(f_ext, state0_y, t, args=(F[1],pose_eq[1],par))
        state_z = odeint(f_ext, state0_z, t, args=(F[2],pose_eq[2],par))
        
        state_x = state_x[1]    
        state_y = state_y[1]    
        state_z = state_z[1]
        
        drone.pose = np.array( [state_x[0], state_y[0], state_z[0]] )
        drone.vel  = np.array( [state_x[1], state_y[1], state_z[1]] )
        
        r = cl.to_polar2(drone.pose-obs)
    
        if traj.len()>50000: break
        eq = cl.to_rect2([R/param,r[1]+df])
        pose_eq = [eq[0]+obs[0],eq[1]+obs[1],0+obs[2]]
            
        equ.add(pose_eq[0], #x
                pose_eq[1]) #y    
        c.add(R*math.cos(r[1]), #x
              R*math.sin(r[1])) #y
        traj.add(drone.pose[0], #x
                 drone.pose[1]) #y      
        
    equ.plot()
    

def func(y,t,x,a,deg,k,y0):
    return -np.sign(y0)*(a-abs(y0))*k**(deg-1)*x*np.exp(-x**2/k)

def func_obs(cond_f,drone_pose,obs,drone_vel,R,trj):    
    a = 1.4
    k = 5
    deg = 0.4
    
    # переношу центр СК в "пряпятствие"
    x0 = drone_pose[0]-obs[0]
    y0 = drone_pose[1]-obs[1] 
    
    #  поворачиваю СК так, чтобы дрон двигался слева направо вдоль оси Х
    vr = cl.to_polar2([drone_vel[0],drone_vel[1]])
    
    x1 =  x0*math.cos(vr[1]) + y0*math.sin(vr[1])
    y1 = -x0*math.sin(vr[1]) + y0*math.cos(vr[1])
    vx =  vr[0]
    vy = 0
    
    plt.scatter(x1,y1)
    
    # массив точек в новых координатах
    x = np.array([x1])
    y = np.array([y1])
    ax = cl.path2('Ox')
    #vr[1] = np.pi/4
    tt = time.time()
    while cond_f(drone_pose,obs,R):
        time_step = time.time() - tt
        tt = time.time()
        t = [0. , time_step]
        
        y1 = odeint(func,y[-1],t,args=(x[-1],a,deg,k,y[0]))[1]    
        x1 = x[-1]+vx*time_step
        
        x = np.append(x,x1)
        y = np.append(y,y1)
                
        x0 = x1*math.cos(vr[1]) - y1*math.sin(vr[1])
        y0 = x1*math.sin(vr[1]) + y1*math.cos(vr[1])
        
        #x0 = x1
        #y0 = y1
        
        ax.add(x0,0)
        drone_pose = [x0,y0,drone_pose[2]]
        
        trj.add(drone_pose[0],
                drone_pose[1])

def new_func(obstacle,drone_pose,drone_vel):
    
    a = 1.4
    k = 7
    deg = 0.7
    
    tt = time.time()
    r = np.array([drone_pose[0]-obstacle[0],
                  drone_pose[1]-obstacle[1],
                  0])
    r[2] = (r[0]**2+r[1]**2)**0.5
#    cl.line(obs,obs+r,'r')

    v = np.array([drone_vel[0],drone_vel[1],0])
    vr = cl.to_polar2(v)
    v[2] = vr[0]
#    cl.line(r+obs,obs+r+v,'v from r')    
    
    c = r + v
    c[2] = (c[0]**2+c[1]**2)**0.5
#    cl.line(obs,obs+c,'c')
    
    al_r = math.atan2(-r[1],-r[0])
    al_v = vr[1]#math.atan2(v[1],v[0])
    al = al_v-al_r
    
    y = r[2]*math.sin(al)
    x = -r[2]*math.cos(al)
    vx = vr[0]
    vy = 0
    
    
    time_step = time.time() - tt
    t = [0. , time_step]
    
    y1 = odeint(func,y,t,args=(x,a,deg,k,y))[1]  
#    is_updated = False
#    if r[2]<R_ :
#        y = y1
#        is_updated = True
    y = y1
    x += vx*time_step
    
    fi = vr[1]           
    x0 =  x*math.cos(fi) - y*math.sin(fi)
    y0 =  x*math.sin(fi) + y*math.cos(fi)
    
    drone_pose = [x0,y0,drone_pose[2]]
    r = np.array([drone_pose[0]-obstacle[0],
              drone_pose[1]-obstacle[1],
              0])
    r[2] = (r[0]**2+r[1]**2)**0.5
    
#    return [drone_pose,r[2],is_updated]
    return [drone_pose,r[2]]