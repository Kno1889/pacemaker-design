import matplotlib
import matplotlib.animation as animation
from matplotlib.figure import Figure
from matplotlib import style
style.use('ggplot')
matplotlib.use("TkAgg")

import pages
import controller
import settings

import com

comms = com.Com(settings.COMPORT)

NUM_POINTS = 40




class Data():

    def __init__(self, SIZE):
        self.data = [0]*SIZE

    def add(self, val):
        self.data.pop(0)
        self.data.append(val)

    def get_data(self):
        return self.data


atrial = Data(NUM_POINTS)
ventrical = Data(NUM_POINTS)
time = Data(NUM_POINTS)
time_interval = 0.0

def animate(i):
    if settings.PD_Flag == True:
        data = comms.getEgramValues()
        time_interval = time_interval + 0.2 

        a_val = data[0]
        v_val = data[1]
        r_val = data[2] ## implemenent me later

        atrial.add(a_val)
        ventrical.add(v_val)
        time.add(time_interval)
        
        a.clear()
        
        a.plot(time.get_data(), atrial.get_data())
        a.plot(time.get_data(), ventrical.get_data())

        print(data)

        # check number of points to add to 40
        # scrap extra points at the end to make space for new points 
        # time interval = 0.2
        a.plot(data)

f = Figure(figsize=(5,5), dpi=100)
a = f.add_subplot(111)

