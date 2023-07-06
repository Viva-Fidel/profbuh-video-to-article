from django.core.files.uploadedfile import InMemoryUploadedFile

from .models import Screenshots, Videos

import cv2
import io
from PIL import Image

class VideoFrameProcessor:
    def __init__(self, video_path, video_id):
        self.video_id = video_id
        self.video_path = video_path
        self.screen_time = 0

    def detect_and_capture(self, frame, timestamp):
        if timestamp - self.screen_time >= 1:
            self.screen_time = timestamp
            # Сгенерировать имя файла с помощью временного смещения (перевести в миллисекунды)
            filename = f"screenshot_{timestamp}.jpg"

            # Сохранить скриншот текущего кадра
            save_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(save_frame)
            image_buffer = io.BytesIO()
            image.save(image_buffer, format='JPEG')
            image_file = InMemoryUploadedFile(
                image_buffer,
                None,
                filename,
                'image/jpeg',
                image_buffer.tell(),
                None)
            
            # Сохранить скриншот текущего кадра
            screenshot = Screenshots.objects.create(screenshot_id=self.video_id, timestamp=timestamp)
            screenshot.screenshot.save(filename, image_file)
                
            current_video = Videos.objects.get(id=self.video_id)
            screenshot.video.add(current_video)  # Связать скриншот с видео
            screenshot.save()   

    def process_video(self):
        video_capture = cv2.VideoCapture(self.video_path)

        while True:
            ret, frame = video_capture.read()

            if not ret:
                break

            # Получить текущую метку времени
            timestamp = video_capture.get(cv2.CAP_PROP_POS_MSEC) / 1000  # Перевести в секунды

            self.detect_and_capture(frame, timestamp)

        # Освободить захват видео и закрыть окна
        video_capture.release()
