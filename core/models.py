from django.db import models
import uuid

# Create your models here.

def video_upload_to(instance, filename):
    # Define the upload path for the video file
    return f'videos/{instance.id}/{filename}'

class Videos(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    youtube_link = models.URLField()
    video_name = models.CharField(max_length=255, blank=True)
    video_file = models.FileField()

    def __str__(self):
        return self.video_file.name

def audio_upload_to(instance, filename):
    # Define the upload path for the audio file
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

def screenshot_upload_to(instance, timestamp):
    
    #Define the upload path for the screenshot file
    return f'screenshots/{instance.screenshot_id}/{timestamp}'

class Screenshots(models.Model):
    video = models.ManyToManyField(Videos)
    screenshot_id = models.CharField(max_length=36, editable=False)
    screenshot = models.ImageField(upload_to=screenshot_upload_to)
    timestamp = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.screenshot.name
    

class Paragraphs(models.Model):
    video = models.ManyToManyField(Videos)
    article = models.TextField()

    def __str__(self):
        return f"Paragraphs for {', '.join(str(video) for video in self.video.all())}"
