from django.core.files.base import ContentFile

from .models import Audios, Videos

import moviepy.editor as mp
import tempfile


class AudioProcessor:
    def __init__(self, video_path, video_id):
        self.video_path = video_path
        self.video_id = video_id

    def process_audio(self):
        # Загрузить видео из файла
        video = mp.VideoFileClip(self.video_path)

        # Извлечь аудио из видео
        audio = video.audio

        # Сохранить аудиофайл в базе данных
        with tempfile.NamedTemporaryFile(suffix='.wav') as temp_audio:
            # Записать аудиофайл во временный файл
            audio.write_audiofile(temp_audio.name)

            # Открыть временный файл аудио для чтения в двоичном режиме
            audio_file = open(temp_audio.name, 'rb')
            # Использовать video_id в качестве имени аудиофайла
            audio_name = f"output_audio.wav"

            # Получить экземпляр видео из базы данных
            video_instance = Videos.objects.get(id=self.video_id)

            # Создать экземпляр аудио с указанием видео в качестве внешнего ключа
            audio_instance = Audios(
                video=video_instance, audio_id=self.video_id)

            # Сохранить файл аудио в поле audio_file модели Audios
            audio_instance.audio_file.save(
                audio_name, ContentFile(audio_file.read()))

            # Сохранить экземпляр аудио
            audio_instance.save()
