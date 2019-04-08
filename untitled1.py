import numpy as np
import matplotlib.pyplot as plt
import math 
import time
from scipy.integrate import odeint
import classes as cl
import trajectory_module as tr

        
drone = cl.copter([-4.5,-4,0],
                  [1,1,0])
obs_p = [0,0,0]
R = 4

plt.scatter(obs_p[0],obs_p[1])

path = cl.path2('trj')
path.add(drone.pose[0],
         drone.pose[1])

tr.func_str_l(tr.func_ext_cond,drone,obs_p,R,path)
#tr.func_obs(tr.func_int_cond,drone.pose,obs_p,drone.vel,R,path)

#-------------------------------------------------------------
drone_pose = drone.pose
drone_vel = drone.vel
obs = obs_p

while tr.func_int_cond(drone_pose,obs,R):
    tr.func_obs_upd(drone_pose,obs,drone_vel,path)
    if path.len()>50000 : break

    
#-------------------------------------------------------------
f = np.arange(0,2*np.pi,0.05)

plt.plot(obs_p[0]+R*np.cos(f),
         obs_p[1]+R*np.sin(f))
path.plot()

plt.plot(obs_p[0]+np.cos(np.linspace(0,2*np.pi,40)),
         obs_p[1]+np.sin(np.linspace(0,2*np.pi,40)))
plt.grid()
plt.axis('equal')
plt.legend()
plt.show()    