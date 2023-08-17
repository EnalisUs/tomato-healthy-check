import cv2
import numpy as np
import tensorflow as tf
import streamlit as st
from PIL import Image
import os
import matplotlib
def load_images_from_boxes(boxes,index,image):
        # empty batches
        batches = None
        for i in index:
                item = load_image_object_detection(boxes[i],image)
                if item is not None:
                        batch = np.array(item,dtype=np.float32)
                # add new item
                        try:
                                batches = np.vstack((batches,batch))
                        except:
                                batches = batch
        return batches
def save_image_from_boxes(boxes,index,image):
        # delete existing image from detect folder
        images = os.listdir("./detected")
        for i in images:
                os.remove('./detected/' + str(i))
        #save item to file

        for i in index:
                item = load_image(boxes[i],image)
                
                if item is not None:
                        cv2.imwrite("./detected/" + str(i) + ".jpg",item)
        
def predictions_batchs_object_detection(model,batches):
        prediction = model.predict(batches)
        class_id = prediction.argmax(axis=1)
        probability = prediction.max(axis=1)
        return class_id,probability
def get_number_from_class(class_id,labels):
        # return text number of instance from each class
        unique, counts = np.unique(class_id, return_counts=True)
        counts = dict(zip(unique, counts))
        return counts
def load_image_object_detection(box,image):
        # extract bounding box
        x,y,w,h = box
        if(x < 0):
                x = 0
        if(y < 0):
                y = 0
        # crop the image
        crop_image = image[y:y+h,x:x+w]
        # resize the image
        im_rgb = cv2.cvtColor(crop_image, cv2.COLOR_BGR2RGB)
        resize_image = cv2.resize(crop_image,(224,224))
        # convert image into array 3 dimension
        x = np.array(resize_image,dtype=np.float32)
        x = np.expand_dims(x,axis=0)
        x = tf.keras.applications.mobilenet_v3.preprocess_input(x)
        return x
def load_image(box,image):
        # extract bounding box
        x,y,w,h = box
        if(x < 0):
                x = 0
        if(y < 0):
                y = 0
        # crop the image
        crop_image = image[y:y+h,x:x+w]
        # resize the image
        im_rgb = cv2.cvtColor(crop_image, cv2.COLOR_BGR2RGB)
        resize_image = cv2.resize(im_rgb,(224,224))
        return resize_image
def predictions_classification(model,image):
        prediction = model.predict(image)
        class_id = prediction.argmax()
        probability = prediction.max()
        return class_id,probability
def load_mobiletnets_model():
        model = tf.keras.models.load_model('./models/mbv3.h5',compile=False)
        model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])
        return model
def sum_value(counts):
        sum = 0
        for key,value in counts.items():
                sum += value
        return sum
def write_count_from_label(counts,labels):
        for key,value in counts.items():
                st.write('Number of {} is: '.format(labels[key]),value)

def grad_model():
        model = load_mobiletnets_model()
        model.layers[-1].activation = None
        return model

def get_heatmap(vectorized_image, model, pred_index=None):
    '''
    Function to visualize grad-cam heatmaps
    '''
    IMG_SIZE = (224, 224)
    last_conv_layer = "Conv_1"
    gradient_model = tf.keras.models.Model(
        [model.inputs], [model.get_layer(last_conv_layer).output, model.output]
    )
    
    # Gradient Computations
    with tf.GradientTape() as tape:
        last_conv_layer_output, preds = gradient_model(vectorized_image)
        if pred_index is None:
            pred_index = tf.argmax(preds[0])
        print(pred_index)
        class_channel = preds[:, pred_index]

    grads = tape.gradient(class_channel, last_conv_layer_output)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    last_conv_layer_output = last_conv_layer_output[0]
    heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)
    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap) # Normalize the heatmap
    return heatmap

def superimpose_gradcam(img_path, heatmap, output_path=None,csv_path=None,alpha=0.4):
    '''
    Superimpose Grad-CAM Heatmap on image
    '''
    img = tf.keras.utils.load_img(img_path)
    img = tf.keras.utils.img_to_array(img)


    heatmap = np.uint8(255*heatmap) # Back scaling to 0-255 from 0 - 1
    jet = matplotlib.cm.get_cmap("jet") # Colorizing heatmap
    jet_colors = jet(np.arange(256))[:, :3] # Using RGB values
    jet_heatmap = jet_colors[heatmap]
    jet_heatmap = tf.keras.utils.array_to_img(jet_heatmap)
    jet_heatmap = jet_heatmap.resize((img.shape[1], img.shape[0]))
    jet_heatmap = tf.keras.utils.img_to_array(jet_heatmap)


    superimposed_img = jet_heatmap + img # Superimposing the heatmap on original image
    superimposed_img = tf.keras.utils.array_to_img(superimposed_img)
    superimposed_img.save(output_path) # Saving the superimposed image
    img = cv2.imread(output_path)
def save_image_gradient():
        # image in detected folder by os and ls object without using name
        images = os.listdir("./detected")
        cols = st.columns(len(images))
        ind = 0
        grad_images = os.listdir("./gradcam")
        for img in grad_images:
                os.remove('./gradcam/'+str(img))
        for i in images:
                image = tf.keras.utils.load_img("./detected/" + str(i), target_size=(224, 224))
                x = tf.keras.utils.img_to_array(image)
                x = np.expand_dims(x, axis=0)
                x = tf.keras.applications.mobilenet_v2.preprocess_input(x)
                model = grad_model()
                heatmap = get_heatmap(x, model)
                output_path = "./gradcam/" + str(i)
                superimpose_gradcam("./detected/" + str(i), heatmap, output_path=output_path,csv_path=None,alpha=0.4)
                with cols[ind]:
                        st.image(output_path,use_column_width=True)
                ind += 1
