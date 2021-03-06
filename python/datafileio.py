import re

def read_tracks(filename, storeTracks = True):
    """pass data filename, return tracks of x tracks, y tracks, number of objects and fps"""
    """Set storeTracks to False, will only read header. Saves time and space"""
    
    try:
        fd = open(filename, 'r')
    except IOError:
        print("Cannot open " + filename)
        exit()
    
    #regular expressions
    fps_pattern = re.compile("#FPS = (\d+)")
    frames_pattern = re.compile("#FRAMES = (\d+)")
    obj_pattern = re.compile("#Object = (\d+)")
    point_pattern = re.compile("\[(\d+\.?\d*), (\d+\.?\d*)\]")

    while True:
        line = fd.readline()
        #Irrelavent line
        if line[0] == '#':
            break

    m = fps_pattern.search(line)
    fps = int(m.group(1))

    line = fd.readline()
    m = frames_pattern.search(line)
    nframes = int(m.group(1))
    
    line = fd.readline()        
    m = obj_pattern.search(line)
    obj_count = int(m.group(1))

    if not storeTracks:
        return fd, obj_count, fps, nframes
    
    #2D arrays, storing track of x and y respectively
    #e.g. structure of obj_x_tracks, m objects, n points each
    # [
    #     [x00, x01, .... x0n]
    #     [x10, x11, .... x1n]
    #     [x20, x21, .... x2n]
    #     [x30, x31, .... x3n]
    #     .
    #     .
    #     [xm0, xm1, .... xmn]
    # ]

    obj_x_tracks = [[] for row in range(obj_count)]
    obj_y_tracks = [[] for row in range(obj_count)]
    
    #Read file
    obj_idx = 0
    while True:
        line = fd.readline()
        if not line:
            break;

        m = point_pattern.search(line)
    
        obj_x_tracks[obj_idx].append(float(m.group(1)))
        obj_y_tracks[obj_idx].append(float(m.group(2)))
    
        obj_idx = (obj_idx + 1) % obj_count
    
    #Close file
    fd.close()

    return obj_x_tracks, obj_y_tracks, obj_count, fps, nframes


def read_config(filename):
    """Extract config data from config files.\n Usage mid, pkpk, freq, duration, tstep = read_config(filename)"""
    
    try:
        fd = open(filename, 'r')
    except IOError:
        print("Cannot open " + filename)
        exit()

    mid = []
    pkpk = []
    freq = []
    duration = []
    tstep = 0
    
    #ignore comments
    line = fd.readline()
    while True:
        if line[0] != '#':
            break;
        line = fd.readline()
        
    #Extract DeltaT
    while True:
        seg = line.split()
        #This is the DeltaT line
        if seg[0] == 'DeltaT(s)':
            tstep = float(seg[1])
            break
        line = fd.readline()
        
    #Find header
    while True:
        line = fd.readline()
        seg = line.split()
        if len(seg) == 4 and seg[0] == 'Midpoint(mm)' and seg[1] == 'pk-pk(mm)' and seg[2] == 'Frequency(Hz)' and seg[3] == 'Duration(s)':
            break;

    while True:
        line = fd.readline()
        if not line:
            break

        seg = line.split()
        if len(seg) == 0:
            break;
        
        mid.append(float(seg[0]))
        pkpk.append(float(seg[1]))
        freq.append(float(seg[2]))
        duration.append(float(seg[3]))
    
    
    fd.close()
            
    return mid, pkpk, freq, duration, tstep

def read_profile(filename):
    """Extract profile data from pantograph profile.\nUsage: x, y, tstep, count = read_profile(filename)"""
    
    try:
        fd = open(filename, 'r')
    except IOError:
        print("Cannot open " + filename)
        exit()
    
    line = fd.readline()
    while True:
        seg = line.split()
        #This line contains 2 segments
        if len(seg) == 2:
            #This is the 'DeltaT' line
            if seg[0][0:6] == 'DeltaT':
                tstep = float(seg[1])
            #This is the 'Xpos(mm) Ypos(mm) header'
            elif seg[0] == 'Xpos(mm)' and seg[1] == 'Ypos(mm)':
                break
        line = fd.readline()


    x = []
    y = []
    count = 0
        
    #Read file
    while True:
        line = fd.readline()
        if not line:
            break;

        line_seg1, line_seg2 = line.split()
    
        x.append(float(line_seg1))
        y.append(float(line_seg2))

        count += 1
    
    fd.close()

    return x, y, tstep, count

def write_profile(filename, x_pos, y_pos, tstep, precision):
    try:
        fd = open(filename, 'w')
    except IOError:
        print("Cannot open " + filename + " to write!")
        exit()

    
    x_pos_str = (precision %x_pos)
    fd = open(filename, 'w')
    
    fd.write('Pantograph Replay File NOTE: Modify just the deltaT value and the X&Y Values then save as a Tab Seperated .txt file)\n')
    fd.write('DeltaT(s)\t' + (precision %tstep) + '\n')
    fd.write('Xpos(mm)\tYpos(mm)\n')
    
    for wave_form in y_pos:
        for data in wave_form:
            fd.write(x_pos_str + '\t' + (precision %data) + '\n')
    
    fd.close()


