from manimlib.imports import *
import os
from projects.project_one.custom_mobjects import *
from itertools import product 
import random
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
    "PortlandTrailBlazers": (53, 29),
    "Houston_Rockets": (53, 29),
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


class NumberAnimation(VMobject):
    """A `Text` object that has an animation bound to a ValueTracker
    """
    CONFIG = {
        "text_kwargs": {
            "color": WHITE,
            "font": "Bitter",
        },
        "scale_factor": .3,
        "animation_length": .5

    }

    def __init__(self, target, next_to_object, **kwargs):
        VMobject.__init__(self, **kwargs)
        number = Text("0", **self.text_kwargs)
        number.next_to(next_to_object, UP, buff=.15)
        self.alpha = ValueTracker(0)
        # number.add_updater(lambda m: m.become(
        #     Text(str(int(self.alpha.get_value() * target)),
        #          color=BLACK).next_to(next_to_object, UP, buff=.3)
        # )
        # )

        def updater(t):
            new_number = Text(
                str(int(self.alpha.get_value() * target)), **self.text_kwargs)
            new_number.scale(self.scale_factor)
            new_number.next_to(next_to_object, UP, buff=.15)
            t.become(new_number)

        number.add_updater(updater)

        self.add(number)
        self.animation = ApplyMethod(
            self.alpha.increment_value, 1, run_time=self.animation_length)


