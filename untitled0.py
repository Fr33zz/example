import time
import math
import numpy as np
import matplotlib.pyplot as plt
import trajectory_module as tr
import classes as cl

initial_pose = np.array([-1.,-0.4,0.])
initial_pose /= math.sqrt(initial_pose[0]**2+initial_pose[1]**2)
initial_pose *= 4
# |y0| <= 1.5 - рабочая зона

initial_vel  = np.array([2.,1.,0.])
initial_vel /= math.sqrt(initial_vel[0]**2+initial_vel[1]**2)
initial_vel *= 2

time_prev = time.time()

drone = cl.copter(initial_pose,initial_vel)
drone.d = [4,0,0]
obs = [0,0,0]
plt.scatter(obs[0],obs[1],label = 'obs')
plt.scatter(drone.pose[0],drone.pose[1])

R = 4
    
trj = cl.path2('trj')
trj.add(drone.pose[0],
        drone.pose[1])

r = np.array([drone.pose[0]-obs[0],
              drone.pose[1]-obs[1],0])
par = (r[0]**2+r[1]**2)**0.5

while par<1.2*R:  
    asd = tr.new_func(obs,drone.pose,drone.vel)
    drone.pose = asd[0]
    par = asd[1]
    trj.add(drone.pose[0],
            drone.pose[1])    
    if trj.len()>50000: break   
    
trj.plot()
        
plt.plot (obs[0] + np.cos(np.linspace(0,2*np.pi,40)),
          obs[1] + np.sin(np.linspace(0,2*np.pi,40)))

plt.plot (obs[0] + R*np.cos(np.linspace(0,2*np.pi,40)),
          obs[1] + R*np.sin(np.linspace(0,2*np.pi,40)))


plt.grid()
plt.axis('equal')
plt.legend()
plt.show()

