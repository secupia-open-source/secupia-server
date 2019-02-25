import locale
locale.setlocale(locale.LC_ALL, 'C')
import tesserocr
from openalpr import Alpr
import sys
import cv2


video = "../../Images/video1.mp4"


alpr = Alpr("in", "/etc/openalpr/openalpr.conf", "./openalpr/runtime_data")
if not alpr.is_loaded():
    print("Error loading OpenALPR")
    sys.exit(1)

# select top 20 results
alpr.set_top_n(20)

cap = cv2.VideoCapture(video)

# for smooth termination after video ends
frame_counter = 0
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

while(frame_counter < length):

        ret,frame = cap.read()
        frame_counter += 1
        results = alpr.recognize_ndarray(frame)

        # print(results['results'])
        i = 0
        for plate in results['results']:
                i += 1
                print("Plate #%d" % i)
                print("  %12s %12s" % ("Plate", "Confidence"))
                for candidate in plate['candidates']:
                        # prefix = "-"
                        if candidate['matches_template']:
                            prefix = "*"
                            print("  %s %12s%12f" % (prefix, candidate['plate'], candidate['confidence']))

               
alpr.unload()
cap.release()