from django.db import models
from django.conf import settings

import uuid
import os

# Определение пути загрузки видеофайла
def video_upload_to(instance, filename):
    return f'videos/{instance.id}/{filename}'


class Videos(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    youtube_link = models.URLField()
    video_name = models.CharField(max_length=255, blank=True)
    video_file = models.FileField(upload_to=video_upload_to)

    def __str__(self):
        return self.video_file.name

# Определение пути загрузки аудиофайла
def audio_upload_to(instance, filename):
    return f'audio/{instance.audio_id}/{filename}'


class Audios(models.Model):
    video = models.ForeignKey('Videos', on_delete=models.CASCADE)
    audio_id = models.CharField(max_length=36, editable=False)
    audio_file = models.FileField(upload_to=audio_upload_to)

    def __str__(self):
        return self.audio_file.name

    def get_audio_path(self):
        audio_instance = Audios.objects.get(video=self.video_id)
        audio_path = audio_instance.audio_file.path
        return audio_path

# Определение пути загрузки файлов скриншотов
def screenshot_upload_to(instance, timestamp):
    return f'screenshots/{instance.screenshot_id}/{timestamp}'


class Screenshots(models.Model):
    video = models.ManyToManyField(Videos)
    screenshot_id = models.CharField(max_length=36, editable=False)
    screenshot = models.ImageField(upload_to=screenshot_upload_to)
    timestamp = models.PositiveIntegerField(default=0)
    group = models.PositiveIntegerField(default=0)
    red_square = models.BooleanField(default=False)

    def __str__(self):
        return self.screenshot.name

    def delete(self, *args, **kwargs):
        # Удаление связанного медиафайла
        file_path = os.path.join(settings.MEDIA_ROOT, str(self.screenshot))
        if os.path.exists(file_path):
            os.remove(file_path)

        # Вызов метода delete() родительского класса для удаления записи из базы данных
        super().delete(*args, **kwargs)


class Paragraphs(models.Model):
    video = models.ManyToManyField(Videos)
    article = models.TextField()
    len_article = models.PositiveIntegerField(default=0)
    timestamp = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Абзацы для {', '.join(str(video) for video in self.video.all())}"

# Определение пути загрузки файлов статей
def article_upload_to(instance, filename):
    return f'article/{instance.article_id}/{filename}'


class Articles(models.Model):
    video = models.ForeignKey('Videos', on_delete=models.CASCADE)
    article_id = models.CharField(max_length=36, editable=False)
    article_file = models.FileField(upload_to=article_upload_to)
