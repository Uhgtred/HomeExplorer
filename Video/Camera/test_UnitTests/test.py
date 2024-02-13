#!/usr/bin/env python3
# @author: Markus Kösters
import time

import cv2

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 30)
framecounter = 0
start = time.time()
stop = 0
while stop - start < 5:
    # Capture frame-by-frame
    ret, frame = cap.read()
    framecounter += 1
    stop = time.time()
print(stop - start)
print(framecounter)