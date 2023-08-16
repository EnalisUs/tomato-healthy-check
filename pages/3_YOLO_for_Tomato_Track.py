import cv2
import streamlit as st
from PIL import Image
from yolo_track_SORT import YOLO_TRACK  # Import your YOLO_Pred class
import numpy as np
import base64
import subprocess
import os
import streamlit.components.v1 as components
with st.spinner('Please wait while your model is loading'):
    yolo_pred = YOLO_TRACK(onnx_model='./models/v5.onnx',
                    data_yaml='./models/data.yaml')
video_data = st.file_uploader("Upload file", ['mp4','mov', 'avi'])

temp_file_to_save = './temp_file_1.mp4'

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
    st.title("Tracking and Counting Tomatoes")
    st.write("Upload a video file for tracking and counting.")
    if video_data:
    # save uploaded video to disc
        write_bytesio_to_file(temp_file_to_save, video_data)
        # tfile = tempfile.NamedTemporaryFile(delete=False) 
        # tfile.write(video_data.read())
        # read it with cv2.VideoCapture(), 
        # so now we can process it with OpenCV functions
        cap = cv2.VideoCapture(temp_file_to_save)
        stframe = st.empty()

    # grab some parameters of video to use them for writing a new, processed video
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_fps = 30  ##<< No need for an int
        st.write(width, height, frame_fps)
    
        # specify a writer to write a processed video to a disk frame by frame
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        
        output_file = "output.mp4"
        writer = cv2.VideoWriter(output_file, fourcc, frame_fps, (width, height))
        col1 , col2 = st.columns(2)
        
        with col1:
            st.info('Preview of Image')
            st.video(temp_file_to_save,format='video/mp4',start_time=0)
            
        with col2:
            button = st.button('Get Detection from YOLO')
            if button:
                with st.spinner('Please regconition objects in video'):
                    totalCount = []
                    while cap.isOpened():
                        ret,frame = cap.read()
                        # Perform object detection and classification
                        if not ret:
                            break
                        if frame.any():

                            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                            image_array = np.array(rgb_frame)

                            output_frame, totalCount = yolo_pred.predictions(image_array,totalCount)
                            
                            # Write the frame to the video writer
                            writer.write(np.uint8(np.array(output_frame)[:,:,::-1]))

                writer.release()

                st.success(f"Output video saved as {output_file}")
                with open(output_file, 'rb') as f:
                    data = f.read()
                    bin_str = base64.b64encode(data).decode()
                    href = f'<a style="text-decoration:none;color:#FAFAFA;" href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(output_file)}">Download</a>'
                components.html(href)
if __name__ == "__main__":
    main()
