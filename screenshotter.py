import os 
import threading
import time 

from PIL import ImageGrab

from util import get_timestamp

class Screenshotter:
    def __init__(self, logger, save_path, interval, 
                 resolution, resolution_factor=None):
        """
        Resolution should be (width, height)

        take ss every interval seconds
        """
        self.logger = logger
        self.save_path = save_path
        os.makedirs(save_path, exist_ok=True)
        
        self.interval = interval
        self.resolution = resolution # monitor resolution
        if resolution_factor is not None:
            self.resolution_factor = resolution_factor
            width, height = resolution
            self.save_resolution = (int(width * resolution_factor), 
                                    int(height * resolution_factor))
            
        self._active = False 
        self.thread = threading.Thread(target=self.main)

    @property 
    def active(self):
        return self._active

    def start(self):
        """start the screenshotter"""
        if not self._active:
            self._active = True 
            self.thread.start()
            self.logger.info("Start screenshotter")

    def stop(self):
        """stop the screenshotter"""
        if self._active:
            self._active = False 
            self.thread.join()
            self.logger.info("Stop screenshotter")

    def capture(self):
        """Capture screenshot"""
        ss = ImageGrab.grab(bbox=(0, 0, *self.resolution))
        if self.resolution_factor is not None:
            ss = ss.resize(self.save_resolution)

        ss = ss.convert("RGB")
        timestamp = get_timestamp()
        ss.save(os.path.join(self.save_path, f"{timestamp}.png"), optimize=True, quality=10)
        self.logger.info("took screenshot")

    def main(self):
        """Screenshotter main loop"""
        while True: 
            if not self._active:
                continue 

            self.capture()
            time.sleep(self.interval)