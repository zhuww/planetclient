#!/homes/janeway/zhuww/bin/py
import numpy
import pyfits
from pylab import *
#from Pgplot import *
#from ppgplot import *
#import ppgplot
from numpy import *



class Cursor:
    badtimestart=[]
    badtimeend=[]
    lines = []
    def __init__(self, ax):
        self.ax = ax
        #self.lx = ax.axhline(color='k')  # the horiz line
        self.ly = ax.axvline(color='k')  # the vert line

        # text location in axes coords
        #self.txt = ax.text( 0.7, 0.9, '', transform=ax.transAxes)
        self.Flag = True

    def mouse_move(self, event):
        if not event.inaxes: return

        x, y = event.xdata, event.ydata
        # update the line positions
        #self.lx.set_ydata(y )
        self.ly.set_xdata(x )

        #self.txt.set_text( 'x=%1.2f, y=%1.2f'%(x,y) )
        draw()

    def click(self, event):
        print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(
            event.button, event.x, event.y, event.xdata, event.ydata)
        self.xdata = event.xdata
        self.ydata = event.ydata
        if '%d' % (event.button) == '1':
            if self.Flag:
                self.badtimestart.append(self.xdata)
                self.Flag = False
                self.lines.append(self.ax.axvline(color='r'))
                self.lines[-1].set_xdata(event.xdata)
            else:
                self.badtimeend.append(self.xdata)
                self.lines.append(self.ax.axvline(color='k'))
                self.lines[-1].set_xdata(event.xdata)
                self.Flag = True
        elif '%d' % (event.button) == '3':
            if self.Flag:
                #self.ax.axvline(color='w').set_xdata(self.badtimeend[-1])
                self.lines[-1].remove()
                self.lines = self.lines[:-1]
                self.badtimeend = self.badtimeend[:-1]
                self.Flag = False
                #self.ax.lines.pop(0)
            else:
                #self.ax.axvline(color='w').set_xdata(self.badtimestart[-1])
                self.lines[-1].remove()
                self.lines = self.lines[:-1]
                self.badtimestart = self.badtimestart[:-1]
                self.Flag = True
                #self.ax.lines.pop(0)
        else:
            print 'event.button: %d' % (event.button)
        draw()
        
    def endedit(self, event):
        print 'Quit editing bad time intervals.'
        #disconnect('button_press_event', cursor.click)


class SnaptoCursor:
    """
    Like Cursor but the crosshair snaps to the nearest x,y point
    For simplicity, I'm assuming x is sorted
    """
    def __init__(self, ax, x, y):
        self.ax = ax
        self.lx = ax.axhline(color='k')  # the horiz line
        self.ly = ax.axvline(color='k')  # the vert line
        self.x = x
        self.y = y
        # text location in axes coords
        #self.txt = ax.text( 0.7, 0.9, '', transform=ax.transAxes)

    def mouse_move(self, event):

        if not event.inaxes: return

        x, y = event.xdata, event.ydata

        indx = searchsorted(self.x, [x])[0]
        x = self.x[indx]
        y = self.y[indx]
        # update the line positions
        self.lx.set_ydata(y )
        self.ly.set_xdata(x )

        #self.txt.set_text( 'x=%1.2f, y=%1.2f'%(x,y) )
        #print 'x=%1.2f, y=%1.2f'%(x,y)
        draw()



hdulist=pyfits.open('histo.fits')
tabdata=hdulist[1].data
cols=hdulist[1].columns
#names=cols.names
#print names
counts=array(tabdata.field('COUNTS'))
time=array(tabdata.field('TIME'))
#starttime=time[0]
#time=time#-starttime
#plotxy(counts,time)
ax = subplot(111)
ax.plot(time, counts)
cursor = Cursor(ax)
#cursor = SnaptoCursor(ax, t, s)
connect('motion_notify_event', cursor.mouse_move)
connect('button_press_event', cursor.click)
duration = max(time) - min(time)
ax.set_xlim((min(time)-0.1*duration, max(time)+0.1*duration))
show()
#while not ppgplot.pgband(0)[2]=="X":
    #print "click on the daigram twice to define a bad time interval:"
    #badtimestart.append(ppgplot.pgband(6)[0])
    #badtimeend.append(ppgplot.pgband(6)[0])
#closeplot()
badtimestart=numpy.array(cursor.badtimestart)#+starttime
badtimeend=numpy.array(cursor.badtimeend)#+starttime
print badtimestart
print badtimeend
#plot(time,counts)
#print tabdata[0]

#check gti
hdulist=pyfits.open('gti.fits')
tabdata=hdulist[1].data
#cols=hdulist[1].columns
start=tabdata.field('START')
stop=tabdata.field('STOP')
print len(start),len(stop)
for j in range(len(badtimestart)):
    badlist=[]
    if badtimestart[j] >= badtimeend[j]:
        print "invalid bad time interval: abandon."
    else:
        print len(start),len(stop)
        for i in range(len(start)):
            if start[i] < badtimestart[j]:
                if stop[i] <= badtimestart[j]:
                    continue
                else:
                    if stop[i] <= badtimeend[j]:
                        stop[i]=badtimestart[j]
                    else:
                        start=insert(start,i+1,badtimeend[j])
                        stop=insert(stop,i+1,stop[i])
                        stop[i]=badtimestart[j]
                        break
            else:
                if start[i] < badtimeend[j]:
                    if stop[i] <= badtimeend[j]:
                        badlist.append(i)
                    else:
                        start[i]=badtimeend[j]
                else:
                    break
        start=delete(start,badlist)
        stop=delete(stop,badlist)
errbar=0.5*(stop-start)
center=array(start+errbar)#-starttime
#array=0.*start+10.
array=array(0.*start+max(counts)/2)
#plotxy(array,center,symbol=1,line=None,errx=errbar,setup=0)
#closeplot()
print sum(stop-start)
col1=pyfits.Column(name="START",format = 'D',unit = 's',array=start)
col2=pyfits.Column(name="STOP",format = 'D',unit = 's',array=stop)
cols=pyfits.ColDefs([col1,col2])
tbhdu=pyfits.new_table(cols)
hdulist.append(tbhdu)
hdulist[2].header=hdulist[1].header
#print hdulist[2].header['ONTIME'],hdulist[2].header['TSTART'],hdulist[2].header['TSTOP']
hdulist[2].header['ONTIME']=sum(stop-start)
hdulist[2].header['TSTART']=start[0]
hdulist[2].header['TSTOP']=stop[len(stop)-1]
#print hdulist[2].header['ONTIME'],hdulist[2].header['TSTART'],hdulist[2].header['TSTOP']
hdulist.remove(hdulist[1])
hdulist.writeto('newgti.fits')
hdulist.close()

#plotxy(counts,time,device="gti.ps/PS")
#plotxy(array,center,symbol=1,line=None,errx=errbar,setup=0)
#closeplot()
plot(time, counts)
errorbar(center, array, xerr=errbar)
show()
