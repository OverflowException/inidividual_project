import sys
import cv2

if len(sys.argv) != 4:
    print("Usage: python " + sys.argv[0] + " [in video] [out image] [frame number]")
    print("Frame number starts from 0")
    sys.exit()

cap = cv2.VideoCapture(sys.argv[1])

for idx in range(int(sys.argv[3]) + 1):
    ret, frame = cap.read()
    #End of video
    if ret == False:
        print("Frame number exceeds total frame number")
        print("max = " + str(idx - 1))
        break;

cv2.imwrite(sys.argv[2], frame)

