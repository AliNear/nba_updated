from manimlib.imports import *
import os
from projects.project_one.custom_mobjects import *
from itertools import product

ASSETS_PATH = os.path.join(os.getcwd(), "projects/nba_update_project/assets/")
TEAMS_PATH = ASSETS_PATH + "teams/"
# Final results for each franchise (EAST/WEST)

REGULAR_SEASON_EAST = {
    "MilwaukeeBucks": (60, 22),
    "TorontoRaptors": (59, 24),
    "Philadelphia76ers": (51, 31),
    "Boston_Celtics": (49, 33),
    "Indiana_Pacers": (48, 34),
    "BrooklynNets": (42, 40),
    "OrlandoMagic": (42, 40),
    "DetroitPistons": (41, 41),
}
REGULAR_SEASON_WEST = {
    "GoldenState": (72, 10),
    "Denver_Nuggets": (54, 28),
    "Houston_Rockets": (53, 29),
    "PortlandTrail": (53, 29),
    "UtahJazz": (50, 32),
    "Oklahoma_City_Thunder": (49, 33),
    "San_Antonio_Spurs": (48, 34),
    "Los_Angeles_Clippers": (48, 34),
}


class Conference:
    """A holder object for a conference (teams, W/L)"""

    def __init__(self):
        self.teams = []
        self.wins = []
        self.losses = []

    def convert(self):
        """This function is used to reverse the properties of the class, it 
        adresses an issue where the objects are displayed in the opposite order
        """
        self.teams.reverse()
        self.wins.reverse()
        self.losses.reverse()
        self.teams = Group(*self.teams)
        self.wins = VGroup(*self.wins)
        self.losses = VGroup(*self.losses)


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
    CONFIG = {
        "numbers_args": {
            "font": "Roboto Condensed Italic",
            "color": WHITE,
        }
    }

    def construct(self):
        self.prepare()
        self.draw_foundation()
        self.add_teams()
        self.setup_conferences()
        self.animate_numbers()
        self.animate_versus()

    def prepare(self):
        """Adding background to the scene and other elements + variable
         initialisation and data preparation """
        self.background = TwoRects()
        # boxes to hold EASTERN CONF/WEST... images
        box_east = Rectangle(
            fill_color=WHITE, fill_opacity=1, width=1.1, height=.7)
        x_box, y_box = 6, 3.4
        box_east.set_xy(-x_box, y_box)
        box_west = box_east.copy()
        box_west.set_x(x_box)
        # east and west confs images
        east_icon = Avatar(ASSETS_PATH + "east0.png", 0, 0, .3)
        west_icon = Avatar(ASSETS_PATH + "west.png", 0, 0, .3)

        self.east_west_confs = Group(box_east, box_west, east_icon, west_icon)

        east_icon.move_to(box_east)
        west_icon.move_to(box_west)
        box_playoffs = Rectangle(fill_color=WHITE, fill_opacity=1,
                                 width=2, height=.6).set_xy(0, 3.5)
        playoffs = Avatar(ASSETS_PATH + "playoffs.png", 0, 3.5, .35)
        self.playoffs = Group(box_playoffs, playoffs)

    def draw_foundation(self):
        """Animation of the scene foundations (bg, title, etc ...)"""
        self.play(FadeInFrom(self.background, direction=-7 * UP))
        self.play(FadeInFrom(self.playoffs, direction=UP))
        self.play(FadeInFrom(self.east_west_confs, direction=3 * UP))

    def add_teams(self):
        """Adding the teams (with W/L) to the Class"""
        self.east = Conference()
        self.west = Conference()
        # We'll use iterators instead of dicts, to gain simplicity

        for i in zip(iter(REGULAR_SEASON_EAST), iter(REGULAR_SEASON_WEST)):
            east, west = i
            imgs = [Avatar(TEAMS_PATH + n + ".png", 0, 0, .25) for n in i]
            txt_win_east = Text(str(
                REGULAR_SEASON_EAST[east][0]), **self.numbers_args).scale(.4)
            txt_loss_east = Text(str(
                REGULAR_SEASON_EAST[east][1]), **self.numbers_args).scale(.4)

            txt_win_west = Text(str(
                REGULAR_SEASON_WEST[west][0]), **self.numbers_args).scale(.4)
            txt_loss_west = Text(str(
                REGULAR_SEASON_WEST[west][1]), **self.numbers_args).scale(.4)
            self.east.teams.append(imgs[0])
            self.east.wins.append(txt_win_east)
            self.east.losses.append(txt_loss_east)
            self.west.teams.append(imgs[1])
            self.west.wins.append(txt_win_west)
            self.west.losses.append(txt_loss_west)
        self.east.convert()
        self.west.convert()

    def setup_conferences(self):
        """Here we set up the coordinates for each conf"""
        x_east = -(FRAME_WIDTH / 2 - 2)
        x_west = 2
        y_conf = -3.5
        self.east.teams.set_xy(x_east, y_conf)
        self.west.teams.set_xy(x_west, y_conf)
        self.east.wins.set_xy(x_east + 1, y_conf)
        self.east.losses.set_xy(x_east + 2, y_conf)

        self.west.wins.set_xy(x_west + 1, y_conf)
        self.west.losses.set_xy(x_west + 2, y_conf)

        # Wins/losses title (W and L)
        y_titles = 2.8
        wins_title_east = Text("W", **self.numbers_args).scale(.45)
        wins_title_east.set_xy(x_east + 1, y_titles)
        losses_title_east = Text("L", **self.numbers_args).scale(.45)
        losses_title_east.set_xy(x_east + 2, y_titles)
        wins_title_west = wins_title_east.copy().set_x(x_west + 1)
        losses_title_west = losses_title_east.copy().set_x(x_west + 2)

        wins_losses = VGroup(wins_title_east, losses_title_east,
                             wins_title_west, losses_title_west)

        # Animate the whole thing
        self.play(self.east.teams.arrange_submobjects,
                  UP, False, False, {"buff": .3})
        self.play(self.west.teams.arrange_submobjects,
                  UP, False, False, {"buff": .3})
        self.play(FadeInFrom(wins_losses, direction=2 * UP))

        self.play(self.east.wins.arrange_submobjects,
                  UP, False, False, {"buff": .52})
        self.play(self.east.losses.arrange_submobjects,
                  UP, False, False, {"buff": .52})

        self.play(self.west.wins.arrange_submobjects,
                  UP, False, False, {"buff": .52})
        self.play(self.west.losses.arrange_submobjects,
                  UP, False, False, {"buff": .52})

    def animate_numbers(self):
        """Animate wins/losses numbers from 0 to their actual values"""

    def animate_versus(self):
        """Animation of the confrontation between teams (1-8, 2-7, ...)"""
        pass


class Test(Scene):

    def construct(self):
        t = Text("dv ", font="Roboto Light")
        rr = Text(" dd", font="Roboto Light")
        t.set_x(4)
        rr.set_x(2)
        v = VGroup(t, rr)
        alpha = ValueTracker(0)

        def updater(g):
            for i in g:
                x, y, z = i.get_center()
                i.become(
                    Text(str(int(alpha.get_value() * 20)),
                         font="Roboto Light", color=BLACK).set_xy(x, y)
                )
        v.add_updater(updater)
        self.add(v)
        self.play(alpha.increment_value, 1)
