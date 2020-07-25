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


class TwoTipsBrokenLine(VMobject):
    """An object consisting of three lines:

    - line from start to end;

    - line from start to start + direction * break_length

    - line from end to end + direction * break_length
    """
    CONFIG = {
        "line_kwargs": {
            "color": WHITE,
            "stroke_width": 4,
        },
    }

    def __init__(self, start, end, break_length=1, direction=RIGHT, **kwargs):
        VMobject.__init__(self, **kwargs)
        long_line = Line(start, end, **self.line_kwargs)
        first_end = start + break_length * direction
        second_end = end + break_length * direction
        first_tip_line = Line(start, first_end, **self.line_kwargs)
        second_tip_line = Line(end, second_end, **self.line_kwargs)
        first_tip_line.add_tip(tip_length=break_length / 5)
        second_tip_line.add_tip(tip_length=break_length / 5)
        self.add(long_line, first_tip_line, second_tip_line)


class Conference:
    """A holder object for a conference (teams, W/L)"""

    def __init__(self):
        numbers_args = {
            "font": "Roboto Condensed Italic",
            "color": WHITE,
        }
        self.teams = []
        self.wins = VGroup(*[Text("00", **numbers_args).scale(.4)
                             for i in range(8)])
        self.losses = VGroup(
            *[Text("00", **numbers_args).scale(.4) for i in range(8)])
        self.wins_raw = []
        self.losses_raw = []

    def convert(self):
        """This function is used to reverse the properties of the class, it
        adresses an issue where the objects are displayed in the opposite order
        """
        self.teams.reverse()
        self.wins_raw.reverse()
        self.losses_raw.reverse()
        self.teams = Group(*self.teams)


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
        self.animate_numbers(self.east)
        self.animate_numbers(self.west)
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

            self.east.teams.append(imgs[0])
            self.west.teams.append(imgs[1])
            self.east.wins_raw.append(REGULAR_SEASON_EAST[east][0])
            self.west.wins_raw.append(REGULAR_SEASON_WEST[west][0])
            self.east.losses_raw.append(REGULAR_SEASON_EAST[east][1])
            self.west.losses_raw.append(REGULAR_SEASON_WEST[west][1])

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

        # Teams ranking (1-8)
        texts = [Text(str(i) + ".", **self.numbers_args).scale(.4)
                 for i in range(1, 9)]
        rankings_east = VGroup(*texts)
        rankings_east.set_xy(x_east - .5, 2.02)
        rankings_west = rankings_east.copy()
        rankings_west.set_x(x_west - .5)
        rankings_east.arrange_submobjects(DOWN, False, False, buff=.5)
        rankings_west.arrange_submobjects(DOWN, False, False, buff=.5)

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
        # self.play(LaggedStart(*rankings_east_animation,
        #                       run_time=4, rate_function=rush_into))

        b = [AnimationGroup(
            Animation(Mobject(), run_time=i),  # <- This is a pause
            FadeIn(rankings_east[i]), lag_ratio=.5, rate_function=rush_from
        ) for i in range(8)]
        a = [AnimationGroup(
            Animation(Mobject(), run_time=i),  # <- This is a pause
            FadeIn(rankings_west[i]), lag_ratio=.5, rate_function=rush_from
        ) for i in range(8)]
        self.play(*a, *b)

    def animate_numbers(self, conf):
        """Animate wins/losses numbers from 0 to their actual values
        Parameters
        ----------
        conf: Conference
            The conference to add animation to its W/L
        """
        alpha = ValueTracker(0)

        def updater_wins(g):
            j = 0
            for i in g:
                x, y, z = i.get_center()
                txt = str(int(alpha.get_value() * conf.wins_raw[j]))
                i.become(
                    Text(txt, **self.numbers_args).set_xy(x, y).scale(.4)
                )
                j += 1

        def updater_losses(g):
            j = 0
            for i in g:
                x, y, z = i.get_center()
                txt = str(int(alpha.get_value() * conf.losses_raw[j]))
                i.become(
                    Text(txt, **self.numbers_args).set_xy(x, y).scale(.4)
                )
                j += 1

        conf.losses.arrange_submobjects(UP, False, False, buff=.52)
        conf.losses.add_updater(updater_losses)
        self.add(conf.losses)

        conf.wins.arrange_submobjects(UP, False, False, buff=.52)
        conf.wins.add_updater(updater_wins)
        self.add(conf.wins)

        self.play(alpha.increment_value, 1)
        self.wait()

    def animate_versus(self):
        """Animation of the confrontation between teams (1-8, 2-7, ...)"""

        groups = Group()
        for i in range(8):
            v = Group(self.east.teams[i],
                      self.east.wins[i], self.east.losses[i])
            groups.add(v)
        teams_animations = VGroup()
        dots_animations = VGroup()
        sequence = [(0, 7, DOWN), (6, 1, DOWN), (5, 4, DOWN), (3, 4, UP)]
        for i, j, k in sequence:
            c = ApplyMethod(groups[i].next_to,
                            groups[j], k, {"buff": .3})
            first_position = groups[i].get_center() - np.array([-.5, 0, 0])
            second_position = groups[j].get_center() - np.array([-.5, 0, 0])
            dots = VGroup(*[Dot(point=i)
                            for i in [first_position, second_position]])
            dot_animation = ShowCreationThenDestruction(dots)
            teams_animations.add(c)
            dots_animations.add(dot_animation)
        self.play(*teams_animations, *dots_animations)


class Test(Scene):

    def construct(self):
        test_line = TwoTipsBrokenLine(
            3 * np.ones(3), 3 * RIGHT, break_length=1)
        alpha = ValueTracker(0)

        test_line.add_updater(lambda m: m.become(
            TwoTipsBrokenLine(np.ones(3), RIGHT,
                              break_length=alpha.get_value())
        )
        )
        self.add(test_line)
        self.play(alpha.increment_value, 1)
#        self.play(ShowCreation(test_line))
