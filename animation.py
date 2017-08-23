
# coding: utf-8

# In[4]:

# """
# A simple example of an animated plot
# """
# %matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig, ax = plt.subplots()

x = np.arange(0, 2*np.pi, 0.01)
line, = ax.plot(x, np.sin(x))


def animate(i):
    line.set_ydata(np.sin(x + i / 10.0))  # update the data
    return line,


# Init only required for blitting to give a clean slate.
def init():
    line.set_ydata(np.ma.array(x, mask=True))
    return line,

ani = animation.FuncAnimation(fig, animate, np.arange(1, 200), init_func=init,
                              interval=25, blit=True)
plt.show()


# In[22]:

# Rocket Dynamics Visualization 3D  - 3D simulation of simulated of measured flight data
# Tom Fetter @2011-2016
# version 1.102


# First Install Python 2.7
# Install pywin from http://sourceforge.net/projects/pywin32/
# Install Vphyton from http://vpython.org/contents/download_windows.html
# from vpython import *
# from visual import *
# import string
# from math import *
# from visual.graph import *
# from rocketobjects import *
# from rocketequations import *

# g = 32    # acceleration due to gravity (f/sec^2)

# #Set Display Resolution
# display_x = 1920.0

# display_y = 1080.0-40.0


# t_max = 35             # set the maximum time for plots that may be less than the length of the data files


# maxscale = .5 * maxrange
# plot_rate = 30      # plot rate (frames per sec)
# calc_plot_interval = (1/delta_t)/plot_rate

# acc_ejection = 20.0*g  # set the accelleration limit for detecting the ejection charge

# beta = 0*pi/180     # orientation axis alignment offset

# if calc_plot_interval <= 1:
#     plot_interval = 1
#     plot_rate = plot_rate * calc_plot_interval
# else:
#     plot_interval = int(calc_plot_interval)

# # Scene 1
# scene1=display(title="Rocket Orientation", width=display_x/4.0, height=display_y/2.0, x=0, y=0)
# scene1.range=(1.2,1.2,1.2)
# scene1.forward = (0,-1,0)
# scene1.up=(0,0,1)
# scene1.select()
# rocket1 = rocket()
# XYZaxes1 = axes(ylen=0, xtext="west", ytext="")
# xyaxes1 = axes(xlen=0.5, ylen=0.5, zlen=0, xtext="x", ytext="y", ztext="")

# # # Scene 2
# # scene2=display(title="Rocket Orientation", width=display_x/4.0, height=display_y/2, x=0, y=display_y/2)
# # scene2.range=(1.5,1.5,1.5)
# # scene2.forward = (0,0,-1)
# # scene2.up=(0,-1,0)
# # scene2.select()
# # rocket2 = rocket(Tiptrail=True)
# # XYZaxes2 = axes(zlen=0, xtext="west", ytext="south", ztext="")

# # # Scene 3
# # scene3=display(title="Rocket Trajectory", width=display_x/4.0, height=display_y/(3.0/2.0),
# #                x=display_x/4.0, y=0)
# # scene3.center=(0,0,1)
# # scene3.range= maxrange
# # scene3.forward = (-1,-1,-0.5)
# # scene3.up=(0,0,1)
# # scene3.select()
# # rocket3 = curve(color=color.white)
# # XYZaxes3 = axes(xlen=maxscale, ylen=maxscale, zlen=maxscale, xtext="west", ytext="south")

# # # Scene 4
# # scene4=display(title="Rocket Trajectory", width=display_x/4, height=display_y/3.0,
# #                x=display_x/4.0, y=display_y/(3.0/2.0))
# # scene4.range= maxrange
# # scene4.forward = (0,0,-1)
# # scene4.up=(0,-1,0)
# # scene4.select()
# # rocket4 = curve(color=color.white)
# # XYXaxes4 = axes(xlen=maxscale, ylen=maxscale, zlen=0, xtext="west", ytext="south", ztext="")

# # Graph 1: 
# graph1=gdisplay(title='Rocket Frame x & y Axis Rotation Rate', width=display_x/4, height=display_y/3.0,
#                 xtitle='t', ytitle='deg/sec',x=display_x/2.0, y=0,xmin=0,xmax=t_max, ymin=-30, ymax=30)
# g1x = gcurve(color=color.red)
# g1y = gcurve(color=color.green)
# g1z = gcurve(color=color.blue)

