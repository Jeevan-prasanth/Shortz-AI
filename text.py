from pydub import AudioSegment
import subprocess
import math
import cv2
import os
from moviepy.editor import AudioFileClip


offset = 50


def get_audio_duration(audio_file):
    clip = AudioFileClip(audio_file)
    duration = clip.duration * 1000  # Convert duration to milliseconds
    clip.close()
    return int(duration)


def write_text(text, frame, video_writer):
    font = cv2.FONT_HERSHEY_SIMPLEX
    white_color = (255, 255, 255)
    black_color = (0, 0, 0)
    thickness = 10
    font_scale = 3
    border = 5

    # Calculate the position for centered text
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    text_x = (frame.shape[1] - text_size[0]) // 2  # Center horizontally
    text_y = (frame.shape[0] + text_size[1]) // 2  # Center vertically
    org = (text_x, text_y)  # Position of the text

    frame = cv2.putText(
        frame,
        text,
        org,
        font,
        font_scale,
        black_color,
        thickness + border * 2,
        cv2.LINE_AA,
    )
    frame = cv2.putText(
        frame, text, org, font, font_scale, white_color, thickness, cv2.LINE_AA
    )

    video_writer.write(frame)


# from moviepy.editor import VideoFileClip, concatenate_audioclips


from moviepy.editor import VideoFileClip, concatenate_audioclips, TextClip


from moviepy.editor import VideoFileClip, concatenate_audioclips, TextClip


def add_narration_to_video(narrations, input_video, output_dir, output_file):
    temp_video = os.path.join(output_dir, "with_transcript.mp4")
    video_clip = VideoFileClip(input_video)

    audio_clips = []
    for i, narration in enumerate(narrations):
        audio = os.path.join(output_dir, "narrations", f"narration_{i+1}.mp3")
        audio_clip = AudioFileClip(audio)
        audio_clips.append(audio_clip)

    full_audio_clip = concatenate_audioclips(audio_clips)
    video_clip = video_clip.set_audio(full_audio_clip)

    output_path = os.path.join(output_dir, output_file)
    video_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=30)

    # Close all clips
    video_clip.close()
    full_audio_clip.close()

    # os.remove(temp_video)
