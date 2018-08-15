import sys
import re
import matplotlib.pyplot as plt
import numpy as np
import itertools as itt
import math
import datafileio as dio
import numana as na


if len(sys.argv) != 3:
    print("Usage: python" + sys.argv[0] + " [gen track] [test track]")
    sys.exit()

track_x_gen, track_y_gen, obj_count_gen, fps, _ = dio.read_tracks(sys.argv[1])
track_x_test, track_y_test, obj_count_test, fps, _  = dio.read_tracks(sys.argv[2])

if obj_count_gen != 1 or obj_count_test != 1:
    print("obj_count_gen = " + str(obj_count_gen))
    print("obj_count_test = " + str(obj_count_test))
    print("obj_count_gen and obj_count_test should both be 1")
    sys.exit()


#Time axis values and frequency axis value
time_axis = np.linspace(0, len(track_x_gen[0]) / fps, len(track_x_gen[0]))
    
mag_x_gen, phase_x_gen, eng_x_gen, freq_axis = na.fft_scaled(track_x_gen[0], fps)
mag_y_gen, phase_y_gen, eng_y_gen, _ = na.fft_scaled(track_y_gen[0], fps)
mag_x_test, phase_x_test, eng_x_test, _ = na.fft_scaled(track_x_test[0], fps)
mag_y_test, phase_y_test, eng_y_test, _ = na.fft_scaled(track_y_test[0], fps)

dc_x_gen = mag_x_gen[0]
mag_x_gen[0] = 0
dc_y_gen = mag_y_gen[0]
mag_y_gen[0] = 0
dc_x_test = mag_x_test[0]
mag_x_test[0] = 0
dc_y_test = mag_y_test[0]
mag_y_test[0] = 0

#Eliminate tiny fluctuations in ground truth
for i in range(len(mag_x_gen)):
    mag_x_gen[i] = 0 if mag_x_gen[i] < 0.05 else mag_x_gen[i]
    mag_y_gen[i] = 0 if mag_y_gen[i] < 0.05 else mag_y_gen[i]

#Get peak location
peak_x_gen, _ = na.get_extrema(mag_x_gen)
peak_y_gen, _ = na.get_extrema(mag_y_gen)

#Print DC info
print("\nX DC component")
print("Ground(deg)\tTracked(deg)\tError rate")
print("%f\t%f\t%f" % (dc_x_gen, dc_x_test, abs(dc_x_gen - dc_x_test) / dc_x_gen))

print("\nY DC component")
print("Ground(deg)\tTracked(deg)\tError Rate")
print("%f\t%f\t%f" % (dc_y_gen, dc_y_test, abs(dc_y_gen - dc_y_test) / dc_y_gen))

#Print AC magnitude info
print("\nX AC component magnitude:")
print("Frequency(Hz)\tGround(pix)\tTracked(pix)\tError Rate")
for i in range(len(peak_x_gen)):
    peak_loc = peak_x_gen[i]
    print("%f\t%f\t%f\t%f" % (freq_axis[peak_loc], mag_x_gen[peak_loc], mag_x_test[peak_loc], abs((mag_x_gen[peak_loc] - mag_x_test[peak_loc]) / mag_x_gen[peak_loc])))

print("\nY AC component magnitude:")
print("Frequency(Hz)\tGround(pix)\tTracked(pix)\tError Rate")
for i in range(len(peak_y_gen)):
    peak_loc = peak_y_gen[i]
    print("%f\t%f\t%f\t%f" % (freq_axis[peak_loc], mag_y_gen[peak_loc], mag_y_test[peak_loc], abs((mag_y_gen[peak_loc] - mag_y_test[peak_loc]) / mag_y_gen[peak_loc])))
    
#Print AC phase info
print("\nX AC components phase:")
print("Frequency(Hz)\tGround(deg)\tTracked(deg)\tError Rate")
for i in range(len(peak_x_gen)):
    peak_loc = peak_x_gen[i]
    print("%f\t%f\t%f\t%f" % (freq_axis[peak_loc], phase_x_gen[peak_loc], phase_x_test[peak_loc], abs((phase_x_gen[peak_loc] - phase_x_test[peak_loc]) / phase_x_gen[peak_loc])))

print("\nY AC components phase:")
print("Frequency(Hz)\tGround(deg)\tTracked(deg)\tError Rate")
for i in range(len(peak_y_gen)):
    peak_loc = peak_y_gen[i]
    print("%f\t%f\t%f\t%f" % (freq_axis[peak_loc], phase_y_gen[peak_loc], phase_y_test[peak_loc], abs((phase_y_gen[peak_loc] - phase_y_test[peak_loc]) / phase_y_gen[peak_loc])))

#Print energy leakage
#eng_x_clean = [mag_x_test[p] for p in [mag_x_gen[i] for i in peak_x_gen]]
eng_x_clean = sum([mag_x_test[loc] ** 2 for loc in peak_x_gen])
eng_y_clean = sum([mag_y_test[loc] ** 2 for loc in peak_y_gen])
print("AC Energy Leakage Rate:")
print("X: %f" %(1 - eng_x_clean / (sum(eng_x_test) - dc_x_test ** 2)))
print("Y: %f" %(1 - eng_y_clean / (sum(eng_y_test) - dc_y_test ** 2)))
    
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