# # # Graph 2: 
# # graph2=gdisplay(title='Ground Frame Rotation Angle', width=display_x/4, height=display_y/3.0,
# #                 xtitle='t', ytitle='deg',x=display_x/2.0, y=display_y/3.0,xmin=0,xmax=t_max, ymin=0, ymax=180)
# # g2 = gcurve(color=color.red)

# # # Graph 3: 
# # graph3=gdisplay(title='Rocket Spin Rate', width=display_x/4, height=display_y/3.0,
# #                 xtitle='t', ytitle='Rev/sec',x=display_x/2.0, y=display_y/(3.0/2.0),xmin=0,xmax=t_max, ymin=-5, ymax=5)
# # g3 = gcurve(color=color.red)

# # # Graph 4
# # graph4=gdisplay(title='Rocket Altitude', width=display_x/4, height=display_y/3.0,
# #                 xtitle='t', ytitle='ft',x=display_x/(4.0/3.0), y=0,xmin=0,xmax=t_max, ymin=0, ymax=10000)
# # g4 = gcurve(color=color.red)

# # # Graph 5
# # graph5=gdisplay(title='Rocket z-Axis Velocity', width=display_x/4, height=display_y/3.0,
# #                 xtitle='t', ytitle='ft/sec',x=display_x/(4.0/3.0), y=display_y/3.0,xmin=0,xmax=t_max, ymin=0, ymax=1000)
# # g5 = gcurve(color=color.red)

# # # Graph 6
# # graph6=gdisplay(title='Rocket z-Axis Acceleration', width=display_x/4, height=display_y/3.0,
# #                 xtitle='t', ytitle='gees',x=display_x/(4.0/3.0),y=display_y/(3.0/2.0),xmin=0,xmax=t_max, ymin=-5, ymax=15)
# # g6 = gcurve(color=color.red)


# # # Define Parameters
# # t = []
# # omega_xs = []
# # omega_ys = []
# # omega_zs = []
# # ax = []
# # ay = []
# # az = []
# # dX = []
# # dY = []
# # dZ = []
# # vz = []

# # # read the data file

# # if data_source == "DataLogger":
# #     line2 = Baro_file.readline()
# #     words2 = string.split(line2,",")
# #     dZ.append(float(words2[0]))
    
# #     line3 = gps_file.readline()
# #     words3 = string.split(line3,",")
# #     dX.append(-float(words3[0]))
# #     dY.append(-float(words3[1]))

# #     for line in DataLogger_file:
# #         words = string.split(line,",")

# #         t.append(float(words[0]))
# #         ax.append(float(words[1])*g)
# #         ay.append(float(words[2])*g)
# #         az.append(float(words[3])*g)
# #         omega_xs.append(float(words[4])*pi/180.0)
# #         omega_ys.append(float(words[5])*pi/180.0)
# #         omega_zs.append(float(words[6])*pi/180.0)
        
# #         if baro_read_counter >= baro_read_interval:
# #             line2 = Baro_file.readline()
# #             words2 = string.split(line2,",")
# #             dZ.append(float(words2[0]))
                
# #             baro_read_counter = 1
            
# #         else:
# #             dZ.append(float(words2[0]))
# #             baro_read_counter += 1

# #         if gps_read_counter >= gps_read_interval:
# #             line3 = gps_file.readline()
# #             words3 = string.split(line3,",")
# #             dX.append(-float(words3[0]))
# #             dY.append(-float(words3[1]))
# #             gps_read_counter = 1
            
# #         else:
# #             dX.append(-float(words3[0]))
# #             dY.append(-float(words3[1]))
# #             gps_read_counter += 1

        
# #     DataLogger_file.close()
# #     Baro_file.close()
# #     gps_file.close()

# # elif data_source == "SimResults":
# #     for line in SimResults_file:    
# #         words = string.split(line,",")

# #         t.append(float(words[0]))
# #         omega_xs.append(float(words[1]))
# #         omega_ys.append(float(words[2]))
# #         omega_zs.append(float(words[3]))
# #         ax.append(float(words[4]))
# #         ay.append(float(words[5]))
# #         az.append(float(words[6]))
# #         dX.append(float(words[7]))
# #         dY.append(float(words[8]))
# #         dZ.append(float(words[9]))
# #         vz.append(float(words[10]))

