#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

###################################################
# by Maciej Kamiński Politechnika Wrocławska
# Under GPL 3 and  MIT licence
#

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import argparse
import sys
#import pdb
import numpy as np


maxx=float(sys.argv[1])
maxy=float(sys.argv[2])
xfs=float(sys.argv[3])
yfs=float(sys.argv[4])
filename=str(sys.argv[5])
output=str(sys.argv[6])

def onkey(event):
    if event.key!=' ':
        return
    global point_zero
    global point_xmax
    global point_ymax
    global points
    #p='button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(event.button, event.x, event.y, event.xdata, event.ydata)
    #print(dir(event.canvas.figure))#.suptitle(p, fontsize=14, fontweight='bold')
    if not point_zero:
        event.canvas.figure.suptitle("Select X max Point", fontsize=14, fontweight='bold')
        point_zero=(event.xdata, event.ydata)
        event.canvas.draw()
        print(point_zero)
    elif not point_xmax:
        event.canvas.figure.suptitle("Select Y max Point", fontsize=14, fontweight='bold')
        point_xmax=(event.xdata, event.ydata)
        event.canvas.draw()
        print(point_xmax)
    elif not point_ymax:
        event.canvas.figure.suptitle("Select First Point", fontsize=14, fontweight='bold')
        point_ymax=(event.xdata, event.ydata)
        event.canvas.draw()
        print(point_ymax)
    else:
        event.canvas.figure.suptitle("Select Next Point", fontsize=14, fontweight='bold')
        points.append((event.xdata, event.ydata))
        event.canvas.draw()
        with open(output,"a") as file:
            zero=complex(*point_zero)
            xmax=complex(*point_xmax)
            ymax=complex(*point_ymax)
            point=complex(*points[-1])
            x=xmax-zero
            y=ymax-zero
            p=point-zero
            xversor=x/maxx
            yversor=y/maxy
            a=np.array([
                [xversor.real,yversor.real],
                [xversor.imag,yversor.imag]
            ])
            b=np.array([p.real,p.imag])
            #np.transpose(a)
            h=np.linalg.solve(a,b)
            print(h)
            print("{:.2f},{:.2f}".format(round(h[0],2),round(h[1],2)),file=file)
            #print("",file=file)


#pdb.set_trace()
def main():
    global point_zero
    global point_xmax
    global point_ymax
    global points

    point_zero=None
    point_xmax=None
    point_ymax=None
    points=[]

    try:
        image=mpimg.imread(filename)
    except:
        image=[[[1.0,1.0,1.0]]]

    #x=[(t-0.0)/10.0 for t in range(steps*10)]

    fig, ax = plt.subplots(figsize=(12,8))

    #f=lambda s: convolution_mix(s,selectivity,conv_a,conv_b,alpha)

    #plt.plot([0],[0],zorder=1)
    fig.suptitle("Select zero point", fontsize=14, fontweight='bold')

    cid = fig.canvas.mpl_connect('key_press_event', onkey)

    plt.imshow(image,zorder=0,extent=[0.0,1.0,0.0,1.0],aspect='auto')

    #fig=plt.figure(figsize=(10,10))
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    plt.tight_layout(pad=0)
    plt.show()

main()
