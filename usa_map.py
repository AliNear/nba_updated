from manimlib.imports import *
import os
ASSETS_PATH = os.getcwd() + "/projects/nba_update_project/assets/"
MAP_FILE = "us.svg"

class NBAScene(MovingCameraScene):
    CONFIG = {

            }
    def prepare(self):
        pass
    def add_teams(self):
        pass


class MainMapScene(MovingCameraScene):
    CONFIG = {
            "text_kwargs": {
                "font": "DW00efoe",
                "color": BLACK,
                }
            }
    def construct(self):
        self.prepare()
        self.general_info()
        self.east_west()
        self.teams_divison()
        self.to_division()
    
    def prepare(self):
        pass
    
    def general_info(self):
        pass
    
    def east_west(self):
        pass
    
    def teams_divison(self):
        pass

    def to_division(self):
        pass
