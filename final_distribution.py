from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm, chi2
from scipy import pi,sqrt,exp
from scipy.special import erf
from currents import *

fig = plt.figure(1) #input
ax1 = fig.add_subplot(111, projection='3d')

x_input, y_input = [], []
size = 10
for i in range(-size+1, size):
    x_input += [i for _ in range(-size+1, size)]
    y_input += [j for j in range(1,size*2)]
x_input, y_input = np.array(x_input), np.array(y_input)
num_elements = len(x_input)
zpos = np.zeros(num_elements)
dx, dy = np.ones(num_elements), np.ones(num_elements)
norm1 = chi2.pdf((x_input**2 + y_input**2)**.5/10, 4) #toy PDFs for example purposes
norm2 = norm.pdf(np.arctan2(y_input, x_input), pi/2, pi/6)
dz = norm1*norm2
norm = np.linalg.norm(dz)
dz = dz/norm

ax1.bar3d(x_input, y_input, zpos, dx, dy, dz, color='#00ceaa')
fig.show()

#currents = example_current1()
#currents = example_current2()
currents = example_current3()
#currents = smoosh()
ocean_scale = 10
out = simulate(currents, ocean_scale, x_input, y_input, dz, 1)
out = out.reshape(len(x_input))
dz = out/np.linalg.norm(out)

fig1 = plt.figure(2)
ax2 = fig1.add_subplot(111, projection='3d')

xpos, ypos = [], []
for i in range(-size+1, size):
    xpos += [i for _ in range(-size+1, size)]
    ypos += [j for j in range(1,size*2)]

xpos = np.array(xpos)
ypos = np.array(ypos)
num_elements = len(xpos)
zpos = np.zeros(num_elements)
dx = np.ones(num_elements)
dy = np.ones(num_elements)

ax2.bar3d(xpos, ypos, zpos, dx, dy, dz, color='#00ceaa')
fig1.show()

raw_input()

