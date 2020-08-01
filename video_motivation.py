from manimlib.imports import *
import os
ASSESTS_PATH = os.getcwd() + '/' + assets + '/'

class MotivationScene(MovingCameraScene):

    class construct(self):
        self.prepare()
        self.draw_map()
        self.show_different_formats()
        self.focus_on_europe()
        self.back_to_us()

    def prepare(self):
        """Assests prepation (mainly the world map and a backgroudn?)
        """
        pass
    
    def draw_map(self):
        """Draw the world map"""
        pass

    def show_different_formats(self):
        """Show the different regions (Europe/Asia/Africa/... vs North America)"""
        pass

    def focus_on_europe(self):
        """Show how chamionships are played (and won) in european countries (football)"""
        pass

    def back_to_us(self):
        """Show why it can't be done in the us (big country)"""
        pass

