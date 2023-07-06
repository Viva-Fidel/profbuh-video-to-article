from .models import Screenshots

import cv2
import numpy as np


class VideoPostFrameProcessor:
    def __init__(self, video_id, focus_time):
        self.video_id = video_id
        self.current_screenshot_group = 1
        self.previous_screenshot = None
        self.show_time = focus_time
        self.threshold = 30

    def calculate_mse(self, img1, img2):
        # Вычисление среднеквадратичной ошибки (MSE) между двумя изображениями
        img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        mse = np.mean((img1_gray - img2_gray) ** 2)
        return mse

    def process_screenshot(self, screenshot, img):
        if self.previous_screenshot is None:
            self.save_screenshot(screenshot, self.current_screenshot_group)
        else:
            mse = self.calculate_mse(img, self.previous_screenshot)
            if mse < self.threshold:
                has_red_square = self.detect_red_square(img)
                screenshot.red_square = has_red_square
                self.save_screenshot(screenshot, self.current_screenshot_group)
            else:
                has_red_square = self.detect_red_square(img)
                screenshot.red_square = has_red_square
                self.current_screenshot_group += 1
                self.save_screenshot(screenshot, self.current_screenshot_group)
        self.previous_screenshot = img

    def save_screenshot(self, screenshot, group):
        # Сохранение скриншота с указанием его группы
        screenshot.group = group
        screenshot.save()

    def detect_red_square(self, image):
        # Преобразование изображения в цветовое пространство RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Задание нижней и верхней границ красного цвета в цветовом пространстве RGB
        lower_red = np.array([100, 0, 0])
        upper_red = np.array([255, 50, 50])

        # Создание бинарной маски на основе диапазона красного цвета
        mask = cv2.inRange(rgb_image, lower_red, upper_red)

        # Поиск контуров на маске
        contours, _ = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Итерация по контурам и проверка, есть ли обнаруженный ограничивающий прямоугольник
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w > 10 and h > 10:  # Минимальные пороги ширины и высоты для учета его как ограничивающего прямоугольника
                return True

        return False

    def process_video_screenshots(self):
        # Получение скриншотов видео и их обработка
        screenshots = Screenshots.objects.filter(
            video=self.video_id).order_by('timestamp')

        for screenshot in screenshots:
            screenshot_path = screenshot.screenshot.path
            img = cv2.imread(screenshot_path)
            self.process_screenshot(screenshot, img)
