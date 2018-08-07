import sys
import datafileio as dio
import math


if len(sys.argv) != 3:
    print("Usage: python" + sys.argv[0] + " [config] [profile]")
    sys.exit()

mid, pkpk, freq, duration, tstep = dio.read_config(sys.argv[1])
#Total number of wave form
nforms = len(mid)

#Number of data points for each wave form
npoint = nforms * [0]
for idx in range(nforms):
    #Number of complete cycles
    ncycle = round(freq[idx] * duration[idx])
    npoint[idx] = int(math.floor(ncycle / float(freq[idx]) / tstep))

#y position data
#Allocate y position data. 2D array, nforms of rows. Each row has different number of data points
y_pos = [[] for form in range(nforms)]

for form_idx in range(nforms):
    #Allocate data space for this wave form
    y_pos[form_idx] = [0.0] * npoint[form_idx]
    #Set parameters
    amp = float(pkpk[form_idx]) / 2
    omega = 2 * math.pi * freq[form_idx]
    dc = mid[form_idx]
    t = 0.0
    #generate data points
    for data_idx in range(npoint[form_idx]):
        y_pos[form_idx][data_idx] = amp * math.sin(omega * t) + dc
        t += tstep



x_pos = -20.0

dio.write_profile(sys.argv[2], x_pos, y_pos, tstep, '%.6f')
