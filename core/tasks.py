from celery import shared_task
from .video_frame_processor import VideoFrameProcessor
from .video_frame_post_processor import VideoPostFrameProcessor
from .audio_extractor import AudioProcessor
from .text_extractor import TextProcessor
from .send_request_to_chatgpt import ArticleCreation


@shared_task
def process_video_task(video_path, video_id):
    # Создание экземпляра VideoFrameProcessor и обработка видео
    frame_processor = VideoFrameProcessor(video_path, video_id)
    frame_processor.process_video()


@shared_task
def process_video_screenshots(self, video_id, focus_time):
    # Создание экземпляра VideoPostFrameProcessor и создание скриншотов видео
    frame_post_processor = VideoPostFrameProcessor(video_id, focus_time)
    frame_post_processor.process_video_screenshots()


@shared_task
def process_audio_task(self, video_path, video_id):
    # Создание экземпляра AudioProcessor и извлечение аудио
    audio_processor = AudioProcessor(video_path, video_id)
    audio_processor.process_audio()


@shared_task
def process_text_task(self, video_id):
    # Создание экземпляра TextProcessor и извлечение текста
    text_processor = TextProcessor(video_id)
    text_processor.process_text()


@shared_task
def send_request_task(self, video_id, article_legth, annotation_length):
    # Создание экземпляра ArticleCreation и получение ответа от ChatGPT
    article_creation = ArticleCreation(
        video_id, article_legth, annotation_length)
    article_creation.get_response()
