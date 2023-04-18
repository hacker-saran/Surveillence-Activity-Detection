from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_protect
from keras.models import load_model
from collections import deque
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
import random
from keras.models import load_model
from collections import deque
from django.core.files.storage import default_storage

@csrf_protect
def video(request):
    if request.method=="POST":
        
        video = (request.FILES['upload'])
        #  Saving POST'ed file to storage
        file = video
        file_name = default_storage.save(file.name, file)

        #  Reading file from storage
        file = default_storage.open(file_name)
        file_url = default_storage.url(file_name)
        j = random.randint(1,10)
        j1 = j*11
        from datetime import datetime
        print("welcome to survillence detection system")
        print("enter the video:")

        #vpath = input("video file:")
        vpath='http://127.0.0.1:8000'+file_url


def print_results(video, limit=None):
        #fig=plt.figure(figsize=(16, 30))
        if not os.path.exists('output'):
            os.mkdir('output')

        print("Loading model ...")
        model = load_model('D:\surveillence-activity-detection-u1\model-1 (3).h5')
        Q = deque(maxlen=128)
        vs = cv2.VideoCapture(video)
        writer = None
        (W, H) = (None, None)
        count = 0     
        while True:
            # read the next frame from the file
            (grabbed, frame) = vs.read()

            # if the frame was not grabbed, then we have reached the end
            # of the stream
            if not grabbed:
                break
            
            # if the frame dimensions are empty, grab them
            if W is None or H is None:
                (H, W) = frame.shape[:2]

            # clone the output frame, then convert it from BGR to RGB
            # ordering, resize the frame to a fixed 128x128, and then
            # perform mean subtraction

            
            output = frame.copy()
           
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (128, 128)).astype("float32")
            frame = frame.reshape(128, 128, 3) / 255

            # make predictions on the frame and then update the predictions
            # queue
            preds = model.predict(np.expand_dims(frame, axis=0))[0]
#             print("preds",preds)
            Q.append(preds)

            # perform prediction averaging over the current history of
            # previous predictions
            results = np.array(Q).mean(axis=0)
            i = (preds > 0.50)[0]
            label = i

            text_color = (0, 255, 0) # default : green

            if label: # Violence prob
                text_color = (0, 0, 255) # red

            else:
                text_color = (0, 255, 0)

            text = "Violence: {}".format(label)
            FONT = cv2.FONT_HERSHEY_SIMPLEX 

            cv2.putText(output, text, (35, 50), FONT,1.25, text_color, 3) 

            # check if the video writer is None
            if writer is None:
                # initialize our video writer
                fourcc = cv2.VideoWriter_fourcc(*"MJPG")
                writer = cv2.VideoWriter("output/v_output.avi", fourcc, 30,(W, H), True)

            # write the output frame to disk
            writer.write(output)

            # show the output image
            cv2.imshow("Output", output)
            key = cv2.waitKey(1) & 0xFF

            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break
        # release the file pointersq
        print("[INFO] cleaning up...")
        writer.release()
        vs.release()
        V_path = "D:\DVE videos\1 Pulling from oven.mp4"
# NV_path = "video/non_violence/NV_25.mp4"
        print_results(V_path)
        return redirect('output_vids',f1=V_path)
        
        return render(request,'video.html')

def output(request,f1,f2):
    
    f1="video/"+f1
    f2="video/"+f2
    return render(request,'output.html',context={'file1':f1,'file2':f2})