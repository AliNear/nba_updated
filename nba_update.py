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


class VersusLines(VMobject):
    CONFIG = {
        "line_kwargs": {
            "color": WHITE,
            "stroke_width": 3,
        },
        "lines_length": .7,
        "merged_line_length": .5

    }

    def __init__(self, first_side, second_side, direction=RIGHT, **kwargs):
        VMobject.__init__(self, **kwargs)
        length = self.lines_length * direction
        main_lines = [Line(i, i + length, **self.line_kwargs)
                      for i in (first_side, second_side)]
        vertical_line = Line(first_side + length,
                             second_side + length, **self.line_kwargs)
        first_point = (first_side + second_side + 2 * length) / 2
        self.last_point = first_point + direction * self.merged_line_length
        merged_line = Line(first_point, self.last_point, **self.line_kwargs)

        self.add(*main_lines, vertical_line, merged_line)


class RankingScene(MovingCameraScene):
    """A scene showing frachise ranking in bothe conferences"""
    CONFIG = {
        "numbers_args": {
            "font": "Roboto Condensed Italic",
            "color": WHITE,
        }
    }

    def __init__(self, **kwargs):
        MovingCameraScene.__init__(self, **kwargs)

    def construct(self):
        self.prepare()
        self.draw_foundation()
        self.add_teams()
        self.setup_conferences()
        self.animate_conferences()
        self.animate_numbers(self.east)
        self.animate_numbers(self.west)
        self.animate_versus()
        self.rearrange_teams()

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

        self.east_west_confs = Group(box_east, east_icon, box_west, west_icon)

        east_icon.move_to(box_east)
        west_icon.move_to(box_west)
        box_playoffs = Rectangle(fill_color=WHITE, fill_opacity=1,
                                 width=2, height=.4).set_xy(0, 3.5)
        playoffs = Avatar(ASSETS_PATH + "nba-playoffs-2.png", 0, 3.5, .15)
        self.playoffs = Group(box_playoffs, playoffs)

    def draw_foundation(self):
        """Animation of the scene foundations (bg, title, etc ...)"""
        self.play(FadeInFrom(self.background, direction=-
                             7 * UP, rate_function=lingering))
        self.play(FadeInFrom(self.playoffs,
                             direction=UP, rate_function=rush_into))
        self.play(FadeInFrom(self.east_west_confs,
                             direction=3 * UP, rate_function=rush_into))

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
                 for i in range(8, 0, -1)]

        self.rankings_east = VGroup(*texts)
        self.rankings_east.set_xy(x_east - .5, y_conf)  # 2.02
        self.rankings_west = self.rankings_east.copy()
        self.rankings_west.set_x(x_west - .5)
        self.rankings_east.arrange_submobjects(UP, False, False, buff=.5)
        self.rankings_west.arrange_submobjects(UP, False, False, buff=.5)

        # Wins/losses title (W and L)
        y_titles = 2.8
        wins_title_east = Text("W", **self.numbers_args).scale(.45)
        wins_title_east.set_xy(x_east + 1, y_titles)
        losses_title_east = Text("L", **self.numbers_args).scale(.45)
        losses_title_east.set_xy(x_east + 2, y_titles)
        wins_title_west = wins_title_east.copy().set_x(x_west + 1)
        losses_title_west = losses_title_east.copy().set_x(x_west + 2)

        self.wins_losses = VGroup(wins_title_east, losses_title_east,
                                  wins_title_west, losses_title_west)

    def animate_conferences(self):

        # Animate the whole thing
        self.play(self.east.teams.arrange_submobjects,
                  UP, False, False, {"buff": .3})
        self.play(self.west.teams.arrange_submobjects,
                  UP, False, False, {"buff": .3})
        self.play(FadeInFrom(self.wins_losses, direction=2 * UP))

        b = [AnimationGroup(
            Animation(Mobject(), run_time=i),
            FadeIn(self.rankings_east[i]), lag_ratio=.5, rate_function=rush_from
        ) for i in range(8)]
        a = [AnimationGroup(
            Animation(Mobject(), run_time=i),
            FadeIn(self.rankings_west[i]), lag_ratio=.5, rate_function=rush_from
        ) for i in range(8)]
        self.play(*a, *b)

    def animate_numbers(self, conf, animation_time=2):
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

        self.play(alpha.increment_value, 1, run_time=animation_time)
        self.wait()

    def animate_versus(self):
        """Animation of the confrontation between teams (1-8, 2-7, ...)"""
        alpha = ValueTracker(0)
        amount_x = np.array([1, 0, 0])
        amount_y = np.array([0, .8, 0])
        start_east = np.array([-5.82, 2.05, 0]) - amount_x
        start_west = np.array([1.26, 2.05, 0]) - amount_x
        end_east = np.array([-5.82, -3.47, 0]) - amount_x
        end_west = np.array([1.26, -3.47, 0]) - amount_x

        versus_line_east = TwoTipsBrokenLine(start_east, end_east)
        versus_line_west = TwoTipsBrokenLine(start_west, end_west)

        self.add(versus_line_east, versus_line_west)
        for i in range(4):
            new_start_east = start_east - i * amount_y
            new_end_east = end_east + i * amount_y
            new_start_west = start_west - i * amount_y
            new_end_west = end_west + i * amount_y

            self.play(versus_line_east.become,
                      TwoTipsBrokenLine(new_start_east, new_end_east),
                      versus_line_west.become,
                      TwoTipsBrokenLine(new_start_west, new_end_west))
            self.wait(.5)

        self.play(FadeOut(versus_line_east), FadeOut(versus_line_west))
        self.wait()

    def rearrange_teams(self):

        self.groups_east = Group()
        self.groups_west = Group()
        for i in range(8):
            east_line = Group(self.rankings_east[i], self.east.teams[i],
                              self.east.wins[i], self.east.losses[i])
            west_line = Group(self.rankings_west[i], self.west.teams[i],
                              self.west.wins[i], self.east.losses[i])
            self.groups_east.add(east_line)
            self.groups_west.add(west_line)
        teams_animations = VGroup()
        sequence = [(0, 7, DOWN), (6, 1, DOWN), (5, 4, DOWN), (3, 4, UP)]
        for i, j, k in sequence:
            e = ApplyMethod(self.groups_east[i].next_to,
                            self.groups_east[j], k, {"buff": .3})
            w = ApplyMethod(self.groups_west[i].next_to,
                            self.groups_west[j], k, buff=.3)
            teams_animations.add(e, w)
        self.play(*teams_animations)


