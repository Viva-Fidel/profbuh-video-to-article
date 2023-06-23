from django.shortcuts import render
from .models import Videos

from .tasks import process_video_task, process_audio_task, process_text_task

import os
from pytube import YouTube
from celery import chain
from moviepy.editor import VideoFileClip

# Create your views here.
def index(request):

    return render(request, 'core/index.html')

def convert_time_to_seconds(time_str):
    parts = time_str.split(':')
    hours, minutes, seconds = map(int, parts)
    total_seconds = hours * 3600 + minutes * 60 + seconds
   
    return total_seconds

def extract_video_segment(input_path, output_path, start_time, end_time):
    clip = VideoFileClip(input_path).subclip(start_time, end_time)
    clip.write_videofile(output_path, codec='libx264')
    os.remove(input_path)

def get_video_duration(video_path):
    clip = VideoFileClip(video_path)
    duration = clip.duration
    clip.close()
    return duration

def save_video(request):

    if request.method == 'POST':
        youtube_link = request.POST.get('youtube-link')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        focus_time = request.POST.get('focus_time')


        video = YouTube(youtube_link)

        # Set the start and end times in seconds
        #start_time = convert_time_to_seconds(start_time)
        #end_time = convert_time_to_seconds(end_time)
        
        start_time = int(start_time)
        end_time = int(end_time)


        # Download the video
        input_path = os.path.join('media/videos/', f'{video.video_id}.mp4')
        video.streams.get_highest_resolution().download(filename=input_path)

        if start_time != 0 and end_time != 0:
           # User provided both start and end time
            output_path = os.path.join('media/videos/', f'{video.video_id}_partial.mp4')
            extract_video_segment(input_path, output_path, start_time, end_time)
        elif start_time != 0:
            end_time  = video.length
            # User provided only the start time
            output_path = os.path.join('media/videos/', f'{video.video_id}_partial.mp4')
            extract_video_segment(input_path, output_path, start_time, end_time)
        elif end_time != 0:
            # User provided only the end time
            output_path = os.path.join('media/videos/', f'{video.video_id}_partial.mp4')
            extract_video_segment(input_path, output_path, None, end_time)
        else:
            # User didn't provide any start or end time, use the original video
            output_path = input_path
        # Save the Video model
        video_model = Videos(youtube_link=youtube_link, video_name=video.title, video_file=output_path)
        video_model.save()

        video_id = video_model.id

        task_chain = chain(
        process_video_task.s(output_path, video_id, focus_time),
        process_audio_task.s(output_path, video_id),
        process_text_task.s(video_id),
        )
        task_chain.delay()

        return render(request, 'core/index.html')
    
    return render(request, 'core/index.html')