import openai
from .models import Paragraphs, Videos, Screenshots
import time

import docx
from docx import Document


class ArticleCreation:
    def __init__(self, video_id, article_legth, annotation_length):
        self.article_legth = article_legth
        self.annotation_length = annotation_length
        self.video_id = video_id
        self.article_total_length = 0
        openai.api_key = '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'
    
    def get_response(self):
        paragraphs = Paragraphs.objects.filter(video=self.video_id)
        doc = Document()
        video = Videos.objects.get(id=self.video_id)
        title = video.video_name
        doc.add_heading(title, level=1)
        blank_paragraph = doc.add_paragraph()
        
        
        if self.article_legth != "Безгранично":
            for paragraph in paragraphs:
                self.article_total_length += paragraph.len_article
        

        full_text = []
        for index, paragraph in enumerate(paragraphs):
            if self.article_legth != "Безгранично":
                proportion = (paragraph.article/self.article_total_length)*self.article_legth
            else:
                proportion = "Безгранично"

            prompt = """
            Задание: Перефразируйте текст таким образом, чтобы сохранить его смысл.
            Тема статьи: {}
            Стиль: Официальный. 
            Запрещено: придумывать или добавлять что-то новое, использовать прямую речь, обращаться к зрителям или читателям (добрый день, уважаемые зрители), использовать слово "мы", указывать тему статьи, писать "В статье обсуждается/рассматривается".
            Разрешено: использовать списки.
            Формат ответа: текст.
            Максимальное количество символов: {}

            Текст: {}
            """.format(title, proportion, paragraph.article)

            # Send a completion request to the ChatGPT model
            response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": prompt}
  ]
)

            # Extract the generated paraphrase from the response
            paraphrase = response.choices[0]['message']['content']
            decoded_content = paraphrase.encode('utf-8').decode()

            # Retrieve the corresponding screenshots for the current paragraph
            screenshot = Screenshots.objects.filter(video=self.video_id).order_by('timestamp')[index]
    
            hours = screenshot.timestamp // 3600  # Get the integer division for hours
            minutes = (screenshot.timestamp % 3600) // 60  # Get the integer division for minutes
            seconds = screenshot.timestamp % 60  # Get the remainder division for seconds
            
            timestamp_formatted = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
            doc.add_paragraph(f"Время начала абзаца: {timestamp_formatted}", style="BodyText")
            full_text.append(decoded_content)
            doc.add_paragraph(decoded_content, style="BodyText")
            doc.add_picture(screenshot.screenshot.path, width=docx.shared.Inches(6), height=docx.shared.Inches(4))
            print('One more iteration done')
            time.sleep(20)
        
        
        prompt = """
            Напиши аннотацию к статье
            Максимальное количество символов: {}

            Текст: {}
            """.format(self.annotation_length, full_text[0])

        # Send a completion request to the ChatGPT model
        response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": prompt}
  ]
)

        # Extract the generated paraphrase from the response
        annotation = response.choices[0]['message']['content']
        decoded_content = annotation.encode('utf-8').decode()
        
        blank_paragraph.text = f"Аннотация: {decoded_content}"
        # Save the document
        doc.save("output.docx")
