import streamlit as st 
from streamlit_webrtc import webrtc_streamer
import av
from yolo_predictions import YOLO_Pred

# load yolo model
yolo = YOLO_Pred('./models/v5.onnx',
                 './models/data.yaml')


def video_frame_callback(frame):
    img = frame.to_ndarray(format="rgb24")
    # any operation 
    #flipped = img[::-1,:,:]
    # rgb_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # image_array = np.array(rgb_frame)
    pred_img, _ = yolo.predictions(img,show_class=True)

    return av.VideoFrame.from_ndarray(pred_img, format="rgb24")


webrtc_streamer(key="example", 
                video_frame_callback=video_frame_callback,
                media_stream_constraints={"video":True,"audio":False})
