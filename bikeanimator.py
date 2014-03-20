import matplotlib.pyplot as mpl
from surface import Surface
import numpy as np
import zoom

   # enable animation mode
   # enable animation mode
   #fig, ax = figure.subplots()

def bikeanim(xw1,yw1,xw2,yw2,xp1,yp1,xp2,yp2,r1,r2,i):
    mpl.ion()
    surface1 = Surface(100,100)
    surfacepoints = surface1.getPoints()

#xw1=1.5
#yw1=1.5
#xw2=3
#yw2=1.5
#xp1=1.7
#yp1=2.5
#xp2=2.7
#yp2=2.5
# connecting points
#w1 = [xw1,yw1]
#w2 = [xw2,yw2]
#p1 = [xp1,yp1]
#p2 = [xp2,yp2]

    figure = mpl.figure()
    axes = figure.add_subplot('111',aspect='equal')

#axes.set_xlim(0,100)
    axes.set_ylim(-5,10)
    time_text = axes.text(0.02, 0.95, '', transform=axes.transAxes)
    dist_text = axes.text(0.02, 0.90, '', transform=axes.transAxes)
    spr1,=axes.plot([xw1,xw2,xp1,xp2,xw2], [yw1,yw2,yp1,yp2,yw2],'-')
    spr2,=axes.plot([xp2,xw1,xp1], [yp2,yw1,yp1],'-')
    wheel1 = mpl.Circle((0,0), radius=r1)
    axes.add_patch(wheel1)
    wheel1.center = (xw1,yw1)
    wheel2 = mpl.Circle((0,0), radius=r2)
    wheel2.center = (xw2,yw2)
    axes.add_patch(wheel2)
    point1 = mpl.Circle((0,0), radius=0.2)
    point1.center = (xp1,yp1)
    axes.add_patch(point1)
    point2 = mpl.Circle((0,0), radius=0.2)
    point2.center = (xp2,yp2)
    axes.add_patch(point2)
    xs, ys = zip(*surfacepoints)
#print xs, ys
    mpl.plot(xs,ys)
    
    for i in range(0,800):
# shift the wheels position
        i=i*0.05
        inew=i/0.05
        wheel1.center = (xw1+i,yw1)
        wheel2.center = (xw2+i,yw2)
        point1.center = (xp1+i,yp1)
        point2.center = (xp2+i,yp2)
        spr1.set_xdata([xw1+i,xw2+i,xp1+i,xp2+i,xw2+i])
        spr2.set_xdata([xp2+i,xw1+i,xp1+i])
        time_text.set_text('time = %.1f' % inew)
        dist_text.set_text('distance = %.3f' % i)
        axes.set_xlim(i-1,i+8)
        mpl.draw()
   
   #spr1=axes.plot([xw1+i,xw2+i,xp1+i,xp2+i,xw2+i], [yw1,yw2,yp1,yp2,yw2],'-')
   #spr2=axes.plot([xp2+i,xw1+i,xp1+i], [yp2,yw1,yp1],'-')
   #spr1.set_ydata(axes.plot([xw1+i,xw+i,xp1,xp2+i,xw2+i], [yw1,yw2,yp1,yp2,yw2]))
   #spr2.set_ydata(axes.plot([xp2+i,xw1+i,xp1+i], [yp2,yw1,yp1]))
   #figure.canvas.draw()   
   # afterwards, switch to zoomable GUI mode

    mpl.ioff()
    mpl.show()
