from manimlib.imports import *
from projects.nba_update_project.usa_map import NBAScene
from projects.nba_update_project.nba_update import TwoRects
from projects.project_one.custom_mobjects import *
from projects.nba_update_project.consts_defs import *
import os
ASSETS_PATH = os.getcwd() + "/projects/nba_update_project/assets/"
DIVISION_COUNT = 5
CONFERENCE_COUNT = 15 
main_team_pos = np.array([-1.4, .25, 0])
second_team_pos = np.array([1.4, .25, 0])
def get_wl(name):
    # print (name)
    for i in SCORES.keys():
        if name.find(i) != -1:
            wl = SCORES[i]
            return (wl.count('W'), wl.count('L'))

def get_cross_line(obj, overflow=.2):
    center = obj.get_center()
    width = obj.get_width() * RIGHT/2
    start = center - width - (overflow * RIGHT)
    end = center + width + (overflow * RIGHT)
    return Line(start, end)
class Conference:
    def __init__(self, teams, wins):
        self.teams = teams
        self.wins_raw = wins
        self.losses_raw = [(82-i) for i in wins]

class DivisionScene(NBAScene):
    CONIFG = {
        "main_team_pos": np.array([-1.4, .25, 0]),
        "second_team_pos": np.array([1.4, .25, 0]),
    }
    def __init__(self, **kwargs):
        NBAScene.__init__(self, **kwargs)
    def construct(self):
        #For the in division games
        self.prepare()
        self.draw_foundation()
        self.begin_matchups()
        self.clear_scene()
        #for the inter-division games
        self.inter_division("NORTHWEST", names=NORTHWEST_NAMES)
        self.wait()
        self.clear_scene(False)
        self.inter_division("SOUTHWEST", names=SOUTHWEST_NAMES)
        self.clear_scene(False)
        self.wait()
        self.eatern_conf()
    def prepare(self):
        self.add_teams("PACIFIC")
        self.teams.set_x(-6)
        self.teams.set_y(1)
        self.teams.arrange_submobjects(DOWN, False, False, buff=.4)
        names = ["Kings", "Suns", "Clippers", "Lakers", "Warriors"]
        names.reverse()
        self.add_team_names(names)

    def add_team_names(self, names):
        """Given a list of names, this method creates text objects of the names and add them 
        to their dedicated position
        """
        self.team_names = VGroup(*[Text(i.upper(), **self.text_kwargs).scale(.4) for i in names])
        y = self.teams[0].get_y()
        x = -5.5
        for i in self.team_names:
            i.set_xy(x + i.get_width()/2, y)
            y -= .9

    def clear_scene(self, first=True):
        i = 0
        if first:
            self.main_team = self.teams[0]
            i = 1
        self.play(
            FadeOut(self.teams[i:]),
            FadeOut(self.team_names),
            FadeOut(self.total),
            FadeOut(self.home_away)
        )
 
    def draw_foundation(self):
        self.play(ShowCreation(self.teams), ShowCreation(self.team_names))
        self.play(Write(self.title))
        self.play(ShowCreation(self.wireframe))
        self.play(FadeInFrom(self.box, 7 * DOWN))
        self.play(FadeInFrom(self.division_name, 7 * DOWN))
        self.play(ShowCreation(self.categories))
        self.play(ShowCreation(self.box_divider))
        self.play(ShowCreation(self.numbers))
        self.play(ShowCreation(self.wl_texts))
        self.play(ShowCreation(self.wl_divider), ShowCreation(self.wl_h_divider))
        self.play(ShowCreation(self.wins), ShowCreation(self.losses))
        self.wait()

    def add_games_description(self, home=2, away=2):
        total = home + away
        self.total = Text("{0} GAMES".format(total), **self.text_kwargs).scale(1)
        self.total.set_y(-2.0)
        self.home_away = Text("{0} Home, {1} Away".format(home, away), **self.text_kwargs).scale(.8)
        self.home_away.set_y(1.8)
        self.play(Write(self.total),
                  Write(self.home_away))

    def single_matchup(self, index, start=1, home=2, away=2, field=0):
        total = home + away
        team = self.teams[index]
        team.save_state()
        wins_losses = get_wl(team.name) 
        self.play(
            team.move_to, second_team_pos,
            team.scale, 2,
        )
        if index == start:
            if hasattr(self, "total"):
                self.play(FadeOut(self.total), FadeOut(self.home_away))
            self.add_games_description(home, away)
        games = [0, 0, 0, total]
        games[field] = total
        game_counts = self.updade_games_count(games)
        wins_losses = self.update_win_losses(*wins_losses)
        self.play(
            *game_counts,
            *wins_losses,
        )
        self.wait()
        self.play(
            Restore(team),
        )
        #Team crossing :)
        if self.team_names == None:
            team_box = team
        else:
            team_box = Group(team, self.team_names[index])
        cross = get_cross_line(team_box, overflow=.1).set_color("#D13C46")
        team.add(cross)
        self.play(ShowCreation(cross), run_time=.5)


    def begin_matchups(self):
        self.my_run_time = 1
        self.teams[0].save_state()
        self.play(
            self.teams[0].move_to, main_team_pos,
            self.teams[0].scale, 2,
        )
        self.wait()
        self.vs_text = Text("VS", font="Strenuous 3D", color=BLACK).scale(1.3)
        self.vs_text.set_y(.3)
        self.play(Write(self.vs_text))
        for i in range(1,DIVISION_COUNT):
            self.single_matchup(i)
    
    def inter_division(self, division, names=None):
        self.add_teams(division)
        self.teams.set_y(1)
        self.teams.set_x(-6)
        self.teams.arrange_submobjects(DOWN, False, False, buff=.4)
        new_division_name = Text(division + " DIVISION", **self.text_kwargs).scale(.6)
        new_division_name.move_to(self.box)
        if names != None:
            self.add_team_names(names)
        self.play(Transform(self.division_name, new_division_name))
        self.play(ShowCreation(self.teams))
        self.play(ShowCreation(self.team_names))
        # self.division_name = new_division_name
        self.remove(new_division_name)
        home_away = [[2,2], [2,2], [2,2], [2,1], [2,1]]
        for i in range(DIVISION_COUNT):
            h, a = home_away[i]
            #This is just to change the games desciption when passing to 3 games
            start = (i // 3) * 3
            self.single_matchup(i, start=start, home=h, away=a, field=1)
        
    def eatern_conf(self):
        self.my_run_time = .2
        self.add_teams("ATLANTIC")
        teams = self.teams
        self.team_names = None
        self.add_teams("CENTRAL")
        teams = Group(*teams, *self.teams)
        self.add_teams("SOUTHEAST")
        teams = Group(*teams, *self.teams)
        self.teams = teams
        self.teams.set_xy(-6.2, -3)
        self.teams.arrange_in_grid(buff=.5)
        self.teams.shift(.7 * DOWN)
        new_name = Text("EASTERN CONFERENCE", **self.text_kwargs).scale(.6)
        new_name.move_to(self.box)
        self.play(ShowCreation(self.teams))
        self.play(Transform(self.division_name, new_name))
        for i in range(CONFERENCE_COUNT):
            self.single_matchup(i, start=0, home=1, away=1, field=2)
        self.wait()

class EndRegularSeason(NBAScene):
    CONFIG = {
        "numbers_args": {
            "font": "DDT W00 Condensed Bold Italic",
            "color": WHITE,
        }
    }

    def __init__(self, **kwargs):
        NBAScene.__init__(self, **kwargs)
    def construct(self):
        self.prepare()
        # self.add_foundation()
        # self.update_numbers()
        # self.clear_scene()
        self.rearrange_teams(self.teams, EASTERN_CONF_RANKING)
        self.rearrange_teams(self.teams_west, WESTERN_CONF_RANKING, east=False)
        self.animate_east()
        #self.add_wl()
        self.to_playoffs()

    def prepare(self): 

        #Western Conference
        self.add_teams("PACIFIC", west=True)
        west_teams = self.teams_west
        self.add_teams("NORTHWEST", west=True)
        west_teams = Group(*west_teams, *self.teams_west)
        self.add_teams("SOUTHWEST", west=True)
        west_teams = Group(*west_teams, *self.teams_west)
        self.teams_west = west_teams
        #Eastern Conference
        self.add_teams("ATLANTIC")
        teams = self.teams
        self.team_names = None
        self.add_teams("CENTRAL")
        teams = Group(*teams, *self.teams)
        self.add_teams("SOUTHEAST")
        teams = Group(*teams, *self.teams)
        self.teams = teams
        self.teams.set_xy(-6.2, -3)
        self.teams.arrange_in_grid(buff=.5)
        self.teams.shift(.7 * DOWN)
        self.add_playoffs_mobjects()
    

    def add_foundation(self):
        new_division_name = Text("EASTERN CONFERENCE", **self.text_kwargs).scale(.6)
        new_division_name.move_to(self.box)
        self.division_name.become(new_division_name)
        self.remove(new_division_name)
        self.add(self.teams)
        self.add(self.title)
        self.add(self.wireframe)
        self.add(self.box)
        self.add(self.division_name)
        self.add(self.categories)
        self.add(self.box_divider)
        self.add(self.numbers)
        self.add(self.wl_texts)
        self.add(self.wl_divider, self.wl_h_divider)
        self.add(self.wins, self.losses)

    def update_numbers(self):
        animations = self.updade_games_count([16, 36, 30, 82])
        self.play(*animations)
        animations = self.update_win_losses(57, 25)
        self.play(*animations)
        self.wait()

    def clear_scene(self):
        self.play(FadeOut(self.wireframe))
        self.play(FadeOut(self.box), FadeOut(self.division_name))
        self.play(FadeOut(self.categories), FadeOut(self.numbers), FadeOut(self.box_divider))
        self.play(FadeOut(self.wl_texts), FadeOut(self.wl_divider), FadeOut(self.wl_h_divider))
        self.play(FadeOut(self.wins), FadeOut(self.losses))

    def add_playoffs_mobjects(self):
        box_east = Rectangle(
            fill_color=WHITE, fill_opacity=1, width=1.1, height=.7)
        x_box, y_box = 6, 3.5
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


    def rearrange_teams(self, teams, ranking, east=True):
        new_teams = [i for i in range(15)]
        for i in teams:
            for j in range(15):
                if i.name.find(ranking[j]) != -1:
                    new_teams[j] = i
        if east:
            self.teams = Group(*new_teams)
        else:
            self.teams_west = Group(*new_teams)

    def animate_east(self):
        self.play(self.teams.scale, .7)
        self.teams_west.scale(.7)
        texts = [Text(str(i) + ".", **self.numbers_args).scale(.3)
                 for i in range(1, 16)]
        self.x_east = 2
        self.x_west = -(FRAME_WIDTH / 2 - 2)
        self.y_conf = 3.05
 
        self.rankings_east = VGroup(*texts)
        self.rankings_east.set_xy(self.x_east - .5, self.y_conf)  # 2.02
        self.rankings_east.arrange_submobjects(DOWN, False, False, buff=.365)
        self.rankings_west = self.rankings_east.copy().set_x(self.x_west - .5)
        self.teams_west.set_xy(self.x_west, self.y_conf)
        self.play(self.teams.arrange_submobjects, DOWN, False, False, {"buff":.13})
        
        vector = 2 * RIGHT + .3 * DOWN
        self.play(self.teams.move_to, vector)
        self.play(self.teams_west.arrange_submobjects, DOWN, False, False, {"buff":.13})
        self.wait()
        self.bg = TwoRects(plot_depth=-10)
        self.play(FadeInFrom(self.bg, 5 * DOWN))
        self.play(FadeInFrom(self.east_west_confs,
                             direction=3 * UP, rate_function=rush_into))

        self.play(FadeIn(self.rankings_east), FadeIn(self.rankings_west))
        self.wait()
    def add_wl(self):
        y_titles = 3.5
        wins_title_east = Text("W", **self.numbers_args).scale(.45)
        wins_title_east.set_xy(self.x_east + 1, y_titles)
        losses_title_east = Text("L", **self.numbers_args).scale(.45)
        losses_title_east.set_xy(self.x_east + 2, y_titles)
        wins_title_west = wins_title_east.copy().set_x(self.x_west + 1)
        losses_title_west = losses_title_east.copy().set_x(self.x_west + 2)

        self.wins_losses = VGroup(wins_title_east, losses_title_east,
                                  wins_title_west, losses_title_west)

        self.eastern_conf = Conference(self.teams, EASTERN_CONF_WINS)
        self.western_conf = Conference(self.teams_west, WESTERN_CONF_WINS)
        wl_numbers = VGroup(*[Text("00", **self.numbers_args).scale(.3)
                 for i in range(1, 16)])
        east_wins = wl_numbers.copy()
        east_losses = wl_numbers.copy()
        west_wins = wl_numbers.copy()
        west_losses = wl_numbers.copy()
        
        east_wins.set_xy(self.x_east + 1, self.y_conf)
        east_losses.set_xy(self.x_east + 2, self.y_conf)
        west_wins.set_xy(self.x_west + 1, self.y_conf)
        west_losses.set_xy(self.x_west + 2, self.y_conf)

        self.eastern_conf.wins = east_wins
        self.eastern_conf.losses = east_losses
        self.western_conf.wins = west_wins
        self.western_conf.losses = west_losses


        self.play(FadeInFrom(self.wins_losses, 3 * UP))
        self.animate_numbers(self.eastern_conf, .1)
        self.animate_numbers(self.western_conf, .1)

    def to_playoffs(self):
        y_divider = -.5
        x_start_east = -6
        x_start_west = 1.1
        length = 3.5
        start_east = np.array([x_start_east, y_divider, 0])
        end_east = start_east + length * RIGHT
        start_west = np.array([x_start_west, y_divider, 0])
        end_west = start_west + length * RIGHT
        east_divider = Line(start_east, end_east, color=WHITE)
        west_divider = Line(start_west, end_west, color=WHITE)
        dividers = VGroup(east_divider, west_divider)
        self.play(ShowCreation(dividers))
        
        self.play(FadeInFrom(self.playoffs,
                             direction=UP, rate_function=rush_into))
        east_rearrange = ApplyMethod(self.teams.arrange_submobjects, DOWN, False, False, buff=.3) 
        west_rearrange = ApplyMethod(self.teams_west.arrange_submobjects, DOWN, False, False, buff=.3) 
        east_text_rearrange = ApplyMethod(self.rankings_east.arrange_submobjects, DOWN, False, False, buff=.6) 
        east_down = ApplyMethod(self.teams.shift, 2 * DOWN)
        west_down = ApplyMethod(self.teams_west.shift, 2 * DOWN)
        self.play(east_rearrange, west_rearrange, east_down, west_down)
        self.play(self.teams.scale, 1/.7,
                  self.teams_west.scale, 1/.7,
                  self.rankings_east.scale, 4/3)
 
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
                txt = str(int(alpha.get_value() * 50))
                i.become(
                    Text(txt, **self.numbers_args).set_xy(x, y).scale(.4)
                )
                j += 1

        conf.losses.arrange_submobjects(DOWN, False, False, buff=.365)
        conf.losses.add_updater(updater_losses)
        self.add(conf.losses)

        conf.wins.arrange_submobjects(DOWN, False, False, buff=.365)
        conf.wins.add_updater(updater_wins)
        self.add(conf.wins)

        self.play(alpha.increment_value, 1, run_time=animation_time)
        self.wait()



# class Test(Scene):
#     def construct(self):
#         icon = Rectangle(fill_color=GREEN, fill_opacity=1)
#         line = get_cross_line(icon )

#         self.play(ShowCreation(icon))
#         self.play(ShowCreation(line))

