from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
import numpy as np
import argparse
from . import facenet, const
from . import detect_face
import os
import sys
import math
import pickle
from sklearn.svm import SVC
from scipy import spatial



    
def getEmbeddingVectors(datadir):
    with tf.Graph().as_default():

        with tf.Session() as sess:

            # print(datadir)

            print('Loading feature extraction model')
            modeldir = os.path.join(const.PAS_FOLDER + 'pre_model/20180402-114759.pb')
            facenet.load_model(modeldir)

            images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
            embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
            phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
            embedding_size = embeddings.get_shape()[1]

            # Run forward pass to calculate embeddings
            print('Calculating features for images')
            batch_size = 1000
            image_size = 160
            paths = facenet.get_dataset(datadir)
            nrof_images = len(paths)
            nrof_batches_per_epoch = int(math.ceil(1.0 * nrof_images / batch_size))
            emb_array = np.zeros((nrof_images, embedding_size))
            for i in range(nrof_batches_per_epoch):
                start_index = i * batch_size
                end_index = min((i + 1) * batch_size, nrof_images)
                paths_batch = paths[start_index:end_index]
                images = facenet.load_data(paths_batch, False, False, image_size)
                feed_dict = {images_placeholder: images, phase_train_placeholder: False}
                emb_array[start_index:end_index, :] = sess.run(embeddings, feed_dict=feed_dict)
        
            emb_array_np = np.array(emb_array)
            # emb_arry_mean=np.mean(emb_array_np, axis=0)
            # max_distance = np.max(np.sqrt(np.sum( np.square(emb_array_np-emb_arry_mean), axis=1)), axis=0)
            # max_distance = np.max()
            np.savetxt("array.csv",emb_array_np , delimiter=",")
            max_dist = np.max(spatial.distance.cdist(emb_array_np,emb_array_np,metric='cosine'))
            return emb_array_np, max_dist
        # classifier_filename = './my_class/my_classifier.pkl'
        # classifier_filename_exp = os.path.expanduser(classifier_filename)

        # # Train classifier
        # print('Training classifier')
        # model = SVC(kernel='linear', probability=True)
        # model.fit(emb_array, labels)

        # # Create a list of class names
        # class_names = [cls.name.replace('_', ' ') for cls in dataset]

        # # Saving classifier model
        # with open(classifier_filename_exp, 'wb') as outfile:
        #     pickle.dump((model, class_names), outfile)
        # print('Saved classifier model to file "%s"' % classifier_filename_exp)
        # print('Goodluck')
