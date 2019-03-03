import locale
locale.setlocale(locale.LC_ALL, 'C')
import tesserocr
from openalpr import Alpr
import sys
import cv2
import requests
import json


video = "../../Images/video1.mp4"

# Destination URL
base_url = "http://10.32.8.101:8080/api/"
api_endpoint = "vehicle/transactions"
url = base_url + api_endpoint

# Request parameters
headers = {'Content-Type':'application/json'}

# Variables for request handling
licensePlate = ""

alpr = Alpr("in", "/etc/openalpr/openalpr.conf", "./openalpr/runtime_data")
if not alpr.is_loaded():
    print("Error loading OpenALPR")
    sys.exit(1)

# select top 20 results
alpr.set_top_n(20)

cap = cv2.VideoCapture(video)
# cap.get(7)

# for smooth termination after video ends
frame_counter = 0
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
# print(length)

while(frame_counter < length):
    ret,frame = cap.read()
    frame_counter += 1
    results = alpr.recognize_ndarray(frame)

    for plate in results['results']:
        if plate['matches_template']:
            newPlate = plate['plate']
            if newPlate is not licensePlate:
                licensePlate = newPlate
                # data = {'data': [{'key1':licensePlate}]}
                print(licensePlate)
                print(type(licensePlate))
                request_data = {
                    'license_plate': licensePlate,
                    'is_entry': False
                }
                requests.post(url, data=json.dumps(request_data), headers=headers)

        # if newPlate['matches_template']:
        #     if newPlate['plate'] is not licensePlate:
        #         newPlate['plate'] = licensePlate 
        #         print("  %12s %12s" % ("Plate", "Confidence"))
        #         print("    %12s %12f" % (licensePlate, newPlate['confidence']))

       
alpr.unload()
cap.release()