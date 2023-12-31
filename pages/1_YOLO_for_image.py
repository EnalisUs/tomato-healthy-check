import streamlit as st
from yolo_predictions import YOLO_Pred
from PIL import Image
import numpy as np
import classify
st.set_page_config(page_title="YOLO Object Detection",
                   layout='wide',
                   page_icon='./images/object.png')

st.header('Get Object Detection for any Image')
st.write('Please Upload Image to get detections')
with st.spinner('Please wait while your model is loading'):
    yolo = YOLO_Pred(onnx_model='./models/v5.onnx',
                    data_yaml='./models/data.yaml')
def upload_image():
    # Upload Image
    image_file = st.file_uploader(label='Upload Image')
    if image_file is not None:
        size_mb = image_file.size/(1024**2)
        file_details = {"filename":image_file.name,
                        "filetype":image_file.type,
                        "filesize": "{:,.2f} MB".format(size_mb)}
        #st.json(file_details)
        # validate file
        if file_details['filetype'] in ('image/png','image/jpeg'):
            st.success('VALID IMAGE file type (png or jpeg)')
            return {"file":image_file,
                    "details":file_details}
        
        else:
            st.error('INVALID Image file type')
            st.error('Upload only png,jpg, jpeg')
            return None
        
def main():
    object = upload_image()
    
    if object:
        prediction = False
        image_obj = Image.open(object['file'])       
        
        col1 , col2 = st.columns(2)
        col3, col4 = st.columns(2)
        with col1:
            st.info('Preview of Image')
            st.image(image_obj)
            
        with col2:
            show_class = st.checkbox('Show classes in Detection')
            if not show_class:
                show_class = False
            else:
                show_class = True
            button = st.button('Get Detection from YOLO')
            if button:
                with st.spinner("""
                Geting Objets from image. please wait
                                """):
                    # below command will convert
                    # obj to array
                    image_array = np.array(image_obj)
                    print(image_array.shape)
                    if len(image_array.shape) > 2 and image_array.shape[2] == 4:
                    #slice off the alpha channel
                        image_array = image_array[:, :, :3]
                        image_array = np.ascontiguousarray(image_array, dtype=np.uint8)
                    pred_img, number = yolo.predictions(image_array,show_class)
                    pred_img_obj = Image.fromarray(pred_img)
                    prediction = True
        if prediction:
            with col3:
                st.subheader("Predicted Image")
                st.caption("Object detection from YOLO V5 model")
                st.image(pred_img_obj)
            with col4:
                if not number:
                    st.write(':tomato: Number of Totomaes Detected: ',0)
                else:
                    st.write(':tomato: Number of Totomaes Detected: ',classify.sum_value(number))
                    st.title("Explain the region of this state:")
                    classify.write_count_from_label(number,yolo.labels)
                    
                    classify.save_image_gradient()
    
    
    
if __name__ == "__main__":
    main()
