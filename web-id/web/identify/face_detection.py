from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
from scipy import misc
import cv2
import matplotlib.pyplot as plt
import numpy as np
import argparse
from . import facenet
from . import detect_face
import os
from os.path import join as pjoin
import sys
import time
import copy
import math
import pickle
from sklearn.svm import SVC
from sklearn.externals import joblib
from . import const
from web import settings



def face_detect(label):
    with tf.Graph().as_default():
        gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.6)
        sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
        with sess.as_default():
            pnet, rnet, onet = detect_face.create_mtcnn(sess, os.path.join(settings.BASE_DIR, 'identify/d_npy/'))

            minsize = 20  # minimum size of face
            threshold = [0.6, 0.7, 0.7]  # three steps's threshold
            factor = 0.709  # scale factor
            margin = 44
            frame_interval = 3
            batch_size = 1000
            image_size = 182
            input_image_size = 160
            video_path = os.path.join(const.VIDEO_PATH, str(label))
            number_of_faces = 1
            counter = 1

  
            folder= os.path.join(const.FACE_TRAIN_FOLDER, str(label),'')
            if not os.path.exists(folder):
                os.makedirs(folder)

            for dirname, dirnames, filenames in os.walk(video_path):
                for filename in filenames:
                    video = os.path.join(dirname, filename)
                    # print(video)
                    
                    video_capture = cv2.VideoCapture(video)
                    
                    # while True:
                    while video_capture.isOpened():
                        # capture frame by frame
                        ret, frame = video_capture.read()
                        if ret:
                            try:
                                frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)    #resize frame (optional)
                                frame = frame[:, :, 0:3]
                                bounding_boxes, _ = detect_face.detect_face(frame, minsize, pnet, rnet, onet, threshold, factor)
                                nrof_faces = bounding_boxes.shape[0]
                                # print('Detected_FaceNum: %d' % nrof_faces)

                                if nrof_faces > 0: 
                                    number_of_faces += 1
                                    if number_of_faces % 5 == 0:
                                        FaceFileName = folder + str(10 + number_of_faces) + ".jpg"
                                        print(FaceFileName)
                                        cv2.imwrite(FaceFileName, frame)
                                    # enter character 'q' to quit
                            except Exception as e:
                                print(e)
                        else:
                            break

                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                                # else:
                                #     break
                        
                    # when everything is done, release the capture
                    print("destroy...., number of images: {0}".format(number_of_faces))
                    video_capture.release()

            return number_of_faces
    # if __name__ == "__main__":
    #     face_detect(1)