class Conference:
    """A holder object for a conference (teams, W/L)"""

    def __init__(self):
        numbers_args = {
            "font": "DDT W00 Condensed Bold Italic",
            "color": WHITE
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
        west_color = "#1c3f87"
        east_color = "#b8002c"
        points_left = [(-x, y), (0, y), (0, -y), (-x, -y)]
        points_right = [(x, y), (0, y), (0, -y), (x, -y)]
        points_left = [np.array([i, j, 0]) for i, j in points_left]
        points_right = [np.array([i, j, 0]) for i, j in points_right]

        self.east_rect = Polygon(*points_right, fill_color=east_color,
                                 fill_opacity=1, stroke_width=0)

        self.west_rect = Polygon(*points_left, fill_color=west_color,
                                 fill_opacity=1, stroke_width=0)
        self.add(self.east_rect, self.west_rect)


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
        self.main_lines = [Line(i, i + length, **self.line_kwargs)
                           for i in (first_side, second_side)]
        vertical_line = Line(first_side + length,
                             second_side + length, **self.line_kwargs)
        first_point = (first_side + second_side + 2 * length) / 2
        self.last_point = first_point + direction * self.merged_line_length
        merged_line = Line(first_point, self.last_point, **self.line_kwargs)

        self.add(*self.main_lines, vertical_line, merged_line)


class RankingScene(MovingCameraScene):
    """A scene showing frachise ranking in bothe conferences"""
    CONFIG = {
        "numbers_args": {
            "font": "DDT W00 Condensed Bold Italic",
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
        self.animate_numbers(self.east, .01)
        self.animate_numbers(self.west, .01)
        # self.animate_versus()
        # self.wait()
        self.rearrange_teams()

    def prepare(self):
        """Adding background to the scene and other elements + variable
         initialisation and data preparation """
        self.background = TwoRects()
        # boxes to hold EASTERN CONF/WEST... images
        box_east = Rectangle(
            fill_color=WHITE, fill_opacity=1, width=1.1, height=.7)
        x_box, y_box = 6, 3.4
        box_east.set_xy(x_box, y_box)
        box_west = box_east.copy()
        box_west.set_x(-x_box)
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
            imgs = [Avatar(TEAMS_PATH + n + ".png", 0, 0, .25)
                    for n in i]

            self.east.teams.append(imgs[0])
            self.west.teams.append(imgs[1])
            self.east.wins_raw.append(REGULAR_SEASON_EAST[east][0])
            self.west.wins_raw.append(REGULAR_SEASON_WEST[west][0])
            self.east.losses_raw.append(REGULAR_SEASON_EAST[east][1])
            self.west.losses_raw.append(REGULAR_SEASON_WEST[west][1])

        # This one to align the versus lines in a different scene (Denver icon is big)
        self.west.teams[1].scale(.88)
        self.east.convert()
        self.west.convert()

    def setup_conferences(self):
        """Here we set up the coordinates for each conf"""
        x_west = -(FRAME_WIDTH / 2 - 2)
        x_east = 2
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
        self.rankings_east.arrange_submobjects(UP, False, False, buff=.65)
        self.rankings_west.arrange_submobjects(UP, False, False, buff=.65)

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

        conf.losses.arrange_submobjects(UP, False, False, buff=.65)
        conf.losses.add_updater(updater_losses)
        self.add(conf.losses)

        conf.wins.arrange_submobjects(UP, False, False, buff=.65)
        conf.wins.add_updater(updater_wins)
        self.add(conf.wins)

        self.play(alpha.increment_value, 1, run_time=animation_time)
        self.wait()

    def animate_versus(self):
        """Animation of the confrontation between teams (1-8, 2-7, ...)"""
        alpha = ValueTracker(0)
        amount_x = np.array([1, 0, 0])
        amount_y = np.array([0, .8, 0])
        start_west = np.array([-5.82, 2.05, 0]) - amount_x
        start_east = np.array([1.26, 2.05, 0]) - amount_x
        end_west = np.array([-5.82, -3.47, 0]) - amount_x
        end_east = np.array([1.26, -3.47, 0]) - amount_x

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
        """Moving teams next to their opponents
        """

        self.groups_east = Group()
        self.groups_west = Group()
        for i in range(8):
            east_line = Group(self.rankings_east[i], self.east.teams[i],
                              self.east.wins[i], self.east.losses[i])
            west_line = Group(self.rankings_west[i], self.west.teams[i],
                              self.west.wins[i], self.west.losses[i])
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
        self.wait()


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
            UP, False, False, buff=.65)
        self.west.wins.arrange_submobjects(
            UP, False, False, buff=.65)
        self.east.losses.arrange_submobjects(
            UP, False, False, buff=.65)
        self.west.losses.arrange_submobjects(
            UP, False, False, buff=.65)

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
        self.finals_animation()
        self.victory_animation()

    def reorganize_teams(self):
        """A team reorganization so that it will be usable with range indexes 
        in future animations"""
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
        """Moving confs to make space for latter animations"""
        east_bloc = self.east_west_confs[:2]
        west_bloc = self.east_west_confs[2:]
        self.play(east_bloc.shift, 4 * RIGHT,
                  west_bloc.shift, 4 * LEFT)

    def to_playoffs_positions(self):
        """This creates and plays the animation consisting of moving from 
        a ranking to 1 vs 1 matchups
        """
        self.matches_east = Group()
        self.matches_west = Group()
        for i in [0, 2, 4, 6]:
            match_east = Group(self.east.teams[i:i + 2])
            self.matches_east.add(match_east)
        for i in [0, 2, 4, 6]:
            match_west = Group(self.west.teams[i:i + 2])
            self.matches_west.add(match_west)

        self.play(self.matches_east.shift, 1.33 * UP + LEFT)
        self.play(self.matches_west.shift, 1.33 * UP + 4 * RIGHT)
        self.play(self.matches_east.arrange_submobjects,
                  DOWN, False, False, {"buff": .7},
                  self.matches_west.arrange_submobjects,
                  DOWN, False, False, {"buff": .7})

    def versus_animation(self, teams, winners_list, scores, direction=RIGHT, save=False):
        """A function that create VersusLines between each two teams in a 
        group object
        Parameters
        ----------
        teams:`Group`
            A Group containing teams Avatar object, it's a nested group (group 
            of groups (2 teams in each subgroup)).
        winners_list: `list`
            A list of 1s and 0s o determine a winner in a two-teams group
        direction: `np.array`.
            an array for the direction of versus lines eg. RIGHT for the eastern
            conference and LEFT for the western conference.
        Returns
        -------
        res_teams: Group
            A nested group containing the remaining teams (the winners).

        """
        # Distance from the Team image to the beginning of the line.
        bias = .4 * direction
        # This will hold the return value
        res_teams = Group()
        faceoff = Group()
        for i in teams:
            first, second = i[0]
            start, end = first.get_center() + bias, second.get_center() + bias
            versus_line = VersusLines(start, end, direction=direction)
            last_point = versus_line.last_point
            # adding the scores
            score = scores.pop(0)
            scores_text = [NumberAnimation(
                score[i], versus_line.main_lines[i]) for i in (0, 1)]
            self.play(ShowCreation(versus_line))
            self.add(*scores_text)
            self.play(scores_text[0].animation, scores_text[1].animation)
            winner = i[0][winners_list.pop(0)]
            winner_copy = winner.copy()
            self.play(winner_copy.move_to, last_point + .3 * direction)
            faceoff.add(winner_copy)
        # This is for creating a group of two-teams subgroups
        for i in range(0, len(faceoff) // 2 + 1, 2):
            res_teams.add(Group(faceoff[i:i + 2]))
        if save:
            self.versus_lines.add(versus_line)
        return res_teams

    def start_versus(self):
        """This is the main fonction for the playoffs series, we feed 
        `versus_animation` with the necessary data (winners in each step and 
        keeping a `Group` of remaining teams )
        """
        # Will be used to store the last versus lines (to remove them after)
        self.versus_lines = VGroup()
        scores_west_first_round = [(4, 2), (2, 4), (4, 1), (3, 4)]
        scores_east_first_round = [(4, 0), (0, 4), (4, 1), (1, 4)]
        scores_west_second_round = [(4, 2), (4, 3)]
        scores_east_second_round = [(4, 1), (3, 4)]
        scores_west = [scores_west_first_round,
                       scores_west_second_round, [(4, 0)]]
        scores_east = [scores_east_first_round,
                       scores_east_second_round, [(4, 2)]]

        next_round_east = [0, 1, 0, 1]
        semi_finals_east = [0, 1]
        winners_east = [next_round_east, semi_finals_east, [1]]

        next_round_west = [0, 1, 0, 1]
        semi_finals_west = [0, 0]
        winners_west = [next_round_west, semi_finals_west, [0]]

        next_teams_east = self.matches_east
        for i in range(3):
            next_teams_east = self.versus_animation(
                next_teams_east, winners_east[i], scores_east[i], save=(i == 2))

        next_teams_west = self.matches_west
        for i in range(3):
            next_teams_west = self.versus_animation(
                next_teams_west, winners_west[i], scores_west[i],
                direction=LEFT, save=(i == 2))
        self.final_east = next_teams_east[0][0]
        self.final_west = next_teams_west[0][0]

    def finals_animation(self):
        finalists = Group(self.final_east, self.final_west)
        x_center = .5
        y_center = .0
        self.final_west.set_x(x_center)
        self.final_east.set_x(-x_center)
        self.camera_frame = self.camera.frame
        self.camera_frame.save_state()
        self.play(
            self.camera_frame.set_width, finalists.get_width() * 2,
            self.camera_frame.move_to, finalists,
            FadeOut(self.versus_lines)
        )

        self.wait()
        finals_logo = Avatar(ASSETS_PATH + "finals_logo.png", 0, 0, .04)
        self.play(
            self.final_east.scale, .45,
            self.final_west.scale, .45,

        )
        finalists = Group(self.final_east, self.final_west)
        finals_box = Rectangle(width=.54, height=.15,
                               fill_color=WHITE, fill_opacity=1)
        finals_box.next_to(finalists, UP, buff=.5)
        finals_logo.move_to(finals_box)

        self.play(FadeIn(finals_box))
        self.play(FadeIn(finals_logo))
        self.wait()

        scenario = [(0, 1), (1, 0), (0, 1), (0, 1), (1, 0), (0, 1)]
        score_east_finalist = Text("0", color=WHITE, font="Digital2").scale(.2)
        score_west_finalist = Text("0", color=WHITE, font="Digital2").scale(.2)

        score_east_finalist.next_to(self.final_east, UP, buff=.2)
        score_west_finalist.next_to(self.final_west, UP, buff=.2)
        font = "DDT W00 Condensed Bold Italic"
        self.games_texts_args = {
            "color": WHITE,
            "font": font,
        }
        game_text = Text("GAME", **self.games_texts_args).scale(.2)
        game_text.next_to(finalists, UP, buff=.15)
        game_number_box = Rectangle(
            width=.2, height=.2, fill_color=WHITE, fill_opacity=1)

        game_number_box.next_to(game_text, DOWN, buff=.06)
        east_count = west_count = 0

        # A little helper function, x: score
        def score_text(x, conference):
            res_text = Text(str(x), color=WHITE, font="Digital2").scale(.2)
            if conference == "east":
                res_text.next_to(self.final_east, UP, buff=.2)
                return ApplyMethod(score_east_finalist.become, res_text)
            else:
                res_text.next_to(self.final_west, UP, buff=.2)
                return ApplyMethod(score_west_finalist.become, res_text)
        games_count = 0
        for i in scenario:
            west, east = i
            east_count += east
            west_count += west

            east_animation = score_text(east_count, "east")
            west_animation = score_text(west_count, "west")
            games_count += 1
            if games_count == 1:
                game_number = Text("1", color="#403c3c", font=font).scale(.2)
                game_number.move_to(game_number_box)
                self.play(
                    east_animation,
                    west_animation,
                    Write(game_text),
                    FadeIn(game_number_box),
                    Write(game_number),
                )
            else:
                new_number = Text(str(games_count),
                                  color="#403c3c", font=font).scale(.2)
                new_number.move_to(game_number_box)
                self.play(
                    east_animation,
                    west_animation,
                    ApplyMethod(game_number.become, new_number)
                )
        # for the next animation
        self.finalists = finalists
        self.game = VGroup(game_number, game_text)
        self.scores = VGroup(score_east_finalist, score_west_finalist)
        self.finals_logobox = Group(finals_logo, finals_box)
        self.wait()

    def victory_animation(self):
        self.finalists[0].plot_depth = 20
        self.finalists[1].plot_depth = 3
        self.game[0].plot_depth = 20
        self.game[1].plot_depth = 20
        self.finals_logobox[0].plot_depth = 20
        self.finals_logobox[1].plot_depth = 20

        self.scores[0].plot_depth = 20
        self.scores[1].plot_depth = 20

        self.background.east_rect.plot_depth = 10
        self.background.west_rect.plot_depth = 2
        cleaning_rect = Rectangle(width=14.2, height=8, fill_color="#1c3f87",
                                  plot_depth=11, fill_opacity=1).set_xy(-7.1, 0)
        champions = Text("NBA CHAMPIONS", plot_depth=20, **
                         self.games_texts_args).scale(.2)
        champions_year = Text("2019", plot_depth=20, color="#b8002c",
                              font="DDT W00 Condensed Bold Italic").scale(.2)
        champions_year.next_to(self.finalists, DOWN, buff=.3)
        champions.move_to(self.game)
        self.add(cleaning_rect)
        self.play(cleaning_rect.scale, 10,
                  Transform(self.game, champions),
                  self.finalists[0].move_to, np.zeros(3),
                  FadeOut(self.scores),)
        self.add(champions)
        self.play(Write(champions_year))
        self.wait()


class Test(Scene):

    def construct(self):
        # second = np.array([1, -2, 0])
        # obj = VersusLines(RIGHT, second)
        # txt = Text("4", color=WHITE).scale(.3)
        # txt.next_to(obj.main_lines[0], UP, buff=.2)
        # self.play(ShowCreation(obj), FadeIn(txt))
        # d = Dot(point=UP, color=RED)
        # num = NumberAnimation(4, d)
        # self.add(num, d)
        # self.play(num.animation)
        # self.wait()
        games_texts_args = {
            "color": BLACK,
            "font": "DDT W00 Condensed Bold Italic",
        }
        game_text = Text("Game", **games_texts_args)
        self.play(Write(game_text))
        self.wait()
