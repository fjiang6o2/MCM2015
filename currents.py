import numpy as np
from math import sqrt

def simulate(currents, ocean_scale, dist_x, dist_y, dist_z, time):
    #initialization
    floaters = []
    offset = -1*dist_x[0]
    for i in range(len(dist_x)):
        x_entry, y_entry, prob = dist_x[i]+offset, dist_y[i]-1, dist_z[i]
        floaters += [Floater(40, x_entry, y_entry, prob)]
    #updates - moving floaters according to corresponding force vectors
    for t in range(time):
        for floater_num in range(len(floaters)):
            floater = floaters[floater_num]
            plot_x = floater.x//ocean_scale
            plot_y = floater.y//ocean_scale
            if (plot_x >= len(currents)) or (plot_x < 0) or (plot_y >= len(currents[0])) or (plot_y < 0):
                floater.floater_gone() #floater floated out of search space
            else:
                floater.mom_update(currents[plot_x, plot_y])
                floater.pos_update()
                floaters[floater_num] = floater
    #format output
    output_distribution = np.zeros((sqrt(len(dist_x)), sqrt(len(dist_y))))
    for floater in floaters:
        x_coord, y_coord = floater.x, floater.y
        if not ((x_coord >= len(output_distribution)) or (y_coord >= len(output_distribution[0])) or (x_coord < 0) or (y_coord < 0)) :
            output_distribution[x_coord, y_coord] += floater.prob
    return output_distribution

class Floater():
    def __init__(self, m, x, y, prob, name = "floater"):
        self.name = name
        self.x = x
        self.y = y
        self.m = m #mass
        self.prob = prob
        self.mom = [0, 0]
    def mom_update(self, velocity): #updates both designed around being called every once every second
        f = force(self.m, velocity) #momentum = force * time
        self.mom[0] += f[0]
        self.mom[1] += f[1]
    def pos_update(self):
        velocity = [self.mom[0]/self.m, self.mom[1]/self.m]
        self.x, self.y = self.x+velocity[0], self.y+velocity[1] #distance = velocity * time
    def floater_gone(self):
        self.prob = 0

def force(m, velocity, drag_co = .47, cross_area = .5): #calculate drag force vector from velocity vector and dummy values
    v_magnitude = sqrt(pow(velocity[0], 2) + pow(velocity[1], 2))
    magnitude = .5 * 1025 * pow(v_magnitude, 2) * drag_co *cross_area
    v_unit_vec = [velocity[0]/v_magnitude, velocity[1]/v_magnitude]
    return [v_unit_vec[0] * magnitude, v_unit_vec[1] * magnitude]

def smoosh(): #overlap
    return np.array([[[-1,0],[-1,0]], [[1,0],[1,0]]])

def example_current1(): #split in half
    return np.array([[[-1, 0],[-1, 0]], [[1, 0], [1, 0]]])

def example_current2(): #split in fourths and push out wards
    return np.array([[[-1, -1], [-1, 1]], [[1, -1], [1, 1]]])

def example_current3(): #merge with currents pushing from corners to center.
    return np.array([[[1, 1], [1, -1]], [[-1, 1], [-1, -1]]])
