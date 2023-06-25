import cv2
import numpy as np
from .models import Screenshots, Videos
from django.db.models import Sum
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
import os

class VideoPostFrameProcessor:
    def __init__(self, video_id, focus_time):
        self.video_id = video_id
        self.current_screenshot_group = 1
        self.previous_screenshot = None
        self.show_time = focus_time
        self.threshold = 50

    def calculate_mse(self, img1, img2):
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
                self.save_screenshot(screenshot, self.current_screenshot_group)
            else:
                self.current_screenshot_group += 1
                self.save_screenshot(screenshot, self.current_screenshot_group)
        self.previous_screenshot = img
        
    def save_screenshot(self, screenshot, group):
        screenshot.group = group
        screenshot.save()

    def detect_red_square(self, image):
        # Convert the image to the RGB color space
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Define the lower and upper bounds for red color in RGB
        lower_red = np.array([100, 0, 0])
        upper_red = np.array([255, 50, 50])
    
        # Create a binary mask based on the red color range
        mask = cv2.inRange(rgb_image, lower_red, upper_red)
    
        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Iterate over the contours and check if any bounding box is detected
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w > 10 and h > 10:  # Minimum width and height thresholds to consider it as a bounding box
                return True
    
        return False

    def process_video_screenshots(self):
        screenshots = Screenshots.objects.filter(video=self.video_id).order_by('timestamp')
    
        for screenshot in screenshots:
            screenshot_path = screenshot.screenshot.path
            img = cv2.imread(screenshot_path)
            self.process_screenshot(screenshot, img)
    
        for group in screenshots.values('group').distinct():
            group_number = group['group']
            group_screenshots = screenshots.filter(group=group_number)

            # Get the total length in seconds for each group
            group_lengths = screenshots.values('group').annotate(length=Sum('timestamp'))

           # Iterate over the groups and delete the ones with length less than 10 seconds
            for group_length in group_lengths:
                group_number = group_length['group']
                length = group_length['length']
                if length < 10:
                    group_screenshots = screenshots.filter(group=group_number)
                    for screenshot in group_screenshots:
                        screenshot_path = screenshot.screenshot.path
                        os.remove(screenshot_path)
                    group_screenshots.delete()
    
            for screenshot in group_screenshots:
                screenshot_path = screenshot.screenshot.path
                img = cv2.imread(screenshot_path)
    
                # Check if there is a red square in the frame
                has_red_square = self.detect_red_square(img)
    
                # Update the red_square field of the screenshot model
                screenshot.red_square = has_red_square
                screenshot.save()
        
