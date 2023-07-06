from django.shortcuts import render
from .models import Videos, Articles

from .tasks import process_video_task, process_video_screenshots, process_audio_task, process_text_task, send_request_task

import os
from pytube import YouTube
from celery import chain
from moviepy.editor import VideoFileClip
from django.http import FileResponse


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
        time_no_limit = request.POST.get('time_no_limit')
        annotation_length = request.POST.get('annotation_length')
        annotation_no_limit = request.POST.get('annotation_no_limit')
        article_legth = request.POST.get('article_legth')
        article_no_limit = request.POST.get('article_no_limit')
        focus_time = request.POST.get('focus_time')

        video = YouTube(youtube_link)

        input_path = os.path.join('media/videos/', f'{video.video_id}.mp4')
        video.streams.get_highest_resolution().download(filename=input_path)

        if time_no_limit != "on":
            try:
                start_time = int(start_time)
            except:
                start_time = 0
            try:
                end_time = int(end_time)
            except:
                end_time = get_video_duration(input_path)

            if start_time != 0 and end_time != 0:
                output_path = os.path.join(
                    'media/videos/', f'{video.video_id}_partial.mp4')
                extract_video_segment(
                    input_path, output_path, start_time, end_time)
            elif start_time != 0:
                end_time = video.length
                output_path = os.path.join(
                    'media/videos/', f'{video.video_id}_partial.mp4')
                extract_video_segment(
                    input_path, output_path, start_time, end_time)
            elif end_time != 0:
                output_path = os.path.join(
                    'media/videos/', f'{video.video_id}_partial.mp4')
                extract_video_segment(input_path, output_path, None, end_time)
        else:
            output_path = input_path

        video_model = Videos(youtube_link=youtube_link,
                             video_name=video.title, video_file=output_path)
        video_model.save()

        video_id = video_model.id

        if article_no_limit == "on":
            article_legth = "Безгранично"

        if annotation_no_limit == "on":
            annotation_length = "Безгранично"

        task_chain = chain(
            process_video_task.s(output_path, video_id),
            process_video_screenshots.s(video_id, int(focus_time)),
            process_audio_task.s(output_path, video_id),
            process_text_task.s(video_id),
            send_request_task.s(video_id, article_legth, annotation_length, focus_time),
        )
        task_result = task_chain.delay()
        result = task_result.get()


        video = Videos.objects.get(id=video_id)
        article = Articles.objects.get(video=video)
        article_file = article.article_file

        # Open the file in binary mode
        file = open(article_file.path, 'rb')

        # Create a FileResponse with the file
        response = FileResponse(file)

        # Set the content type and filename for the response
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = f'attachment; filename="output.docx"'

        return response

    return render(request, 'core/index.html')
