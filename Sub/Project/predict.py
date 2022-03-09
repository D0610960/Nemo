#!/usr/bin/env python
# coding: utf-8

# In[1]:


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from utils import file_processing, image_processing
import face_recognition
import create
from scipy import misc
import tensorflow as tf
import numpy as np
import cv2
import function
import time
import os

# basic size of per image
resize_width = 160
resize_height = 160

exist = ''
numStranger = 1
numUnknown = 1
numFamily = 1

# In[2]:


def face_recognition_image(names_list, dataset_emb, face_detect, face_net, dataset_path, filename, image_path):
    # read image
    image = image_processing.read_image_gbk(image_path)
    # start face detecting, get bounding_box
    bboxes, landmarks = face_detect.detect_face(image)
    bboxes, landmarks = face_detect.get_square_bboxes(bboxes, landmarks)

    if bboxes == [] or landmarks == []:
        return 'x'
    else:
        face_images = image_processing.get_bboxes_image(
            image, bboxes, resize_height, resize_width)
        face_images = image_processing.get_prewhiten_images(face_images)

        start = time.time()
        pred_emb = face_net.get_embedding(face_images)
        end = time.time()
        print('embedding: ', end-start)

        start = time.time()
        pred_name, pred_score = compare_embadding(
            pred_emb, dataset_emb, names_list)
        end = time.time()
        print('compare: ', end-start)

        '''
        # show result on image
        show_info=[ n+':'+str(s)[:5] for n,s in zip(pred_name, pred_score)]
        image_processing.show_image_bboxes_text("face_recognition", image, bboxes, show_info)
        '''
        return pred_name


def load_dataset(dataset_path, filename):
    embeddings = np.load(dataset_path)
    names_list = file_processing.read_data(
        filename, split=None, convertNum=False)
    return embeddings, names_list


def compare_embadding(pred_emb, dataset_emb, names_list, threshold=0.65):
    pred_num = len(pred_emb)
    dataset_num = len(dataset_emb)
    pred_name = []
    pred_score = []
    for i in range(pred_num):
        dist_list = []
        for j in range(dataset_num):
            dist = np.sqrt(
                np.sum(np.square(np.subtract(pred_emb[i, :], dataset_emb[j, :]))))
            dist_list.append(dist)
        min_value = min(dist_list)
        pred_score.append(min_value)
        if (min_value > threshold):
            pred_name.append('foreign')
        else:
            pred_name.append(names_list[dist_list.index(min_value)])
    return pred_name, pred_score

# In[3]:


def predictMember(path, dataset_emb, names_list, face_detect, face_net, dataset_path, filename):
    global exist
    global numStranger
    global numUnknown
    global numFamily

    if int(time.strftime('%S')) % 10 == 0:
        # download lastest image
        image_name = function.downloadImage(path)

        # if have not predicted
        if exist != image_name:
            exist = image_name
            image_path = os.path.join(path, image_name)

            start = time.time()
            result = face_recognition_image(
                names_list, dataset_emb, face_detect, face_net, dataset_path, filename, image_path)
            end = time.time()
            print('predict: ', end-start)

            if result == 'x':
                pass
            elif set(result).difference(['foreign']) == set():
                function.uploadPredictResult(
                    "Stranger", numStranger, image_name)
                print('Stranger', result)
                numStranger += 1
                if numStranger > 5:
                    numStranger = 1
            # if image contains at least one family member
            elif set(result).difference(names_list) == set(['foreign']):
                function.uploadPredictResult("Unknown", numUnknown, image_name)
                print('Unknown', result)
                numUnknown += 1
                if numUnknown > 5:
                    numUnknown = 1
            else:
                function.uploadPredictResult("Family", numFamily, image_name)
                print('Family', result)
                numFamily += 1
                if numFamily > 5:
                    numFamily = 1
            print('==================================')
        else:
            pass


# In[4]:


def start():
    print('start predict')
    model_path = 'models/20180408-102900.pb'
    dataset_path = 'dataset/emb/faceEmbedding.npy'
    filename = 'dataset/emb/name.txt'
    path = 'camera/'

    # initialize MTCNN
    face_detect = face_recognition.Facedetection()
    # initialize facenet
    face_net = face_recognition.facenetEmbedding(model_path)
    dataset_emb, names_list = load_dataset(dataset_path, filename)
    
    cnt = 0
    while True:
        try:
            if(cnt == 600):
                # clear real time images
                print("clear")
                os.system("rm -rf /home/pi/Project/camera/*.jpg")
                cnt = 0
                
            retrain = function.getRetrain()
            camMode, camTimedOn = function.getCamMode()

            # new memmber is detected
            if retrain == 'on':
                # start training
                create.train_members_model()
                # change retrain flag on firebase
                function.uploadRetrain()
                # reload model
                dataset_emb, names_list = load_dataset(dataset_path, filename)
            else:
                # if camera mode is on
                if camMode == 'on':
                    predictMember(path, dataset_emb, names_list,
                                  face_detect, face_net, dataset_path, filename)
                    cnt += 1
                # if camera mode is off
                else:
                    # if timed on mode is on
                    if camTimedOn == 'on':
                        duration, diff = function.camTimedOnRange()
                        # if in time range
                        if duration > diff:
                            # predict
                            predictMember(path, dataset_emb, names_list,
                                          face_detect, face_net, dataset_path, filename)
                            cnt += 1
                        else:
                            pass
                    else:
                        pass
        except Exception as e:
            print('Error:', e)
        finally:
            pass
        continue

# In[5]:


if __name__ == '__main__':
    start()
