import cv2
# import cvlib as cv
from imutils import face_utils
import dlib
import numpy as np
import io
from PIL import Image

class VideoFeed:

    def __init__(self,mode=1,name="w1",capture=1):
        print(name)
        self.camera_index = 0
        self.name = name
        
        # self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        # self.facealigner = face_utils.FaceAligner(self.predictor, desiredFaceWidth=512)
        
        if capture == 1:
            self.cam = cv2.VideoCapture(self.camera_index)
            self.cam.set(3,852)
            self.cam.set(4,480)

    def get_frame(self):
        _, img = self.cam.read()
        img = cv2.flip(img, 1)
        cv2.waitKey(1)
        # if cv2.waitKey(1) & 0xFF == ord('n'):
        #     self.camera_index += 1 #try the next camera index
        #     self.cam = cv2.VideoCapture(self.camera_index)
        #     if not self.cam: #if the next camera index didn't work, reset to 0.
        #         self.camera_index = 0
        #         self.cam = cv2.VideoCapture(self.camera_index)

        # -------- RESIZING ----------
        # scale_percent = 50 # percent of original size
        # width = int(img.shape[1] * scale_percent / 100)
        # height = int(img.shape[0] * scale_percent / 100)
        # dim = (width, height)
        # dim = (852, 480)
        # resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        # img = resized
        # -------- END RESIZING -------

        # cv2.imshow('my webcam', img)

        # -------- OPEN CV ----------

        # CLASSIC
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        # for (x, y, w, h) in faces:
        #     cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # CVLIB
        # cv2_im = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # face, confidences = cv.detect_face(cv2_im)
        # for idx, f in enumerate(face):
        #     (startX, startY) = f[0], f[1]
        #     (endX, endY) = f[2], f[3]
        #     cv2.rectangle(cv2_im, (startX,startY), (endX,endY), (0,255,0), 2)

        # DLIB
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        rects = self.detector(gray, 0)
        
        for (i, rect) in enumerate(rects):
            face_bb = face_utils.rect_to_bb(rect)
            shape = self.predictor(gray, rect)
            
            upperFace_bb = [(0,0), (img.shape[1],shape.part(30).y)]
            lowerFace_bb = [(0,shape.part(30).y), (img.shape[1],img.shape[0])]

            # aligned = self.facealigner.align(img, gray, rect)

            # cv2.rectangle(img, face_bb, (0,255,0), 2)
            # cv2.line(img, (0, shape.part(30).y), (img.shape[1],shape.part(30).y),(255,0,0), 2)
            # cv2.circle(img, (shape.part(30).x, shape.part(30).y), 2, (0, 0, 255), 2)
            cv2.rectangle(img, lowerFace_bb[0], lowerFace_bb[1], (0,0,0), -1)

        # -------- END OPEN CV ----------

        cv2_im = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pil_im = Image.fromarray(cv2_im)
        b = io.BytesIO()
        pil_im.save(b, 'jpeg')
        im_bytes = b.getvalue()
        return im_bytes

    def set_frame(self, frame_bytes):
        pil_bytes = io.BytesIO(frame_bytes)
        pil_image = Image.open(pil_bytes)
        cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        cv2.imshow(self.name, cv_image)

if __name__=="__main__":
    vf = VideoFeed(1,"test",1)
    while 1:
        m = vf.get_frame()
        vf.set_frame(m)

