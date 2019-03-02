# IMP: Import locale first 
import locale
locale.setlocale(locale.LC_ALL, 'C')

import cv2
import json
import requests
import sys
import tesserocr
from openalpr import Alpr

from secutopia.settings import BASE_DIR

# Absolute Video Path
video_dir_rel_path = "dl/Videos"
video_name = "video1.mp4"
video_path = BASE_DIR + '/' + video_dir_rel_path + '/' + video_path

# Destination URL
base_url = "http://10.32.8.101:8080/api/"
api_endpoint = "vehicle/transactions"
destination_url = base_url + api_endpoint

# Request parameters
headers = {'Content-Type':'application/json'}
body = {}

# Variables for request handling
licensePlate = ""

alpr = Alpr("in", "/etc/openalpr/openalpr.conf", "./openalpr/runtime_data")
if not alpr.is_loaded():
    print("Error loading OpenALPR")
    sys.exit(1)

# Select top 20 results
alpr.set_top_n(20)

cap = cv2.VideoCapture(video)
# cap.get(7)

# For smooth termination after video ends
# frame_counter = 0
# length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# while(frame_counter < length):
while True:
    ret,frame = cap.read()
    # frame_counter += 1
    results = alpr.recognize_ndarray(frame)

    for plate in results['results']:
        if plate['matches_template']:
            newPlate = plate['plate']
            if newPlate is not licensePlate:
                licensePlate = newPlate
                requests.post(url, data=json.dumps(licensePlate), headers=headers)
       
alpr.unload()
cap.release()