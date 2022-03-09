#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
from utils import image_processing, file_processing, debug
import face_recognition
import cv2
import os
import sys
import shutil
import pyrebase

resize_width = 160
resize_height = 160

config = {
    "apiKey": "AIzaSyCZIO4jkPAZXIM_L1rEcu1LMx8JAFbe8-c",
    "authDomain": "littlepi-78630.firebaseapp.com",
    "databaseURL": "https://littlepi-78630.firebaseio.com",
    "projectId": "littlepi-78630",
    "storageBucket": "littlepi-78630.appspot.com",
    "messagingSenderId": "95913815433",
    "appId": "1:95913815433:web:3b8dcc3f9ad8bd831e0558",
    "measurementId": "G-4284WKWVBT"
}
firebase = pyrebase.initialize_app(config)
database = firebase.database()
storage = firebase.storage()


# In[2]:


def removeFolder(path):
    files = os.listdir(path)

    for file in files:
        fullpath = os.path.join(path, file)
        print('file name:', fullpath)
        if os.path.isdir(fullpath):
            shutil.rmtree(fullpath)


def downloadAllMemberImage(dataset_path):
    # clear dataset
    removeFolder(dataset_path)

    # get all members
    all_members = database.child('USERDATA/Member').get()
    for member in all_members.each():
        print("id:", member.key(), " ,name:", member.val())
        folder_path = dataset_path + member.val()
        ref = 'face/' + member.val() + '/'
        os.mkdir(folder_path)
        for i in range(1, 4):
            img_name = str(i) + '.jpg'
            storage.child(ref + img_name).download(folder_path + '/' + img_name)


# In[3]:


def get_face_embedding(model_path, files_list, names_list):
    colorSpace = "RGB"
    # initialize MTCNN
    face_detect = face_recognition.Facedetection()
    # initialize facenet
    face_net = face_recognition.facenetEmbedding(model_path)

    embeddings = []
    label_list = []
    for image_path, name in zip(files_list, names_list):
        print("processing image :{}".format(image_path))
        # read image
        image = image_processing.read_image_gbk(
            image_path, colorSpace=colorSpace)
        # start face detecting, get bounding_box
        bboxes, landmarks = face_detect.detect_face(image)
        bboxes, landmarks = face_detect.get_square_bboxes(bboxes, landmarks)

        # ignore no face and multiple faces statement
        if bboxes == [] or landmarks == []:
            print("-----no face")
            continue
        if len(bboxes) >= 2 or len(landmarks) >= 2:
            print("-----image have {} faces".format(len(bboxes)))
            continue

        face_images = image_processing.get_bboxes_image(
            image, bboxes, resize_height, resize_width)
        # prewhiten
        face_images = image_processing.get_prewhiten_images(
            face_images, normalization=True)
        # get features and save labels
        pred_emb = face_net.get_embedding(face_images)
        embeddings.append(pred_emb)
        label_list.append(name)
    return embeddings, label_list


def create_face_embedding(model_path, dataset_path, out_emb_path, out_filename):
    files_list, names_list = file_processing.gen_files_labels(
        dataset_path, postfix=['*.jpg', '*.png'])
    embeddings, label_list = get_face_embedding(
        model_path, files_list, names_list)
    print("label_list:{}".format(label_list))
    print("have {} label".format(len(label_list)))

    embeddings = np.asarray(embeddings)
    np.save(out_emb_path, embeddings)
    file_processing.write_list_data(out_filename, label_list, mode='w')

# In[4]:


def train_members_model():
    model_path = 'models/20180408-102900.pb'
    dataset_path = 'dataset/members/'
    out_emb_path = 'dataset/emb/faceEmbedding.npy'
    out_filename = 'dataset/emb/name.txt'

    downloadAllMemberImage(dataset_path)
    create_face_embedding(model_path, dataset_path, out_emb_path, out_filename)


# In[5]:


if __name__ == '__main__':
    train_members_model()
