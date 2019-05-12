import os
import sys
import random
import math
import numpy as np
import skimage.io
import h5py

import coco
from mrcnn import utils
from mrcnn import model as modellib
from mrcnn import visualize

class InferenceConfig(coco.CocoConfig):
    # Set batch size to 1 since we'll be running inference on
    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

config = InferenceConfig()
#config.display()

class Masker:
    def __init__(self):
        # Create model object in inference mode.
        model = modellib.MaskRCNN(mode="inference",
                                  model_dir='.', config=config)
        model.load_weights('mask_rcnn_coco.h5', by_name=True)

        self.model = model

        # COCO Class names
        # Index of the class in the list is its ID. For example, to get ID of
        # the teddy bear class, use: class_names.index('teddy bear')

        self.class_labels = [
            'BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane',
            'bus', 'train', 'truck', 'boat', 'traffic light',
            'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird',
            'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear',
            'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie',
            'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
            'kite', 'baseball bat', 'baseball glove', 'skateboard',
            'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
            'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
            'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
            'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed',
            'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote',
            'keyboard', 'cell phone', 'microwave', 'oven', 'toaster',
            'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
            'teddy bear', 'hair drier', 'toothbrush']


    def __call__(self, img):

        if isinstance(img, str):
            img = skimage.io.imread(img)

        res = self.model.detect([img], verbose=0)[0]

        res['class_labels'] = [
            self.class_labels[k] for k in res['class_ids']]

        return res

    #for i in results['class_ids']:
    #    print(f"Found a {class_names[i]}")
    #r = results
    #visualize.display_instances(
    #image, r['rois'], r['masks'], r['class_ids'], 
    #class_names, r['scores'])
    #with h5py.File(f_mask, 'w') as h5:
    #    h5['class_ids'] = r['class_ids']
    #    h5['rois'] = r['rois']
    #    h5['scores'] = r['scores']
    #    h5['masks'] = r['masks']
    
