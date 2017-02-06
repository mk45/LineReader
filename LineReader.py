#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###################################################
# by Maciej Kamiński Politechnika Wrocławska
# Under GPL 3 and  MIT licence
#
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import argparse
import sys
#import pdb
import numpy as np


parser=argparse.ArgumentParser(description="Helps determine point coordinates in scanned chart")
parser.add_argument('-xfs','--x_figure_size', type=int, help='Window width in inches',default=12)
parser.add_argument('-yfs','--y_figure_size', type=int, help='Window height in inches',default=9)
parser.add_argument('maxx', type=int, help='Max X point - (0,X) coordinated')
parser.add_argument('maxy', type=int, help='Max Y point - (Y,0) coordinated')
parser.add_argument('input', type=str, help='Input image filename')
parser.add_argument('output', type=str, help='Output CSV filename')

args=parser.parse_args()


def onkey(event):
    print(dir(event))

    if event.key!=' ':
        return
    global point_zero
    global point_xmax
    global point_ymax
    global points

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
        with open(args.output,"a") as file:
            zero=complex(*point_zero)
            xmax=complex(*point_xmax)
            ymax=complex(*point_ymax)
            point=complex(*points[-1])
            x=xmax-zero
            y=ymax-zero
            p=point-zero
            xversor=x/args.maxx
            yversor=y/args.maxy
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

def zoom_fun(event):
    # get the current x and y limits
    base_scale=2
    ax=event.canvas.axis

    cur_xlim = ax.get_xlim()
    cur_ylim = ax.get_ylim()
    cur_xrange = (cur_xlim[1] - cur_xlim[0])*.5
    cur_yrange = (cur_ylim[1] - cur_ylim[0])*.5
    xdata = event.xdata # get event x location
    ydata = event.ydata # get event y location
    if event.button == 'up':
        # deal with zoom in
        scale_factor = 1/base_scale
    elif event.button == 'down':
        # deal with zoom out
        scale_factor = base_scale
    else:
        # deal with something that should never happen
        scale_factor = 1
        print event.button
    # set new limits
    ax.set_xlim([xdata - cur_xrange*scale_factor,
                 xdata + cur_xrange*scale_factor])
    ax.set_ylim([ydata - cur_yrange*scale_factor,
                 ydata + cur_yrange*scale_factor])
    plt.draw() # force re-draw

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
    image=mpimg.imread(args.input)
    fig, ax = plt.subplots(figsize=(args.x_figure_size,args.y_figure_size))
    fig.suptitle("Select zero point", fontsize=14, fontweight='bold')
    fig.canvas.mpl_connect('key_press_event', onkey)
    fig.canvas.mpl_connect('scroll_event',zoom_fun)
    plt.imshow(image,zorder=0,extent=[0.0,1.0,0.0,1.0],aspect='auto')
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    plt.tight_layout(pad=0)
    plt.show()

main()
