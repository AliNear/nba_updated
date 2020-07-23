from manimlib.imports import *
import os

ASSETS_PATH = os.path.join(os.getcwd(), "assets")


class TwoRects(VMobject):
    """Two rectangles with different colors representing eastern/western
       conferences"""

    def __init__(self, **kwargs):
        VMobject.__init__(self, **kwargs)
        x, y = 10, 5
        points_left = [(-x, y), (0, y), (0, -y), (-x, -y)]
        points_right = [(x, y), (0, y), (0, -y), (x, -y)]
        points_left = [np.array([i, j, 0]) for i, j in points_left]
        points_right = [np.array([i, j, 0]) for i, j in points_right]

        east_rect = Polygon(*points_left, fill_color="#1c3f87",
                            fill_opacity=1, stroke_width=0)

        west_rect = Polygon(*points_right, fill_color="#b8002c",
                            fill_opacity=1, stroke_width=0)
        self.add(east_rect, west_rect)


class RankingScene(Scene):
    """A scene showing frachise ranking in bothe conferences"""

    def construct(self):
        self.prepare()
        self.add_teams()
        self.animate_numbers()
        self.animate_versus()

    def prepare(self):
        """Adding background to the scene and other elements + variable
         initialisation and data preparation"""
        pass

    def add_teams(self):
        """Adding the teams to the scene"""
        pass

    def animate_numbers(self):
        """Animate wins/losses numbers from 0 to their actual values"""
        pass

    def animate_versus(self):
        """Animation of the confrontation between teams (1-8, 2-7, ...)"""
        pass
