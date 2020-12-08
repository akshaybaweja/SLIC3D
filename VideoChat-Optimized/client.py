# run this program on each RPi to send a labelled image stream
import socket
import time
import imutils
from imutils.video import VideoStream
import imagezmq

sender = imagezmq.ImageSender(connect_to='tcp://127.0.0.1:5555')

clientName = "client-macbook-pro"
camera = VideoStream(src=0).start()
time.sleep(2.0)  # allow camera sensor to warm up

while True:  # send images as stream until Ctrl-C
	image = camera.read()
	image = imutils.resize(image, width=480)
	sender.send_image(clientName, image)