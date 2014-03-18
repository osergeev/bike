import matplotlib.pyplot as plt
import numpy

# enable animation mode
plt.ion()
#fig, ax = figure.subplots()


xw1=1.5
yw1=1.5
xw2=3
yw2=1.5
xp1=1.7
yp1=2.5
xp2=2.7
yp2=2.5

# connecting points
#w1 = [xw1,yw1]
#w2 = [xw2,yw2]
#p1 = [xp1,yp1]
#p2 = [xp2,yp2]
figure = plt.figure()
axes = figure.add_subplot('111',aspect='equal')

axes.set_xlim(0,20)
axes.set_ylim(0,20)

spr1,=axes.plot([xw1,xw2,xp1,xp2,xw2], [yw1,yw2,yp1,yp2,yw2],'-')
spr2,=axes.plot([xp2,xw1,xp1], [yp2,yw1,yp1],'-')

#spr2, = plt.plot(w1,p1,'go-')
#plt.plot(p1,p2,'go-')
#plt.plot(w1,p2,'go-')
#plt.plot(p1,w2,'go-')
#plt.plot(p2,w2,'go-')

# define the figure hierarchy (figure holds axes)




# add a patch to the axis
wheel1 = plt.Circle((0,0), radius=0.4)
axes.add_patch(wheel1)
wheel1.center = (xw1,yw1)
wheel2 = plt.Circle((0,0), radius=0.4)
wheel2.center = (xw2,yw2)
axes.add_patch(wheel2)
point1 = plt.Circle((0,0), radius=0.2)
point1.center = (xp1,yp1)
axes.add_patch(point1)
point2 = plt.Circle((0,0), radius=0.2)
point2.center = (xp2,yp2)
axes.add_patch(point2)



# shift the wheels position
for i in range(0, 300, 1):
   i=i*0.05
   wheel1.center = (xw1+i,yw1)
   wheel2.center = (xw2+i,yw2)
   point1.center = (xp1+i,yp1)
   point2.center = (xp2+i,yp2)
   spr1.set_xdata([xw1+i,xw2+i,xp1+i,xp2+i,xw2+i])
   spr2.set_xdata([xp2+i,xw1+i,xp1+i])
   
   #spr1=axes.plot([xw1+i,xw2+i,xp1+i,xp2+i,xw2+i], [yw1,yw2,yp1,yp2,yw2],'-')
   #spr2=axes.plot([xp2+i,xw1+i,xp1+i], [yp2,yw1,yp1],'-')
   #spr1.set_ydata(axes.plot([xw1+i,xw2+i,xp1,xp2+i,xw2+i], [yw1,yw2,yp1,yp2,yw2]))
   #spr2.set_ydata(axes.plot([xp2+i,xw1+i,xp1+i], [yp2,yw1,yp1]))
   
   #figure.canvas.draw()
   plt.draw()

# afterwards, switch to zoomable GUI mode

plt.ioff()
plt.show()

