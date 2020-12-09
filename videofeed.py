import cv2
# import cvlib as cv
from imutils import face_utils
import dlib
import numpy as np
import io
from PIL import Image
import time
import random 

class VideoFeed:

    def __init__(self,mode=1,name="w1",capture=1):
        print(name)
        self.camera_index = 0
        self.name = name
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

        if capture == 1:
            self.cam = cv2.VideoCapture(self.camera_index)
            self.cam.set(3,640)
            self.cam.set(4,480)

    def get_frame(self):
        _, img = self.cam.read()
        img = cv2.flip(img, 1)
        
        cv2.waitKey(1)
        # cv2.imshow('my webcam', img)

        cv2_im = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pil_im = Image.fromarray(cv2_im)
        b = io.BytesIO()
        pil_im.save(b, 'jpeg')
        im_bytes = b.getvalue()
        return im_bytes

    def merge_images(self, upperImage, lowerImage):

        upperImageSliced = self.getFaceSlice(upperImage)
        lowerImageSliced = self.getFaceSlice(lowerImage, False)

        if upperImageSliced is not None and lowerImageSliced is not None:
            if upperImageSliced.ndim is not 0 and lowerImageSliced.ndim is not 0:
                mergedImage = np.vstack((upperImageSliced, lowerImageSliced))
                # print("Shukar hai rabba")
        elif upperImageSliced is not None and lowerImageSliced is None:
            # print("upperImageSliced - None nhi hai")
            mergedImage = upperImage
        elif upperImageSliced is not None and lowerImageSliced is None:
            # print("lowerImageSliced - None nhi hai")
            mergedImage = lowerImage
        else:
            # print("hello")
            mergedImage = upperImage
        
        cv2.resize(mergedImage, (640, 480),  interpolation = cv2.INTER_NEAREST)
        return mergedImage
    
    def getFaceSlice(self, img, getUpper = True):
        # -------- OPEN CV ----------
        # DLIB
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        rects = self.detector(gray, 0)
        
        for (i, rect) in enumerate(rects):
            # face_bb = face_utils.rect_to_bb(rect)
            shape = self.predictor(gray, rect)
            
            upperFace_bb = [(0,0), (img.shape[1],shape.part(30).y)]
            lowerFace_bb = [(0,shape.part(30).y), (img.shape[1],img.shape[0])]

            if getUpper:
                # cv2.rectangle(img, lowerFace_bb[0], lowerFace_bb[1], (0,0,0), -1)
                return img[0:shape.part(30).y, 0:img.shape[1]]
            else:
                # cv2.rectangle(img, upperFace_bb[0], upperFace_bb[1], (0,0,0), -1)
                return img[shape.part(30).y:img.shape[0], 0:img.shape[1]]

            # return img

            # cv2.rectangle(img, face_bb, (0,255,0), 2)
            # cv2.line(img, (0, shape.part(30).y), (img.shape[1],shape.part(30).y),(255,0,0), 2)
            # cv2.circle(img, (shape.part(30).x, shape.part(30).y), 2, (0, 0, 255), 2)
        # -------- END OPEN CV ---------- 

    def set_frame(self, frame_bytes, frame_bytes_self):
        pil_bytes = io.BytesIO(frame_bytes)
        pil_image = Image.open(pil_bytes)
        cv_image_remote = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

        pil_bytes_self = io.BytesIO(frame_bytes_self)
        pil_image_self = Image.open(pil_bytes_self)
        cv_image_self = cv2.cvtColor(np.array(pil_image_self), cv2.COLOR_RGB2BGR)

        cv_image = self.merge_images(cv_image_self, cv_image_remote)
        cv2.imshow(self.name, cv_image)

if __name__=="__main__":
    vf = VideoFeed(1,"test",1)
    while 1:
        m = vf.get_frame()
        vf.set_frame(m, m)

