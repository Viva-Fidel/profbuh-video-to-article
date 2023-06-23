import cv2
import numpy as np
from .models import Screenshots, Videos
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image

class VideoFrameProcessor:
    def __init__(self, video_path, video_id, focus_time=10):
        self.video_id = video_id
        self.video_path = video_path
        self.threshold = 50
        self.start_time = 5
        self.prev_frame = None
        self.counter = 1 
        self.screen_time = 0
        self.show_time = focus_time


    def calculate_mse(self, frame1, frame2):
        # Calculate the mean squared error between two frames
        error = np.mean((frame1.astype("float") - frame2.astype("float")) ** 2)
        return error

    def detect_and_capture(self, frame, timestamp):

        if self.prev_frame is not None:
            # Convert frame to grayscale
            new_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            mse = self.calculate_mse(self.prev_frame, new_frame)
            self.prev_frame = new_frame
  
            # Check if the MSE is above the threshold
            if mse > self.threshold:
                if timestamp - self.show_time >= self.screen_time:
                    self.screen_time = timestamp
                    
                    # Generate the file name using the time offset # Convert to milliseconds
                    filename = f"screenshot_{timestamp-self.show_time}.jpg"

                    # Save a screenshot of the current frame
                    image = Image.fromarray(frame)
                    image_buffer = io.BytesIO()
                    image.save(image_buffer, format='JPEG')
                    image_file = InMemoryUploadedFile(
                           image_buffer,
                           None,
                           filename,
                           'image/jpeg',
                           image_buffer.tell(),
                           None
                        )
    
                    # Save a screenshot of the current frame
                    screenshot = Screenshots.objects.create(screenshot_id=self.video_id, timestamp=timestamp-5)
                    screenshot.screenshot.save(filename, image_file)
                        
                    current_video = Videos.objects.get(id=self.video_id)
                    screenshot.video.add(current_video)  # Associate the screenshot with the video
                    screenshot.save()
                else:
                    self.screen_time = timestamp


    def process_video(self):
      
        video_capture = cv2.VideoCapture(self.video_path)

        while True:
            ret, frame = video_capture.read()

            if not ret:
                break

            # Get the current timestamp
            timestamp = video_capture.get(cv2.CAP_PROP_POS_MSEC) / 1000  # Convert to seconds

            if timestamp > self.start_time:
                self.detect_and_capture(frame, timestamp)
            else:
                self.prev_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                self.screen_time = timestamp

        # Release the video capture and close windows
        video_capture.release()