# #     SimResults_file.close()
    

# # if len(t) * delta_t > t_max:
# #     n = int(t_max/delta_t)
# # else:
# #     n = len(t)


# # phi = [0 for x in range(n)]
# # psi = [0 for x in range(n)]
# # theta = [0.0000001 for x in range(n)]
# # phi_s = [0 for x in range(n)]
# # psi_s = [0 for x in range(n)]
# # theta_s = [0.0000001 for x in range(n)]
# # alpha_zs = [0 for x in range(n)]
# # omega_xu = [0 for x in range(n)]
# # omega_yu = [0 for x in range(n)]
# # Theta_z = [0 for x in range(n)]
# # UxsX = [0 for x in range(n)]
# # UxsY = [0 for x in range(n)]
# # UxsZ = [0 for x in range(n)]
# # UysX = [0 for x in range(n)]
# # UysY = [0 for x in range(n)]
# # UysZ = [0 for x in range(n)]
# # UzsX = [0 for x in range(n)]
# # UzsY = [0 for x in range(n)]
# # UzsZ = [0 for x in range(n)]
# # UxX = [0 for x in range(n)]
# # UxY = [0 for x in range(n)]
# # UxZ = [0 for x in range(n)]
# # UyX = [0 for x in range(n)]
# # UyY = [0 for x in range(n)]
# # UyZ = [0 for x in range(n)]
# # UzX = [0 for x in range(n)]
# # UzY = [0 for x in range(n)]
# # UzZ = [0 for x in range(n)]


# # if data_source == "DataLogger":   
# # ##    dX = [0 for x in range(n)]
# # ##    dY = [0 for x in range(n)]
# #     vz = [0 for x in range(n)]

# # j = 1
# # plot_max = n
# # for i in range(1,n):

# #     omega_x_temp = omega_xs[i] * cos(beta) - omega_ys[i] * sin(beta)  # Rotate the DataLogger within the rocket about z to align the x-axis
# #     omega_y_temp = omega_xs[i] * sin(beta) + omega_ys[i] * cos(beta)  # with ease and the y-axis with south
# #     omega_xs[i] = omega_x_temp
# #     omega_ys[i] = omega_y_temp


# #     alpha_zs[i] = omega_zs[i] * delta_t + alpha_zs[i-1]   # de-spin the rocket to create the x-y axes
        
# #     omega_xu[i] = omega_xs[i] * cos(alpha_zs[i]) - omega_ys[i] * sin(alpha_zs[i])
# #     omega_yu[i] = omega_xs[i] * sin(alpha_zs[i]) + omega_ys[i] * cos(alpha_zs[i])
             
# #     phi[i] = euler_phi(psi[i-1],phi[i-1],theta[i-1],omega_xu[i],omega_yu[i],0,delta_t)
# #     psi[i] = euler_psi(psi[i-1],phi[i-1],theta[i-1],omega_xu[i],omega_yu[i],0,delta_t)
# #     theta[i] = euler_theta(psi[i-1],phi[i-1],theta[i-1],omega_xu[i],omega_yu[i],0,delta_t)
        
# #     phi_s[i] = euler_phi(psi_s[i-1],phi_s[i-1],theta_s[i-1],omega_xs[i],omega_ys[i],omega_zs[i],delta_t)
# #     psi_s[i] = euler_psi(psi_s[i-1],phi_s[i-1],theta_s[i-1],omega_xs[i],omega_ys[i],omega_zs[i],delta_t)
# #     theta_s[i] = euler_theta(psi_s[i-1],phi_s[i-1],theta_s[i-1],omega_xs[i],omega_ys[i],omega_zs[i],delta_t)

# #     UxsX[i] = eulerX(1,0,0,phi_s[i],psi_s[i],theta_s[i])
# #     UxsY[i] = eulerY(1,0,0,phi_s[i],psi_s[i],theta_s[i])
# #     UxsZ[i] = eulerZ(1,0,0,phi_s[i],psi_s[i],theta_s[i])
# #     UysX[i] = eulerX(0,1,0,phi_s[i],psi_s[i],theta_s[i])
# #     UysY[i] = eulerY(0,1,0,phi_s[i],psi_s[i],theta_s[i])
# #     UysZ[i] = eulerZ(0,1,0,phi_s[i],psi_s[i],theta_s[i])
# #     UzsX[i] = eulerX(0,0,1,phi_s[i],psi_s[i],theta_s[i])
# #     UzsY[i] = eulerY(0,0,1,phi_s[i],psi_s[i],theta_s[i])
# #     UzsZ[i] = eulerZ(0,0,1,phi_s[i],psi_s[i],theta_s[i])
    
