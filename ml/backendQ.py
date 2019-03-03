import time
import locale
locale.setlocale(locale.LC_ALL, 'C')
import tesserocr
from openalpr import Alpr
import cv2
import requests
import json
import queue
import statistics


video = "../../Images/EvalFiles/vid4.mp4"

# Destination URL
base_url = "http://10.32.8.101:8080/api/"
api_endpoint = "vehicle/transactions"
url = base_url + api_endpoint

# Request parameters
headers = {'Content-Type':'application/json'}

# Variables for request handling
licensePlate = ""
plates = queue.Queue(maxsize=10)

alpr = Alpr("in", "/usr/local/share/openalpr/config/openalpr.defaults.conf", "./openalpr/runtime_data")
if not alpr.is_loaded():
    print("Error loading OpenALPR")
    sys.exit(1)

# select top 20 results
alpr.set_top_n(20)
alpr.set_default_region("in")

cap = cv2.VideoCapture(video)
start_time = time.time()
# cap.get(7)

# for smooth termination after video ends
frame_counter = 0
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(length)

while(frame_counter < length):
    ret, frame = cap.read()
    frame_counter += 3  
    print(frame_counter)
    results = alpr.recognize_ndarray(frame)

    for plate in results['results']:
        if plates.qsize() == 10:
            plates.get()

        plates.put(plate['plate'])
        # print(plates.queue)
        if plates.qsize() >= 5:
            mostFrequent = statistics.mode(list(plates.queue))

            if mostFrequent != licensePlate:
                licensePlate = mostFrequent
                print(licensePlate)
                request_data = {
                    'license_plate': licensePlate,
                    'is_entry': False
                }
                requests.post(url, data=json.dumps(request_data), headers=headers)

print("--- %s seconds ---" % (time.time() - start_time))             
alpr.unload()
cap.release()