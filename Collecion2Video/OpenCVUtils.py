import cv2
import math
import os
import copy

def read_video_frames(video_path):
    frames = []
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Check if the video file is opened successfully
    if not cap.isOpened():
        print("Error: Couldn't open the video file", source_directory + video_path)
        return (False, None, None)

    # Get the video's width, height, and frames per second
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Read and store each frame in the frames list
    while True:
        ret, frame = cap.read()

        if not ret:
            break

        frames.append(frame)

    # Release the VideoCapture object
    cap.release()

    return (True, frames, {"width": width, "height": height, "fps": fps})

def load_all_videos(video_paths):
    """
    Load all videos from the given directory and return the frames and video information.

    Args:
        source_directory (str): The directory path where the videos are located.
        video_paths (list): List of video file names.

    Returns:
        tuple: A tuple containing the frames and video information.

    """
    VIDEO_INFO = None
    all_frames = []

    for video_path in video_paths:
        # Read video frames
        rst, frames, info = read_video_frames(video_path)

        if not rst:
            continue

        if VIDEO_INFO is None:
            VIDEO_INFO = info

        all_frames.append(frames)
    
    return (all_frames, VIDEO_INFO)

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

def add_transition_frames(all_frames, fps):
    result_frames = []
    for i in range(len(all_frames) - 1):
        if i > 0:
            # Add transition frames
            local_FPS = math.floor(fps * 0.7)
            transition_frames = []
            for j in range(local_FPS):
                # Calculate the alpha and beta values for blending
                alpha = j / local_FPS
                beta = 1 - alpha
                # Blend the frames using alpha and beta values
                transition_frame = cv2.addWeighted(all_frames[i][0], alpha, all_frames[i-1][len(all_frames[i])-1], beta, 0)
                transition_frames.append(transition_frame)
            
            result_frames.append(transition_frames)
        
        result_frames.append(all_frames[i])

    return result_frames

def combine_videos(video_paths, output_video_path, resize_factor=1):
    all_frames, VIDEO_INFO = load_all_videos(video_paths)

    # Define codec and VideoWriter object
    width = VIDEO_INFO["width"] * resize_factor
    height = VIDEO_INFO["height"] * resize_factor
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, VIDEO_INFO["fps"], (width, height))

    all_frames = add_transition_frames(all_frames, VIDEO_INFO["fps"])

    for frames in all_frames:
        for frame in frames:
            # Skip the first and last frame
            if frame is frames[0] or frame is frames[-1]:
                continue

            # Resize the frame to double the resolution using bicubic interpolation
            resized_frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_CUBIC)

            out.write(resized_frame)

    out.release()

if __name__ == "__main__":
    source_directory = "./source/"
    output_video_path = "test.mp4"

    Resize_Factor = 4

    # Read videos
    filenames = list_filenames(source_directory)
    video_paths = [os.path.join(source_directory, file) for file in filenames]

    # Combine videos
    combine_videos(video_paths, output_video_path, Resize_Factor)
