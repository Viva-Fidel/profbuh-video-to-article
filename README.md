# profbuh-video-to-article
## Инструкция для корректной работы

1. Скачайте архив с моделью Vosk:
   [https://alphacephei.com/vosk/models/vosk-model-ru-0.22.zip](https://alphacephei.com/vosk/models/vosk-model-ru-0.22.zip)

2. Распакуйте архив и поместите папку "vosk" в папку "models".

3. Установите зависимости:
   - Для веб-интерфейса:
     - Перейдите в папку "frontend":
       ```
       cd frontend
       ```
     - Установите зависимости с помощью npm:
       ```
       npm i
       ```
     - Запустите веб-интерфейс:
       ```
       npm start
       ```

   - Для backend:
     - Установите зависимости Python:
       ```
       pip install -r requirements.txt
       ```
     - Запустите сервер:
       ```
       python manage.py runserver
       ```
4. Установите зависимости:
   - Создайте папку media со следующими подпапками:
```
       screenshots
       ```
```
       videos
       ```
```
       audio
       ```
   
6. Для запуска Celery выполните следующую команду:
   ```
   celery -A profbuh_video_to_article worker -l info
   ```
