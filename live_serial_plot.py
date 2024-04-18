#!/usr/bin/env python3

"""
Simple live plot reading serial data
Graph is not exact as it can be altered by delays in serial communication and plot time, but it is useful nonetheless

Usage example: ./live_serial_plot.py --tty /dev/ttyUSB0 --plot var1 --plot var2 --plot_n vars3 2 --save ./log.csv

Data on the serial line for the above command:    [note: space after prefix is optional]
var1 1.4427
var2 42
vars3 1 2 3 4 5

The last received data is used if no data was updated when the plot is redrawn.
"""

import argparse
import csv
import functools
import time

import serial

import matplotlib.pyplot as plt
import matplotlib.animation as animation

parser = argparse.ArgumentParser()
parser.add_argument("--tty", "-t", required=True)
parser.add_argument("--baudrate", "-b", default=115200)
parser.add_argument("--plot", "-p", nargs=1, default=[], action='append')
parser.add_argument("--plot_n", "-pn", nargs=2, action='append', dest='plot')
parser.add_argument("--save", "-s", default=None)
parser.add_argument("--no-show-all", "-nsa", action='store_false', default=True, dest='show_all')
parser.add_argument("--ymin", "-y", type=int, default=0)
parser.add_argument("--ymax", "-Y", type=int, default=100)
parser.add_argument("--ms", "-ms", type=int, default=30)
parser.add_argument("--buffer", "-buf", type=int, default=200)
parser.add_argument("--no-blit", "-nb", action='store_false', default=True, dest='blit')
args = parser.parse_args()

last_value = [0] * len(args.plot)
datapoints = [[], *([] for _ in args.plot)]
plots = []
negt = [ms/1000 for ms in range(-args.buffer*args.ms, 0, args.ms)]
t0 = time.time()

def decode_line(line): # str -> list[tuple(id:int, value:float)]
    lst = []
    for i, t in enumerate(args.plot):
        if line.startswith(t[0]):
            sp = line[len(t[0]):].split()
            n = int(t[1]) if len(t) > 1 else 0
            try:
                lst.append((i, float(sp[n])))
            except:
                pass
    return lst

def animate(frame_nr, s):
    while line := ser.readline().decode():
        for i, v in decode_line(line):
            last_value[i] = v
    datapoints[0].append(time.time() - t0)
    for i, data in enumerate(datapoints[1:]):
        data.append(last_value[i])
        plots[i].set_data(negt[-min(len(data), args.buffer):], data[-args.buffer:])
    return plots

fig, ax = plt.subplots()
for _ in args.plot:
    plots.append(ax.plot([])[0])
ax.set_xlim([-args.buffer*args.ms/1000,0])
ax.set_ylim([args.ymin, args.ymax])
with serial.Serial(args.tty, args.baudrate, timeout=0.001) as ser:
    afunc = functools.partial(animate, s=ser)
    ani = animation.FuncAnimation(fig, afunc, interval=args.ms, blit=args.blit, cache_frame_data=False)
    plt.show()

if args.show_all:
    fig, ax = plt.subplots()
    for data in datapoints[1:]:
        ax.plot(datapoints[0], data)
    ax.set_ylim([args.ymin, args.ymax])
    plt.show()

if args.save:
    with open(args.save, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['t', *(' '.join(p) for p in args.plot)])
        writer.writerows(zip(*datapoints))