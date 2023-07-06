# profbuh-video-to-article
## Установка

1. Скачайте архив с моделью Vosk:
   [https://alphacephei.com/vosk/models/vosk-model-ru-0.22.zip](https://alphacephei.com/vosk/models/vosk-model-ru-0.22.zip)

2. Распакуйте архив и поместите папку "vosk-model-ru-0.42" в папку "models".

3. В файле confog.py, которая находится в папке "profbuh_video_to_article" необходимо для значения OPEN_AI_KEY установить значения ключа от API Open AI ChatGPT (https://platform.openai.com/account/api-keys)

4. Установите зависимости:
   - Для frontend:
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
5. Создайте необходимые папки:
   - Создайте папку media со следующими подпапками:
       ```
       article
       ```
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


## Использование
1. Введите необходимые настройки:
![Screenshot from 2023-07-06 15-34-02](https://github.com/Viva-Fidel/profbuh-video-to-article/assets/98227548/60b0893c-dd5b-44de-9d3e-269527620594)

2. Дождитесь окончания обработки. Время обработки может зависеть от конфигурации сервера, но не менее 10 минут для ролика, длинною в 5 минут
3. Файл скачается в бразуере после окончания обработки
4. Пример созданной статьи можно увидеть в файле "example_output.docx"
![Screenshot from 2023-07-06 15-38-31](https://github.com/Viva-Fidel/profbuh-video-to-article/assets/98227548/48ef6a18-9a95-4bbb-8f77-907c12e16fff)
