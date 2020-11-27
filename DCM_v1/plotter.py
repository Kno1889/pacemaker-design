import matplotlib
import matplotlib.animation as animation
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')
matplotlib.use("TkAgg")

import pages
import controller
import settings

import math
import com

comms = com.Com(settings.COMPORT)
time_interval = 0.0
NUM_POINTS = 40

class Data():

    def __init__(self, SIZE):
        self.data = [0.5]*SIZE

    def add(self, val):
        self.data.pop(0)
        self.data.append(val)

    def get_data(self):
        return self.data

atrial = Data(NUM_POINTS)
ventrical = Data(NUM_POINTS)
time = Data(NUM_POINTS)


def animate(i):
    if settings.PD_Flag == True:
        global time_interval
        data = comms.getEgramValues()
        time_interval += 0.04 

        a_val = round(data[0],3)
        v_val = round(data[1],3)
        r_val = data[2] ## implemenent me later

        atrial.add(a_val)
        ventrical.add(v_val)
        time.add(time_interval)
        
        a.clear()
        #have min scale
        a.plot(time.get_data(), atrial.get_data(), label = "atrial")
        a.plot(time.get_data(), ventrical.get_data(), label = "ventrical")
        legend = a.legend(loc='upper right')

f = Figure(figsize=(5,5), dpi=100)
a = f.add_subplot(111)
axes = plt.axes()
print(axes)
axes.set_ylim([0, 1])