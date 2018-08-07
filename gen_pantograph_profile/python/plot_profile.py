import sys
import matplotlib.pyplot as plt
import datafileio as dio


if len(sys.argv) != 2:
    print("Usage: python" + sys.argv[0] + " [profile]")
    sys.exit()

x, y, tstep, count = dio.read_xy(sys.argv[1])

#Construct time axis data
time = count * [0.0]

for idx in range(1, count):
    time[idx] = time[idx - 1] + tstep


#Display
print('x = ' + str(x[0]))
print('tstep = ' + str(tstep))
print('count = ' + str(count))
plt.plot(time, y)
plt.title('Y movement')
plt.xlabel('Time(s)')
plt.ylabel('Y position(mm)')
plt.show()

