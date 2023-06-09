# media_controller.py

import time
import os
from PIL import Image
from application.gui.media_handler import ImageHandler
from application.gui.media_handler import VideoHandler
from application.infrastructure.local_storage import LocalImageStorage 
from application.infrastructure.local_storage import LocalVideoStorage
from application.infrastructure.local_storage import VideoExtensions
from application.infrastructure.local_storage import ImageExtensions

class MediaController:
    def __init__(self, media_folder, image_time=2):
        self.media_folder = media_folder
        self.image_time = image_time
        self.image_handler = ImageHandler(self.resize_image)
        self.video_handler = VideoHandler(self.resize_image)
        self.image_storage = LocalImageStorage()
        self.video_storage = LocalVideoStorage()

    @staticmethod
    def is_image_extension(file_extension):
        return ImageExtensions.contains(file_extension)

    @staticmethod
    def is_video_extension(file_extension):
        return VideoExtensions.contains(file_extension)

    @staticmethod
    def get_file_extension(file_path):
        _, file_extension = os.path.splitext(file_path)
        return file_extension

    @staticmethod
    def resize_image(image, max_width, max_height):
        width_ratio = max_width / image.width
        height_ratio = max_height / image.height
        min_ratio = min(width_ratio, height_ratio)

        new_width = int(image.width * min_ratio)
        new_height = int(image.height * min_ratio)

        return image.resize((new_width, new_height), Image.LANCZOS)

    def get_media_files(self):
        media_files = self.image_storage.get_media_files(self.media_folder) + self.video_storage.get_media_files(self.media_folder)
        return media_files

    def show_media(self):
        media_files = self.get_media_files()
        index = 0

        while True:
            if index >= len(media_files):
                index = 0

            file_path = media_files[index]
            file_extension = os.path.splitext(file_path)[1]

            if LocalImageStorage.contains(file_extension):
                self.image_handler.show(file_path)

            index += 1
            time.sleep(self.image_time)