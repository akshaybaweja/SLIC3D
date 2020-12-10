import cv2
from imutils import face_utils
import imutils
import dlib
import numpy as np
import imagezmq
image_hub = imagezmq.ImageHub()

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

images = {"macbook-pro": None, "macbook-air": None}
def merge_images(upperImage, lowerImage):

        upperImageSliced = None
        lowerImageSliced = None
        upperFaceArea = None
        lowerFaceArea = None

        try:
            upperImageSliced = getFaceSlice(upperImage)
            lowerImageSliced = getFaceSlice(lowerImage, False)
        except:
            pass

        if upperImageSliced is not None and lowerImageSliced is not None:

            mergedImage = np.vstack((upperImageSliced, lowerImageSliced))
        elif upperImageSliced is not None and lowerImageSliced is None:
            mergedImage = upperImage
        elif upperImageSliced is not None and lowerImageSliced is None:
            mergedImage = lowerImage
        else:
            mergedImage = upperImage
        
        imutils.resize(mergedImage, width=720)
        return mergedImage

def getFaceSlice(img, getUpper = True):
        # -------- OPEN CV ----------
        # DLIB
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        rects = detector(gray, 0)
        for (i, rect) in enumerate(rects):
            shape = predictor(gray, rect)
            face_bb = face_utils.rect_to_bb(rect)
            
            if getUpper:
                return img[0:shape.part(30).y, 0:img.shape[1]]
            else:
                return img[shape.part(30).y:img.shape[0], 0:img.shape[1]]

while True:  # show streamed images until Ctrl-C
    clientName, image = image_hub.recv_image()
    images[clientName] = image
    merged = merge_images(images["macbook-pro"], images["macbook-air"])
    cv2.imshow("SLIC3D", merged) # 1 window for each RPi
    cv2.waitKey(1)
    image_hub.send_reply(b'OK')