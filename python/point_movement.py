#!/usr/bin/python
###########################
#Author: liyao
#Python version: 2.7
#Dependency: matplotlib
###########################
import sys
import re
import matplotlib.pyplot as plt
import numpy as np
import datafileio as dio
import numana as na

if len(sys.argv) != 2:
    print("Usage: python" + sys.argv[0] + " [point log]")
    sys.exit()

tracks_x, tracks_y, obj_count, fps, nframes = dio.read_tracks(sys.argv[1])

print("Total " + str(nframes) + " track points for each track.")

#Calculate phase shift
#phshift, _, _ = na.phshift(tracks_y[0][:], tracks_y[5][:])
#print("phase shift of y between object 0 and 5: " + str(phshift))

#Time domain figure
time_domain_fig, (x_time_plot, y_time_plot) = plt.subplots(nrows = 2, ncols = 1)

for obj_idx in range(0, obj_count):
    x_time_plot.plot(tracks_x[obj_idx])
    y_time_plot.plot(tracks_y[obj_idx])

lengend_marker = []
for obj_idx in range(0, obj_count):
    lengend_marker.append("Tracking Point " + str(obj_idx))
    
x_time_plot.legend(lengend_marker, loc='upper right')
x_time_plot.set_title("X movement")
x_time_plot.set_xlabel("Frame number")
x_time_plot.set_ylabel("X coordinate")
x_time_plot.grid()

y_time_plot.legend(lengend_marker, loc='upper right')
y_time_plot.set_title("Y movement")
y_time_plot.set_xlabel("Frame number")
y_time_plot.set_ylabel("Y coordinate")
y_time_plot.grid()

time_domain_fig.suptitle("Tracking point movement", fontsize = 20);
time_domain_fig.show()

#######################################

#perform FFT transform
mag, phase, energy, freq = na.fft_scaled(tracks_y[5], fps)
#Eliminate DC
print("DC = %f" % (mag[0]))
mag[0] = 0
freq_domain_fig, (mag_plot, phase_plot)= plt.subplots(nrows = 2, ncols = 1)

mag_plot.plot(freq, mag)
mag_plot.grid()
phase_plot.plot(freq, phase)
phase_plot.grid()

freq_domain_fig.suptitle("Object Y Movement Freq Component")

freq_domain_fig.show()

raw_input("Press [Enter] to continue...")
