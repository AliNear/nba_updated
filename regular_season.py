from manimlib.imports import *
from projects.nba_update_project.usa_map import NBAScene

from projects.project_one.custom_mobjects import *
from projects.nba_update_project.consts_defs import *
import os
ASSETS_PATH = os.getcwd() + "/projects/nba_update_project/assets/"

main_team_pos = np.array([-1.4, .25, 0])
second_team_pos = np.array([1.4, .25, 0])
def get_wl(name):
    for i in SCORES.keys():
        if i.find(name) != -1:
            wl = SCORES[i]
            return (wl.count('W'), wl.count('L'))

class DivisionScene(NBAScene):
    CONIFG = {
        "main_team_pos": np.array([-1.4, .25, 0]),
        "second_team_pos": np.array([1.4, .25, 0]),
    }
    def __init__(self, **kwargs):
        NBAScene.__init__(self, **kwargs)
    def construct(self):
        self.prepare()
        self.draw_foundation()
        self.begin_matchups()
    def prepare(self):
        self.add_teams("PACIFIC")
        self.teams.set_x(-6)
        self.teams.set_y(2)
        self.teams.arrange_submobjects(DOWN, False, False, buff=.4)
        names = ["Kings", "Suns", "Clippers", "Lakers", "Warriors"]
        names.reverse()
        self.team_names = VGroup(*[Text(i.upper(), **self.text_kwargs).scale(.4) for i in names])
        self.team_names.arrange_submobjects(DOWN, False, False, buff=.75)
        self.team_names.set_xy(-5., .2)
    def draw_foundation(self):
        self.play(ShowCreation(self.teams), ShowCreation(self.team_names))
        self.play(Write(self.title))
        self.play(ShowCreation(self.wireframe))
        self.play(ShowCreation(self.categories))
        self.play(ShowCreation(self.box_divider))
        self.play(ShowCreation(self.numbers))
        self.wait()

    def single_matchup(self, index):
        team = self.teams[index]
        team.save_state()
        wins_losses = get_wl(team.name) 
        self.play(
            team.move_to, second_team_pos,
            team.scale, 2
        )
        game_counts = self.updade_games_count([2, 0, 0, 2])
        self.play(
            *game_counts
        )
        self.wait()
        self.play(Restore(team))


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
