import cv2
import streamlit as st
from PIL import Image
from yolo_predictions import YOLO_Pred  # Import your YOLO_Pred class
import numpy as np
import base64
import os
import datetime

import streamlit.components.v1 as components

with st.spinner('Please wait while your model is loading'):
    yolo_pred = YOLO_Pred(onnx_model='./models/v5.onnx',
                    data_yaml='./models/data.yaml')
video_data = st.file_uploader("Upload file", ['mp4','mov', 'avi'])

temp_file_to_save = './temp_file_1.mp4'
temp_file_result  = './temp_file_2.mp4'

# func to save BytesIO on a drive
def write_bytesio_to_file(filename, bytesio):
    """
    Write the contents of the given BytesIO to a file.
    Creates the file or overwrites the file if it does
    not exist yet. 
    """
    with open(filename, "wb") as outfile:
        # Copy the BytesIO stream to the output file
        outfile.write(bytesio.getbuffer())


    
def main():
    st.title("Object Detection and Classification")
    st.write("Upload a video file for object detection and classification.")
    if video_data:
    # save uploaded video to disc
        write_bytesio_to_file(temp_file_to_save, video_data)

        # read it with cv2.VideoCapture(), 
        # so now we can process it with OpenCV functions
        cap = cv2.VideoCapture(temp_file_to_save)

    # grab some parameters of video to use them for writing a new, processed video
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_fps = int(cap.get(cv2.CAP_PROP_FPS))  ##<< No need for an int
        st.write(width, height, frame_fps)
    
        # specify a writer to write a processed video to a disk frame by frame
        fourcc_h264 = cv2.VideoWriter_fourcc(*'H264')
        out_mp4 = cv2.VideoWriter(temp_file_result, fourcc_h264, frame_fps, (width, height),isColor = False)
        
        output_file = 'output.mp4'
        print(output_file)
        writer = cv2.VideoWriter(output_file, fourcc_h264, frame_fps, (width, height))
        col1 , col2 = st.columns(2)
        
        with col1:
            st.info('Preview of Video')
            st.video(temp_file_to_save)
            
        with col2:
            button = st.button('Get Detection from YOLO')
            if button:
                with st.spinner('Please regconition objects in video'):
                    while True:
                        ret,frame = cap.read()
                        # Perform object detection and classification
                        if not ret:
                            break
                        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                        image_array = np.array(rgb_frame)

                        output_frame, number = yolo_pred.predictions(image_array,show_class=True)
                        
                        # Write the frame to the video writer
                        writer.write(np.uint8(np.array(output_frame)[:,:,::-1]))

                writer.release()

                st.success(f"Output video saved as {output_file}")
                with open(output_file, 'rb') as f:
                    data = f.read()
                    bin_str = base64.b64encode(data).decode()
                    href = f'<a style="text-decoration:none;color:#FAFAFA;padding:12px 16px;background-color:#fcfcfc" href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(output_file)}">Download</a>'
                components.html(href)
if __name__ == "__main__":
    main()
