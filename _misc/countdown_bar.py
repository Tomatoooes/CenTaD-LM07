# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 18:18:24 2022

@author: CIL-SCSE
"""

import time
# import sys
from psychopy import visual, core
 
win = visual.Window([1000,800], color="black", fullscr=False,allowGUI=False, winType='pyglet',monitor="testMonitor", units="pix") #open a window

lEndPoint = -(win.size[0]/2)
rEndPoint = (win.size[0]/2)

line = visual.ShapeStim(win, vertices=[(lEndPoint, 0), (rEndPoint, 0)],lineColor = "blue", lineWidth = 30)

# time = 10

dist = win.size[0]/(60.5*time)

timer = core.CountdownTimer(time)
while timer.getTime() > 0:
    rEndPoint -= dist
    line.vertices = [(lEndPoint,0),(rEndPoint,0)]
    line.draw()
    win.flip()

win.close()
core.quit()