class BlankNBAScene(RankingScene):
    """A scene that shows how the playoffs games are played
    """

    def setup(self):
        self.prepare()
        self.add_teams()
        self.setup_conferences()
        self.arrange_objects()
        self.add_all()
        self.rearrange_teams()
        self.remove_unnecessary_mobjects()

    def arrange_objects(self):
        self.east.teams.arrange_submobjects(
            UP, False, False, buff=.3)
        self.west.teams.arrange_submobjects(
            UP, False, False, buff=.3)
        self.east.wins.arrange_submobjects(
            UP, False, False, buff=.52)
        self.west.wins.arrange_submobjects(
            UP, False, False, buff=.52)
        self.east.losses.arrange_submobjects(
            UP, False, False, buff=.52)
        self.west.losses.arrange_submobjects(
            UP, False, False, buff=.52)

    def add_all(self):
        self.add(self.background, self.east_west_confs, self.playoffs)
        self.add(self.east.teams)
        self.add(self.west.teams)
        self.add(self.rankings_east, self.rankings_west)
        self.add(self.wins_losses)

    def remove_unnecessary_mobjects(self):
        for i in range(8):
            self.remove(*self.groups_east[i][0])
            self.remove(*self.groups_west[i][0])
            self.remove(*self.groups_east[i][2:])
            self.remove(*self.groups_west[i][2:])
        self.remove(self.wins_losses)


class PlayoffsScene(BlankNBAScene):

    def construct(self):
        self.reorganize_teams()
        self.move_conferences_names()
        self.to_playoffs_positions()
        self.start_versus()

    def reorganize_teams(self):
        # indexes are used to reorganize the teams (due to previous movements)
        self.indexes = [7, 0, 3, 4, 5, 2, 1, 6]
        new_group_east = Group()
        new_group_west = Group()

        for i in range(8):
            new_group_east.add(self.east.teams[self.indexes[i]])
            new_group_west.add(self.west.teams[self.indexes[i]])

        self.east.teams = new_group_east
        self.west.teams = new_group_west

    def move_conferences_names(self):
        east_bloc = self.east_west_confs[:2]
        west_bloc = self.east_west_confs[2:]
        self.play(east_bloc.shift, 4 * RIGHT,
                  west_bloc.shift, 4 * LEFT)

    def to_playoffs_positions(self):
        self.matches_east = Group()
        self.matches_west = Group()
        for i in [0, 2, 4, 6]:
            match_east = Group(self.east.teams[i:i + 2])
            self.matches_east.add(match_east)
        for i in [0, 6, 4, 2]:
            match_west = Group(self.west.teams[i:i + 2])
            self.matches_west.add(match_west)

        self.play(self.matches_east.shift, 1.33 * UP + LEFT)
        self.play(self.matches_west.shift, 1.33 * UP + 4 * RIGHT)
        self.play(self.matches_east.arrange_submobjects,
                  DOWN, False, False, {"buff": .7},
                  self.matches_west.arrange_submobjects,
                  DOWN, False, False, {"buff": .7})

    def versus_animation(self, teams, winners_list, direction=RIGHT):

        bias = .4 * direction
        res_teams = Group()
        faceoff = Group()
        for i in teams:
            first, second = i[0]
            start, end = first.get_center() + bias, second.get_center() + bias
            versus_line = VersusLines(start, end, direction=direction)
            last_point = versus_line.last_point
            self.play(ShowCreation(versus_line))
            winner = i[0][winners_list.pop(0)]
            winner_copy = winner.copy()
            self.play(winner_copy.move_to, last_point + .3 * direction)
            faceoff.add(winner_copy)
        for i in range(0, len(faceoff) // 2 + 1, 2):
            res_teams.add(Group(faceoff[i:i + 2]))
        return res_teams

    def start_versus(self):
        next_round_east = [0, 1, 0, 1]
        semi_finals_east = [0, 1]
        winners_east = [next_round_east, semi_finals_east, [1]]

        next_round_west = [1, 0, 1, 0]
        semi_finals_west = [0, 1]
        winners_west = [next_round_west, semi_finals_west, [0]]

        next_teams_east = self.matches_east
        for i in range(3):
            next_teams_east = self.versus_animation(
                next_teams_east, winners_east[i])

        next_teams_west = self.matches_west
        for i in range(3):
            next_teams_west = self.versus_animation(
                next_teams_west, winners_west[i], direction=LEFT)


class Test(Scene):

    def construct(self):
        second = np.array([1, -2, 0])
        obj = VersusLines(RIGHT, second)
        self.play(ShowCreation(obj))
