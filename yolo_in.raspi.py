from picamera.array import PiRGBArray
from picamera import PiCamera

import time
import cv2
class YOLO_Pred():
    def __init__(self,onnx_model):
        # load YAML
        self.labels = ['Tomato']
        self.nc = 1
        # load YOLO model
        self.yolo = cv2.dnn.readNetFromONNX(onnx_model)
        self.yolo.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.yolo.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
    
    def predictions(self,image,show_class=False):
        # load model h5
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
        x_factor = image_w/INPUT_WH_YOLO
        y_factor = image_h/INPUT_WH_YOLO

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
        classes_np = np.array(classes).tolist()
        # NMS
        index = np.array(cv2.dnn.NMSBoxes(boxes_np,confidences_np,0.5,0.5)).flatten()
        # box list from index
        number = []
        
        # Draw the Bounding
        for ind in index:
            # extract bounding box
            x,y,w,h = boxes_np[ind]

            bb_conf = int(confidence[ind]*100)
            
            classes_id = classes_np[ind]
            
            class_name = self.labels[classes_id]

            colors = self.generate_colors(classes_id)

            text = f'{class_name}: {bb_conf}%'

            cv2.rectangle(image,(x,y),(x+w,y+h),colors,2)
            
            if show_class:
                cv2.rectangle(image,(x,y-30),(x+w,y),colors,-1)
                cv2.putText(image,text,(x,y-10),cv2.FONT_HERSHEY_PLAIN,0.7,(0,0,0),1)
        
        return image
    
    
    def generate_colors(self,ID):
        np.random.seed(42)
        colors = np.random.randint(100,255,size=(self.nc,3)).tolist()
        return tuple(colors[ID])
        
yolo_pred = YOLO_Pred(onnx_model='./v5.onnx')     
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
# allow the camera to warmup
time.sleep(0.1)
# capture frames from the camera
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image
    image = frame.array
    image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    image_array = np.array(image)
    # show the frame
    image = yolo_pred.predictions(image_array)
    pred_img_obj = Image.fromarray(pred_img)
    cv2.imshow("Frame", pred_img_obj)
    key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)
    if key == ord("q"):
        break