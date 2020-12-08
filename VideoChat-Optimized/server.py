import cv2
import imagezmq
image_hub = imagezmq.ImageHub()
while True:  # show streamed images until Ctrl-C
    clientName, image = image_hub.recv_image()
    cv2.imshow(clientName, image) # 1 window for each RPi
    cv2.waitKey(1)
    image_hub.send_reply(b'OK')