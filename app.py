import streamlit as st
import os
import subprocess
from moviepy.editor import VideoFileClip


def run_main():
    subprocess.run(["python", "main.py", "ai.txt"])

def main():
    st.title("Video Generation App")
    start_button = st.button("Start Video Generation")
    if start_button:
        
        video_path ="video_path.txt"
        with open(video_path, "r") as f:
            video_path = f.read().strip()
        if os.path.exists(video_path):  # Path to save the converted .mp4 file
            st.video(video_path)
        else:
            st.write("Video file not found.")

if __name__ == "__main__":
    main()
