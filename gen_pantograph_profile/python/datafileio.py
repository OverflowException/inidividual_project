def read_config(filename):
    """Extract config data from config files.\n Usage mid, pkpk, freq, duration, tstep = read_config(filename)"""
    
    try:
        fd = open(filename, 'r')
    except IOError:
        print("Cannot open " + filename)

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

    
    x_pos_str = (precision %x_pos)
    fd = open(filename, 'w')
    
    fd.write('Pantograph Replay File NOTE: Modify just the deltaT value and the X&Y Values then save as a Tab Seperated .txt file)\n')
    fd.write('DeltaT(s)\t' + (precision %tstep) + '\n')
    fd.write('Xpos(mm)\tYpos(mm)\n')
    
    for wave_form in y_pos:
        for data in wave_form:
            fd.write(x_pos_str + '\t' + (precision %data) + '\n')
    
    fd.close()


