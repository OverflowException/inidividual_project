import sys
import datafileio as dio
import numana as na

if len(sys.argv) < 3:
    print("Usage: " + sys.argv[0] + " <profile config> <data> [prefix]")
    exit()


_, pkpk, freq, duration, tstep = dio.read_config(sys.argv[1])
#Number of points for each freqency segment
seg_points = []
for i in range(len(duration)):
    seg_points.append(na.profile_points(freq[i], duration[i], tstep))
# #Find duration ratio of each frequency segment
# duration_ratio = [float(p) / sum(seg_points) for p in seg_points]
# print(duration_ratio)

data_fd, obj_count, fps, total_frames = dio.read_tracks(sys.argv[2], storeTracks = False)

seg_frames = na.ratio_split(total_frames, seg_points)
print(seg_frames)

file_prefix = "" if len(sys.argv) == 3 else sys.argv[3]
#Copy to new segment files
#Traverse files
for f_idx in range(len(duration)):
    f_name = "{0}pkpk{1}_f{2}".format(file_prefix, int(pkpk[f_idx]), int(10 * freq[f_idx]))
    print(f_name)
    try:
        seg_data_fd = open(f_name, 'w')
    except IOError:
        print("Cannot open " + f_name)
        exit()
        
    #Write seg file header
    seg_data_fd.write("#FPS = %d\n" % (fps))
    seg_data_fd.write("#FRAMES = %d\n" % (seg_frames[f_idx]))
    seg_data_fd.write("#Object = %d\n" % (obj_count))

    #Copy onject tracks
    for fr in range(seg_frames[f_idx]):
        for ob in range(obj_count):
            line = data_fd.readline()
            seg_data_fd.write(line)
    
    seg_data_fd.close()


data_fd.close()
