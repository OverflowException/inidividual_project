import sys
import re
import matplotlib.pyplot as plt
import numpy as np
import datafileio as dio
import phshift as ps
import itertools as itt
import math

if len(sys.argv) != 3:
    print("Usage: python" + sys.argv[0] + " [gen track] [test track]")
    sys.exit()

track_x_gen, track_y_gen, obj_count_gen, fps= dio.read_tracks(sys.argv[1])
track_x_test, track_y_test, obj_count_test, fps = dio.read_tracks(sys.argv[2])

if obj_count_gen != 1 or obj_count_test != 1:
    print("obj_count_gen = " + str(obj_count_gen))
    print("obj_count_test = " + str(obj_count_test))
    print("obj_count_gen and obj_count_test should both be 1")
    sys.exit()


#Total number of tracking points per object
p_count = len(track_x_gen[0])
#Time axis values and frequency axis value
time_axis = np.linspace(0, p_count / fps, p_count)
freq_axis = np.linspace(0, fps / 2, p_count / 2 + 1)

#DC filtering
dc_x_gen = sum(track_x_gen[0]) / len(track_x_gen[0])
dc_y_gen = sum(track_y_gen[0]) / len(track_y_gen[0])
dc_x_test = sum(track_x_test[0]) / len(track_x_test[0])
dc_y_test = sum(track_y_test[0]) / len(track_y_test[0])

track_x_gen[0] = [x - dc_x_gen for x in track_x_gen[0]]
track_y_gen[0] = [y - dc_y_gen for y in track_y_gen[0]]
track_x_test[0] = [x - dc_x_test for x in track_x_test[0]]
track_y_test[0] = [y - dc_y_test for y in track_y_test[0]]

#Generate spectrum of all x, y track
spect_x_gen = np.fft.rfft(track_x_gen[0])
mag_x_gen = np.abs(spect_x_gen)

spect_y_gen = np.fft.rfft(track_y_gen[0])
mag_y_gen = np.abs(spect_y_gen)

spect_x_test = np.fft.rfft(track_x_test[0])
mag_x_test = np.abs(spect_x_test)

spect_y_test = np.fft.rfft(track_y_test[0])
mag_y_test = np.abs(spect_y_test)

#Normalize all spectrums
mag_scale = p_count / 2
for i in range(len(mag_x_gen)):
    mag_x_gen[i] = mag_x_gen[i] / mag_scale
    mag_y_gen[i] = mag_y_gen[i] / mag_scale
    mag_x_test[i] = mag_x_test[i] / mag_scale
    mag_y_test[i] = mag_y_test[i] / mag_scale

#Plot x movement related data
x_mov_fig, x_plots = plt.subplots(nrows = 2, ncols = 2)
x_plots[0, 0].plot(time_axis, track_x_gen[0])
x_plots[0, 0].set_title("Ground Truth Trajectory")

x_plots[1, 0].plot(freq_axis, mag_x_gen)
x_plots[1, 0].set_title("Ground Truth Spectrum")

x_plots[0, 1].plot(time_axis, track_x_test[0])
x_plots[0, 1].set_title("Tracked Trajectory")

x_plots[1, 1].plot(freq_axis, mag_x_test)
x_plots[1, 1].set_title("Tracked Spectrum")

for i in range(2):
    x_plots[0, i].set_xlabel("Time(s)")
    x_plots[0, i].set_ylabel("Amplitude(pixels)")
    x_plots[0, i].grid()

for i in range(2):
    x_plots[1, i].set_xlabel("Frequency(Hz)")
    x_plots[1, i].set_ylabel("Magnitude(pixels)")
    x_plots[1, i].grid()
    
x_mov_fig.suptitle("X Trajectory", fontsize = 20)
x_mov_fig.show()



#Plot y movement related data
y_mov_fig, y_plots = plt.subplots(nrows = 2, ncols = 2)
y_plots[0, 0].plot(time_axis, track_y_gen[0])
y_plots[0, 0].set_title("Ground Truth Trajectory")

y_plots[1, 0].plot(freq_axis, mag_y_gen)
y_plots[1, 0].set_title("Ground Truth Spectrum")

y_plots[0, 1].plot(time_axis, track_y_test[0])
y_plots[0, 1].set_title("Tracked Trajectory")

y_plots[1, 1].plot(freq_axis, mag_y_test)
y_plots[1, 1].set_title("Tracked Spectrum")

for i in range(2):
    y_plots[0, i].set_xlabel("Time(s)")
    y_plots[0, i].set_ylabel("Amplitude(pixels)")
    y_plots[0, i].grid()

for i in range(2):
    y_plots[1, i].set_xlabel("Frequency(Hz)")
    y_plots[1, i].set_ylabel("Magnitude(pixels)")
    y_plots[1, i].grid()
    
y_mov_fig.suptitle("Y Trajectory", fontsize = 20)
y_mov_fig.show()


raw_input("Press [Enter] to continue...")
