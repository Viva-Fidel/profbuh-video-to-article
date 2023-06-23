from celery import shared_task
from .video_frame_processor import VideoFrameProcessor
from .audio_extractor import AudioProcessor
from .text_extractor import TextProcessor

@shared_task
def process_video_task(video_path, video_id, focus_time):
    frame_processor = VideoFrameProcessor(video_path, video_id, focus_time)
    frame_processor.process_video()


@shared_task
def process_audio_task(self, video_path, video_id):
    audio_processor = AudioProcessor(video_path, video_id)
    audio_processor.process_audio()

@shared_task
def process_text_task(self, video_id):
    text_processor = TextProcessor(video_id)
    text_processor.process_text()