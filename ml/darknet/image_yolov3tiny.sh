
# Detect car from images
./darknet detect cfg/yolov3-tiny.cfg yolov3-tiny.weights ~/chevrolet-beat-front-photo.jpg       
# ./darknet detect cfg/yolov3-tiny.cfg yolov3-tiny.weights ~/chevrolet-cruze-road-test-photo.jpg 


# detect license plate
alpr -c in -j result_img/*.jpg