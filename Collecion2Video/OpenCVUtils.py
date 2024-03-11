import cv2
import math
import os
import numpy as np
from PIL import Image

def add_transitions(images):
    # Get dimensions of the images
    # height, width, _ = images[0].shape

    resultFrames = [images[0]]

    for i in range(1, len(images) - 1):
        # Add transition frames
        transition_frames = 60
        for j in range(transition_frames + 1):
            alpha = j / transition_frames
            beta = 1 - alpha
            transition_frame = cv2.addWeighted(images[i-1][len(images[i-1]) - 1], alpha, images[i][0], beta, 0)
            resultFrames.append(transition_frame)

    # Add videos
    resultFrames.append(images[i])
    
    return resultFrames

def read_video_frames(video_path):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Check if the video file is opened successfully
    if not cap.isOpened():
        print("Error: Couldn't open the video file")
        return None

    frames = []

    # Read frames until the video ends
    while True:
        # Read a frame from the video
        ret, frame = cap.read()

        # Check if the frame is successfully read
        if not ret:
            break

        # Append the frame to the frames array
        frames.append(frame)

    # Release the VideoCapture object
    cap.release()

    return frames

def Img2Array(image):
    return np.array(image)

def Array2Img(np_array):
    return Image.fromarray(np.uint8(np_array))

def list_filenames(directory):
    try:
        # Get the list of all files in the directory
        files = os.listdir(directory)
        
        # Filter out directories from the list
        files = [file for file in files if os.path.isfile(os.path.join(directory, file))]
        
        return files
    except Exception as e:
        print(f"Error: {e}")
        return None

def list_MP4(directory):
    return [filename for filename in os.listdir(directory) if filename.endswith('.mp4')]

if __name__ == "__main__":
    source_directory = "./source/"
    output_video_path = "test.mp4"

    FPS = None
    # Read images
    filenames = list_filenames(source_directory)
    
    # Define codec and VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = None

    all_frames = []

    for video_path in filenames:
        frames = []
        # Open the video file
        cap = cv2.VideoCapture(source_directory + video_path)

        # Check if the video file is opened successfully
        if not cap.isOpened():
            print("Error: Couldn't open the video file", source_directory + video_path)
            continue

        # If output video is not initialized yet, initialize it using first video's parameters
        if out is None:
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            FPS = fps
            out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

        # Read and write frames to the output video
        while True:
            ret, frame = cap.read()

            if not ret:
                break

            frames.append(frame)

        # Release the VideoCapture object
        cap.release()
        all_frames.append(frames)

    for i in range(len(all_frames) - 1):
        # Add Transitions
        if i > 0:
            local_FPS = math.floor(FPS * 0.5)
            for j in range(local_FPS):
                alpha = j / local_FPS
                beta = 1 - alpha
                transition_frame = cv2.addWeighted(all_frames[i][0], alpha, all_frames[i-1][len(all_frames[i])-1], beta, 0)
                out.write(transition_frame)
    
        for j in range(len(all_frames[i])):
            # drop the first frame to get better experience
            if j == 0 or j == len(all_frames[i]) - 1:
                continue
            out.write(all_frames[i][j])

    out.release()