#!/usr/bin/env python
# coding: utf-8
import cv2
import numpy as np
import os
import cvzone
import yaml
from yaml.loader import SafeLoader
import tensorflow as tf
import classify
from sort import *
class YOLO_TRACK():
    def __init__(self,onnx_model,data_yaml):
        # load YAML
        with open(data_yaml,mode='r') as f:
            data_yaml = yaml.load(f,Loader=SafeLoader)

        self.labels = data_yaml['names']
        self.nc = data_yaml['nc']
        self.mobilenet_v2 = classify.load_mobiletnets_model()
        # load YOLO model
        self.yolo = cv2.dnn.readNetFromONNX(onnx_model)
        self.yolo.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.yolo.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
        # Tracking
        self.tracker = Sort(max_age=20, min_hits=3, iou_threshold=0.3)
        self.limits = []
    
    def predictions(self,image,totalCount):
        totalCount = totalCount
        row, col, d = image.shape
        
        # get the YOLO prediction from the the image
        # step-1 convert image into square image (array)
        max_rc = max(row,col)
        input_image = np.zeros((max_rc,max_rc,3),dtype=np.uint8)
        input_image[0:row,0:col] = image
        # step-2: get prediction from square array
        INPUT_WH_YOLO = 640
        blob = cv2.dnn.blobFromImage(input_image,1/255,(INPUT_WH_YOLO,INPUT_WH_YOLO),crop=False)
        self.yolo.setInput(blob)
        preds = self.yolo.forward() # detection or prediction from YOLO

        # Non Maximum Supression
        # step-1: filter detection based on confidence (0.4) and probability score (0.25)
        detections = preds[0]
        boxes = []
        confidences = []
        classes = []

        # widht and height of the image (input_image)
        image_w, image_h = input_image.shape[:2]
        self.limits = [INPUT_WH_YOLO/2,0,INPUT_WH_YOLO/2,INPUT_WH_YOLO]
        x_factor = image_w/INPUT_WH_YOLO
        y_factor = image_h/INPUT_WH_YOLO
        # draw line in center of image with w,h
        

        for i in range(len(detections)):
            row = detections[i]
            confidence = row[4] # confidence of detection an object
            if confidence > 0.5:
                class_score = row[5:].max() # maximum probability from 20 objects
                class_id = row[5:].argmax() # get the index position at which max probabilty occur

                if class_score > 0.5:
                    cx, cy, w, h = row[0:4]
                    # construct bounding from four values
                    # left, top, width and height
                    left = int((cx - 0.5*w)*x_factor)
                    top = int((cy - 0.5*h)*y_factor)
                    width = int(w*x_factor)
                    height = int(h*y_factor)
                    box = np.array([left,top,width,height])
                    # append values into the list
                    confidences.append(confidence)
                    boxes.append(box)
                    classes.append(class_id)
        # clean
        boxes_np = np.array(boxes).tolist()
        confidences_np = np.array(confidences).tolist()
        
        # NMS
        index = np.array(cv2.dnn.NMSBoxes(boxes_np,confidences_np,0.5,0.5)).flatten()

        tracks = np.empty((0, 5))
        # Draw the Bounding

        if len(index) > 0:
            batches = classify.load_images_from_boxes(boxes_np,index,input_image)
            class_id, confidence = classify.predictions_batchs_object_detection(self.mobilenet_v2,batches)
            # Draw the Bounding
            for ind in index:
                i=0
                # extract bounding box
                x,y,w,h = boxes_np[ind]
                # return to x1,y1,x2,y2
                x1,y1,x2,y2 = x,y,x+w,y+h
                bb_conf = int(confidence[i]*100)
                classes_id = class_id[i]
                i+=1
                class_name = self.labels[classes_id]
                # Tracking
                currentArray = np.array([x1,y1,x2,y2, bb_conf])
                tracks = np.vstack((tracks, currentArray))
        resultsTracker = self.tracker.update(tracks)
        #draw line center of image
        
        cv2.line(image, (int(self.limits[0]), int(self.limits[1])), (int(self.limits[2]), int(self.limits[3])), (255, 0, 0), 5)
        for result in resultsTracker:
            i = 0
            x1, y1, x2, y2, trackid = result
            
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            w, h = x2 - x1, y2 - y1
            _index = class_id[i]
            label = self.labels[_index]
            colors = self.generate_colors(classes_id)
            i+=1
            cvzone.cornerRect(image, (x1, y1, w, h), l=5, rt=2, colorR=colors)
            cvzone.putTextRect(image, f' {int(trackid)}{label}', (max(0, x1), max(35, y1)),
                            scale=2, thickness=1, offset=5)

            cx, cy = x1 + w // 2, y1 + h // 2
            cv2.circle(image, (cx, cy), 5, (0, 0, 255), cv2.FILLED)
            # check if the object is in the line
            
            if self.limits[0] - 15 < cx < self.limits[2] + 15:
                if totalCount.count(trackid) == 0:
                    totalCount.append(trackid)
                    cv2.line(image, (int(self.limits[0]), int(self.limits[1])), (int(self.limits[2]), int(self.limits[3])), (0, 255, 0), 5)


        # cvzone.putTextRect(img, f' Count: {len(totalCount)}', (50, 50))
        cv2.putText(image,str(len(totalCount)),(255,100),cv2.FONT_HERSHEY_PLAIN,5,(50,50,255),8)

        return image, totalCount
    
    
    def generate_colors(self,ID):
        np.random.seed(10)
        colors = np.random.randint(100,255,size=(self.nc,3)).tolist()
        return tuple(colors[ID])
        
        
    
    
    



