import numpy
from pylab import *


class label:
    results = ()
    folding_results = ()
    period = 0.
    @classmethod
    def labeling(self, event):
        """
        do labeling by pressing a key, 
        "g" --> good
        "b" --> bad
        "c" --> correct, by deleting the last saved result so you may correct your labeling should you pressed the wrong key.
        """
        #print ('you pressed', event.key, event.xdata, event.ydata)
        if event.key in ["g", "b", "h"]:
            self.results.append(self.folding_results[-1] + [event.key])
            print "you labeled candidate period %s as %s" % (self.period, event.key)
        elif event.key == 'c':
            self.results = self.results[:-1]
            print "you cancelled candidate period %s's label %s" % (self.period, event.key)
        else:
            pass

class Cursor:
    """
    A cursor class for linking the mouse event like this:
    connect('motion_notify_event', cursor.mouse_move)
    connect('button_press_event', cursor.click)
    """
    start=0
    end=-1
    lines = []
    def __init__(self, ax, x, y):
        self.ax = ax
        #self.lx = ax.axhline(color='k')  # the horiz line
        self.ly = ax.axvline(color='k')  # the vert line

        # text location in axes coords
        #self.txt = ax.text( 0.7, 0.9, '', transform=ax.transAxes)
        self.Flag = True
        self.x = x
        self.y = y
        self.redline = []
        self.blueline = []

    def mouse_move(self, event):
        if not event.inaxes: return

        x, y = event.xdata, event.ydata
        # update the line positions
        #self.lx.set_ydata(y )
        self.ly.set_xdata(x )

        #self.txt.set_text( 'x=%1.2f, y=%1.2f'%(x,y) )
        draw()

    def click(self, event):
        #print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(
            #event.button, event.x, event.y, event.xdata, event.ydata)
        self.xdata = event.xdata
        self.ydata = event.ydata
        if '%d' % (event.button) == '1':
            if self.xdata <= min(self.x) or self.xdata >= max(self.x):
                pass
            elif self.Flag:
                indx = len(self.x[self.x>self.xdata])-1
                self.start = indx
                self.Flag = False
                #while not len(self.redline) == 0:
                    #self.redline[-1].remove()
                self.redline.append(self.ax.axvline(color='r'))
                self.lines.append(self.redline[-1])
                
                self.lines[-1].set_xdata(event.xdata)
            else:
                indx = len(self.x[self.x>self.xdata])-1
                self.end = indx
                #while not len(self.blueline) == 0:
                    #self.blueline[-1].remove()
                self.blueline.append(self.ax.axvline(color='k'))
                self.lines.append(self.blueline[-1])
                self.lines[-1].set_xdata(event.xdata)
                self.Flag = True
        elif '%d' % (event.button) == '3':
            if self.Flag:
                #self.ax.axvline(color='w').set_xdata(self.end[-1])
                try:
                    self.lines[-1].remove()
                    self.lines = self.lines[:-1]
                    self.end = -1
                    self.Flag = not self.Flag
                except:
                    print "no more lines to delete"
                    pass
                    self.Flag = True
                #self.ax.lines.pop(0)
            else:
                #self.ax.axvline(color='w').set_xdata(self.start[-1])
                try:
                    self.lines[-1].remove()
                    self.lines = self.lines[:-1]
                    self.start = 0
                    self.Flag = not self.Flag
                except:
                    print "no more lines to delete"
                    pass
                    self.Flag = True
                #self.ax.lines.pop(0)
        else:
            #print 'event.button: %d' % (event.button)
            self.func()
        draw()
        
    def link_exe(self, func):
        self.func = func
    #def endedit(self, event):
        #print 'Quit editing bad time intervals.'
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

    def click(self, event):
        #print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(
            #event.button, event.x, event.y, event.xdata, event.ydata)
        self.xdata = event.xdata
        self.ydata = event.ydata
        if '%d' % (event.button) == '1':
            if self.Flag:
                self.start.append(self.xdata)
                self.Flag = False
                self.lines.append(self.ax.axvline(color='r'))
                self.lines[-1].set_xdata(event.xdata)
            else:
                self.end.append(self.xdata)
                self.lines.append(self.ax.axvline(color='k'))
                self.lines[-1].set_xdata(event.xdata)
                self.Flag = True
        elif '%d' % (event.button) == '3':
            if self.Flag:
                #self.ax.axvline(color='w').set_xdata(self.end[-1])
                try:
                    self.lines[-1].remove()
                    self.lines = self.lines[:-1]
                    self.end = self.end[:-1]
                except:pass
                finally:
                    self.Flag = False
                #self.ax.lines.pop(0)
            else:
                #self.ax.axvline(color='w').set_xdata(self.start[-1])
                try:
                    self.lines[-1].remove()
                    self.lines = self.lines[:-1]
                    self.start = self.start[:-1]
                except:pass
                finally:
                    self.Flag = True
                #self.ax.lines.pop(0)
        else:
            pass
            #print 'event.button: %d' % (event.button)
        draw()



#hdulist=pyfits.open('histo.fits')
#tabdata=hdulist[1].data
#cols=hdulist[1].columns
#counts=array(tabdata.field('COUNTS'))
#time=array(tabdata.field('TIME'))
#ax = subplot(111)
#ax.plot(time, counts)
#cursor = Cursor(ax)
#connect('motion_notify_event', cursor.mouse_move)
#connect('button_press_event', cursor.click)
#duration = max(time) - min(time)
#ax.set_xlim((min(time)-0.1*duration, max(time)+0.1*duration))
#show()
