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

def animate(i):
    if settings.PD_Flag == True:
        data = comms.getEgramValues()
        a.clear()
        print(data)
        a.plot(data)

f = Figure(figsize=(5,5), dpi=100)
a = f.add_subplot(111)


