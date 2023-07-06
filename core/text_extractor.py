from django.db.models import Max, Min

from .models import Audios, Screenshots, Paragraphs, Videos

import logging
import subprocess
import json
from torch import package
from vosk import KaldiRecognizer, Model

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


class TextProcessor:
    def __init__(self, video_id):
        # Загрузка модели распознавания речи
        self.model = Model('models/vosk-model-ru-0.42')
        self.video_id = video_id

    def split_to_paragraphs(self, data):
        # Получение группы временных меток скриншотов
        group_timestamps = Screenshots.objects.values('group').annotate(
            min_timestamp=Min('timestamp'), max_timestamp=Max('timestamp'))

        # Получение максимальной временной метки первой группы скриншотов
        first_group_max_timestamp = Screenshots.objects.filter(
            group=1).aggregate(max_timestamp=Max('timestamp'))['max_timestamp']

        paragraph_times = []

        for entry in group_timestamps:
            if entry['group'] > 1:
                paragraph_times.append(entry['min_timestamp'])

        paragraphs = [[] for _ in range(len(paragraph_times))]

        i = 0

        # Итерация по каждому объекту в массиве 'result'
        for obj in data['result']:
            start = obj['start']

            if start <= first_group_max_timestamp:
                pass
            elif start < paragraph_times[i]:
                paragraphs[i].append(obj['word'])
            elif i == len(paragraph_times) - 1:
                paragraphs[i].append(obj['word'])
            elif i < len(paragraph_times) - 1:
                i += 1
                paragraphs[i].append(obj['word'])

        return paragraphs, paragraph_times

    def apply_te(self, text, model, lan='ru'):
        # Применение техники улучшения текста
        return model.enhance_text(text, lan)

    def set_punctuation(self, data, timings):
        # Установка пунктуации и сохранение параграфов
        imp = package.PackageImporter('models/silero/v2_4lang_q.pt')
        model = imp.load_pickle("te_model", "model")

        current_video = Videos.objects.get(id=self.video_id)

        for lists, timing in zip(data, timings):
            input_text = ' '.join(lists)
            processed_text = self.apply_te(input_text, model, lan='ru')
            len_article = len(processed_text)
            paragraph = Paragraphs(
                article=processed_text, len_article=len_article, timestamp=timing)
            paragraph.save()
            paragraph.video.add(current_video)  # Связывание текста с видео

    def merge_paragraphs(self, data, paragraph_times):
        new_data = []
        temp_list = []

        first_time = True
        counter = 0
        timing = []

        for lists in data:
            if sum(len(word) for word in lists) <= 255:
                temp_list.extend(lists)
                if first_time == True:
                    timing.append(paragraph_times[counter])
                    first_time = False
                    counter += 1
            elif len(temp_list) > 0:
                temp_list.extend(lists)
                new_data.append(temp_list)
                temp_list = []
                first_time = True
                counter += 1
            else:
                new_data.append(lists)
                first_time = True
                timing.append(paragraph_times[counter])
                counter += 1

        return new_data, timing

    def process_text(self):
        # Получение экземпляра аудиофайла
        audio_instance = Audios.objects.get(video__id=self.video_id)
        audio_path = audio_instance.audio_file.path

        # Инициализация распознавателя речи
        recognizer = KaldiRecognizer(self.model, 16000)
        recognizer.SetWords(True)

        process = subprocess.Popen(['ffmpeg', '-loglevel', 'quiet', '-i', audio_path, '-ar', '16000', '-ac', '1', '-f', 's16le', '-'],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

        # Ожидание завершения процесса ffmpeg и получение вывода
        stdout, _ = process.communicate()

        recognizer.AcceptWaveform(stdout)
        result = recognizer.FinalResult()
        result = json.loads(result)

        result, paragraph_times = self.split_to_paragraphs(result)
        result, timings = self.merge_paragraphs(result, paragraph_times)
        self.set_punctuation(result, timings)
