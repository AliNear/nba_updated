from manimlib.imports import *
from projects.nba_update_project.usa_map import NBAScene

from projects.project_one.custom_mobjects import *
from projects.nba_update_project.consts_defs import *
import os
ASSETS_PATH = os.getcwd() + "/projects/nba_update_project/assets/"

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
        self.inter_division()

    def prepare(self):
        self.add_teams("PACIFIC")
        self.teams.set_x(-6)
        self.teams.set_y(2)
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

    def clear_scene(self):
        self.main_team = self.teams[0]
        self.play(
            FadeOut(self.teams[1:]),
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
        # self.play(ShowCreation(self.wl_box))
        # self.play(ShowCreation(self.wins), ShowCreation(self.losses))
        self.wait()

    def add_games_description(self, total=4, home=2, away=2):
        self.total = Text("{0} GAMES".format(total), **self.text_kwargs).scale(1)
        self.total.set_y(-2.0)
        self.home_away = Text("{0} Home, {1} Away".format(home, away), **self.text_kwargs).scale(.8)
        self.home_away.set_y(1.8)
        self.play(Write(self.total),
                  Write(self.home_away))

    def single_matchup(self, index):
        team = self.teams[index]
        team.save_state()
        wins_losses = get_wl(team.name) 
        self.play(
            team.move_to, second_team_pos,
            team.scale, 2
        )
        if index == 1:
            self.add_games_description()
        game_counts = self.updade_games_count([2, 0, 0, 2])
        wins_losses = self.update_win_losses(*wins_losses)
        self.play(
            *game_counts,
            *wins_losses
        )
        self.wait()
        self.play(Restore(team))
        #Team crossing :)
        cross = get_cross_line(Group(team, self.team_names[index]), overflow=.1).set_color(RED)
        team.add(cross)
        self.play(ShowCreation(cross), run_time=.5)


    def begin_matchups(self):
        self.teams[0].save_state()
        self.play(
            self.teams[0].move_to, main_team_pos,
            self.teams[0].scale, 2
        )
        self.wait()
        self.vs_text = Text("VS", font="Strenuous 3D", color=BLACK).scale(1.3)
        self.vs_text.set_y(.3)
        self.play(Write(self.vs_text))
        for i in (1,2):
            self.single_matchup(i)
    
    def inter_division(self):
        self.add_teams("NORTHWEST")
        self.teams.set_y(2)
        self.teams.set_x(-6)
        self.teams.arrange_submobjects(DOWN, False, False, buff=.4)
        
        names = ["Nuggets", "Timberwolves", "Thunder", "Blazers", "Jazz" ]
        self.add_team_names(names)
        self.play(ShowCreation(self.teams))
        self.play(ShowCreation(self.team_names))

# class Test(Scene):
#     def construct(self):
#         icon = Rectangle(fill_color=GREEN, fill_opacity=1)
#         line = get_cross_line(icon )

#         self.play(ShowCreation(icon))
#         self.play(ShowCreation(line))