# #     UxX[i] = eulerX(1,0,0,phi[i],psi[i],theta[i])
# #     UxY[i] = eulerY(1,0,0,phi[i],psi[i],theta[i])
# #     UxZ[i] = eulerZ(1,0,0,phi[i],psi[i],theta[i])
# #     UyX[i] = eulerX(0,1,0,phi[i],psi[i],theta[i])
# #     UyY[i] = eulerY(0,1,0,phi[i],psi[i],theta[i])
# #     UyZ[i] = eulerZ(0,1,0,phi[i],psi[i],theta[i])
# #     UzX[i] = eulerX(0,0,1,phi[i],psi[i],theta[i])
# #     UzY[i] = eulerY(0,0,1,phi[i],psi[i],theta[i])
# #     UzZ[i] = eulerZ(0,0,1,phi[i],psi[i],theta[i])


# #     Theta_z[i] = Theta(UzsX[i],UzsY[i],UzsZ[i])

# #     if data_source == "DataLogger":              # Calculate the parameters missing from the data files

# #         vz[i] = (az[i] - g)* delta_t + vz[i-1]

# #         if abs(az[i]) > acc_ejection:
# #             print az[i]/g
# #             if plot_max == n:
# #               plot_max = i

# ##        delta_Z = dZ[i] - dZ[i-1]
# ##        if abs(delta_Z) > delta_Z_max :      #set p at first ejection charge
# ##            if plot_max == n:
# ##                plot_ma x = i-2*baro_read_interval
# ##        delta_X = delta_Z * UzsX[i]/UzsZ[i]
# ##        delta_Y = delta_Z * UzsY[i]/UzsZ[i]
# ##        dX[i] = dX[i-1] + delta_X
# ##        dY[i] = dY[i-1] + delta_Y


# for i in range(plot_interval,n,plot_interval):
# # plot results - at this point, all parameters have been calculated regardless of the source file       
#     rate (plot_rate)

#     # Plot Rocket Orientation
#     rocket1.axis = (UzsX[i],UzsY[i],UzsZ[i])     # frame axis points in z direction
#     rocket1.up = (UxsX[i],UxsY[i],UxsZ[i])       # frame up points in x direction
#     xyaxes1.axis = (UzX[i],UzY[i],UzZ[i])
#     xyaxes1.up = (UxX[i],UxY[i],UxZ[i])

#     # Plot Rocket Frame Rotation Rate
#     g1x.plot(pos=(t[i],omega_xs[i]*180/pi))
#     g1y.plot(pos=(t[i],omega_ys[i]*180/pi))
            
# #     # Plot Ground Frame Rotation Angle
# #     g2.plot(pos=(t[i],Theta_z[i]*180/pi))

# #     # Plot spin rate
# #     g3.plot(pos=(t[i],omega_zs[i]/(2*pi)))

# #     # Plot Altitude
# #     g4.plot (pos=(t[i],dZ[i]))
 
# #     # Plot Velocity
# #     g5.plot (pos=(t[i],vz[i]))

# #     # Plot Acceleration
# #     g6.plot (pos=(t[i],az[i]/g))

# #     # Plot 3d Trajectory
# #     rocket3.append(vector(dX[i-plot_interval],dY[i-plot_interval],dZ[i-plot_interval]))

# #     # Plot Ground Projection Trajectory
# #     rocket4.append(vector(dX[i-plot_interval],dY[i-plot_interval],dZ[i-plot_interval]))

#     # Plot Orientation Sphere
#     if i < plot_max:                                 # stop the orientation plot at the first ejection charge
#         rocket2.axis = (UzsX[i],UzsY[i],UzsZ[i])     # frame axis points in z direction
#         rocket2.up = (UxsX[i],UxsY[i],UxsZ[i])       # frame up points in x direction

        
        
        

        
      


                    




# In[ ]:



