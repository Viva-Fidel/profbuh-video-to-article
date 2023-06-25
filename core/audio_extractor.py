from .models import Audios, Videos
from django.core.files.base import ContentFile

import moviepy.editor as mp
import tempfile

class AudioProcessor:
    def __init__(self, video_path, video_id):
        self.video_path = video_path
        self.video_id = video_id
        # self.skip_time = 5

    def process_audio(self):
        video = mp.VideoFileClip(self.video_path)
        # video = video.subclip(self.skip_time)
        audio = video.audio

       # Save the audio file in the database
        with tempfile.NamedTemporaryFile(suffix='.wav') as temp_audio:
            audio.write_audiofile(temp_audio.name)

            audio_file = open(temp_audio.name, 'rb')
            audio_name = f"output_audio.wav"  # Use the video_id as the audio file name

            video_instance = Videos.objects.get(id=self.video_id)
            audio_instance = Audios(video=video_instance, audio_id=self.video_id)  # Set video instance as the foreign key
            audio_instance.audio_file.save(audio_name, ContentFile(audio_file.read()))
            audio_instance.save()

