from pathlib import Path
import cv2     # for capturing videos
import math   # for mathematical operations
import matplotlib.pyplot as plt    # for plotting the images
import pandas as pd
import numpy as np
import os
import matplotlib.gridspec as gridspec
from tqdm import tqdm
import re
import glob
from convenience import is_cv3

def extract_frames(k, video_path, path_to_save, event, channel, start, stop, nframes):
    
#     m = re.search('tos/(.+?).mpg', video_path)
#     if m:
#         name = m.group(1)
#     name = name.replace('/','__')   
#     path_to_save = path_to_save + name + '__' + str(int(start))
#     if not os.path.exists(path_to_save):
#         os.mkdir(path_to_save)

    path_to_save = path_to_save + '/'
    path_to_save = path_to_save + event + '_event'+'{:03d}'.format(k)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error opening video")
        
#     if (stop == None) and (nframes == None):
#         stop = start + (1/cap.get(cv2.CAP_PROP_FPS))*1000
#     elif (nframes != None):
#         stop = start + (nframes*1/cap.get(cv2.CAP_PROP_FPS))*1000
#     elif (stop != None):
#         # No need to do anything stop is already time
#         pass 
    
    #assert(stop>start), f"The end time for video {video_path} provided is before the start time {start}, {stop}"
    assert(stop<(1000*cap.get(cv2.CAP_PROP_FRAME_COUNT)*cap.get(cv2.CAP_PROP_FPS))), "stop greater than video end"
    
    cap.set(cv2.CAP_PROP_POS_MSEC, stop)
    stop_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
    cap.set(cv2.CAP_PROP_POS_MSEC, start)
    start_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
    frames = np.linspace(start_frame, stop_frame, nframes)
    #print(start_frame)
    #print(stop_frame)
    #print('YO!!!')
    if len(frames)>400:
        times = len(frames)/400
        frames = frames[int(times/2)*400 : (int(times/2)+1)*400]
    for j in range(len(frames)):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(frames[j]))
        suc,im = cap.read()
        cv2.imwrite(path_to_save + '_channel' + str(channel) + '_frame' + '{:06d}'.format(j) + '.png', im)