import locale
locale.setlocale(locale.LC_ALL, 'C')
import tesserocr
from openalpr import Alpr
import sys
import cv2
import time


video = "../../Images/vid1.mp4"


alpr = Alpr("in", "/usr/local/share/openalpr/config/openalpr.defaults.conf", "./openalpr/runtime_data")
if not alpr.is_loaded():
    print("Error loading OpenALPR")
    sys.exit(1)

# select top 10 results
alpr.set_top_n(10)
alpr.set_default_region("in")

cap = cv2.VideoCapture(video)

# for smooth termination after video ends
frame_counter = 0
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(length)

start_time = time.time()

while(frame_counter < length):

    ret,frame = cap.read()
    frame_counter += 3
    results = alpr.recognize_ndarray(frame)

    # print(results['results'])
    i = 0
    for plate in results['results']:
        i += 1
        print("Plate #%d" % i)
        print("  %12s %12s" % ("Plate", "Confidence"))
        for candidate in plate['candidates']:
            # prefix = "-"
            # if candidate['matches_template']:
            prefix = "*"
            print("  %s %12s%12f" % (prefix, candidate['plate'], candidate['confidence']))


print("--- %s seconds ---" % (time.time() - start_time))             
alpr.unload()
cap.release()