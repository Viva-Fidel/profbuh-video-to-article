import logging
import subprocess
from .models import Audios, Screenshots, Paragraphs, Videos
import json
from torch import package

from vosk import KaldiRecognizer, Model

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class TextProcessor:
    def __init__(self, video_id):
        self.model = Model('models/vosk-model-ru-0.42')
        self.video_id = video_id
    

    def split_to_paragraphs(self, data):

        paragraph_times = []

        screenshots_time = Screenshots.objects.filter(video__id=self.video_id).order_by('timestamp')

        for timestamp in screenshots_time:
            paragraph_times.append(timestamp.timestamp)

        
        # Create an empty list for each start_time
         
        paragraphs = [[] for _ in range(len(paragraph_times))]
        i = 0
        
        # Iterate over each object in the 'result' array
        for obj in data['result']:
            start = obj['start']
            # print(paragraphs)
            if start < 5:
                pass
            elif start < paragraph_times[i]:
                paragraphs[i].append(obj['word'])
                
            elif i == len(paragraph_times)-1:
                paragraphs[i].append(obj['word'])
            
            elif i < len(paragraph_times)-1:
                i += 1
                paragraphs[i].append(obj['word'])

    
        return paragraphs
    
    def apply_te(self, text, model, lan='ru'):
        return model.enhance_text(text, lan)

    def set_punctuation(self, data):
        imp = package.PackageImporter('models/silero/v2_4lang_q.pt')
        model = imp.load_pickle("te_model", "model")

        current_video = Videos.objects.get(id=self.video_id)
        
        for lists in data:
            input_text = ' '.join(lists)
            processed_text = self.apply_te(input_text, model, lan='ru')
            paragraph = Paragraphs(article=processed_text)
            paragraph.save()
            paragraph.video.add(current_video)  # Associate the text with the video


    # Convert audio to text
    def process_text(self):
        audio_instance = Audios.objects.get(video__id=self.video_id)
        audio_path = audio_instance.audio_file.path
        recognizer = KaldiRecognizer(self.model, 16000)
        recognizer.SetWords(True)
    
        process = subprocess.Popen(['ffmpeg', '-loglevel', 'quiet', '-i', audio_path, '-ar', '16000', '-ac', '1', '-f', 's16le', '-'],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
    
        stdout, _ = process.communicate()  # Wait for ffmpeg process to finish and capture the stdout
    
        recognizer.AcceptWaveform(stdout)
        result = recognizer.FinalResult()
        result = json.loads(result)

        result = self.split_to_paragraphs(result)
        self.set_punctuation(result)
        
