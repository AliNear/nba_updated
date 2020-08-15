from manimlib.imports import *
from projects.project_one.custom_mobjects import *
from projects.nba_update_project.consts_defs import *
import os
ASSETS_PATH = os.getcwd() + "/projects/nba_update_project/assets/"
MAP_FILE = "us.svg"

class NumberAnimation(VMobject):
    """A `Text` object that has an animation bound to a ValueTracker
    """
    CONFIG = {
        "text_kwargs": {
            "color": "#403c3c",
            "font": "Fjalla One",
        },
        "scale_factor": .3,
        "animation_length": 1,

    }

    def __init__(self, next_to_object, spacing=.3, **kwargs):
        VMobject.__init__(self, **kwargs)
        self.current_value = 0
        self.number = Text("0", **self.text_kwargs)
        self.number.scale(self.scale_factor)
        self.number.next_to(next_to_object, RIGHT, buff=spacing)
        self.next_to_object = next_to_object
        self.first = True
        self.spacing = spacing
        self.add(self.number)
    def increment(self, amount):
        alpha = ValueTracker(0)
        self.old_alpha = 0
        if not self.first: self.number.updaters.pop(0)
        def updater(t):
            self.current_value = self.current_value + (alpha.get_value() - self.old_alpha) * amount
            new_number = Text(
                    str(int(self.current_value)), **self.text_kwargs)
            new_number.scale(self.scale_factor)
            new_number.next_to(self.next_to_object, RIGHT, buff=self.spacing)
            #new_number.set_xy(self.x, self.y)
            t.become(new_number)
            self.old_alpha = alpha.get_value()

        self.number.add_updater(updater)

        self.add(self.number)
        self.animation = ApplyMethod(
            alpha.increment_value, 1, run_time=self.animation_length)
        self.first = False
        return self.animation 



class NBAScene(MovingCameraScene):
    CONFIG = {
            "text_kwargs": {
                "font": "DDT W00 Condensed Bold Italic",
                "color":"#403c3c",
                },
            "title_kwargs": {
                "font": "DDT W00 Condensed Bold Italic",
                "color": BLACK,
                },
            "background_img": ASSETS_PATH + "background.png",
            "normal_team_scale": .25,
            "zoomed_team_scale": .35,
            }
    def __init__(self, **kwargs):
        MovingCameraScene.__init__(self, **kwargs)
    def setup(self):
        self.background = Avatar(self.background_img, 0, 0, 6, plot_depth=-10)
        self.add(self.background)
        self.title = Text("REGULAR SEASON", **self.title_kwargs).scale(.5)
        self.title.set_xy(0, 3.5)
        self.add_wireframe()
        self.add_games_count()

    def add_teams(self, division):
        self.teams = Group()
        all_files = os.listdir(ASSETS_PATH + '/teams')
        all_files = [i for i in all_files if i.startswith('.') is False]

        skip_check = (division == "ALL")

        for i in all_files:
            team_name = i.split('.')[0]
            if TEAMS_POSITIONS[team_name].division == division or skip_check:
                name = ASSETS_PATH + '/teams/' + i.split('.')[0]
                team = Avatar(name, 0, 0, .25)
                if skip_check:
                    team.position = TEAMS_POSITIONS[team_name].pos
                self.teams.add(team)
                    
    def add_wireframe(self):
        y_main_line = 2.8
        x_main_dividers = 3
        y_upper_team_divider = 1.13
        y_lower_teal_divider = -.61
        self.main_line = Line(np.array([-10, y_main_line, 0]), 
                              np.array([10, y_main_line, 0]),
                              color=BLACK, stroke_width=3)
        left_divider = Line(np.array([-x_main_dividers, y_main_line, 0]), 
                            np.array([-x_main_dividers, -10, 0])
                            , color=BLACK, stroke_width=2)
        right_divider = left_divider.copy().set_x(x_main_dividers)
        upper_team_divider = Line(np.array([-x_main_dividers, y_upper_team_divider, 0]), 
                np.array([x_main_dividers, y_upper_team_divider, 0]), color=BLACK, stroke_width=1)
        lower_team_divider = upper_team_divider.copy().set_y(y_lower_teal_divider)
        self.main_dividers = VGroup(left_divider, right_divider)
        self.team_dividers = VGroup(upper_team_divider, lower_team_divider)
        self.wireframe = VGroup(self.main_dividers, self.main_line, self.team_dividers)
    def add_games_count(self, count=3):
        """This method add a table like object to hold different games 
        count, ex: In Division, Other Division, ...

        """
        texts = ["In Division", "Other Division", "Other Conference"]
        texts = texts[:3]
        self.categories = VGroup()
        starting_x = 4.5
        starting_y = 2.3
        for i in texts:
            category = Text(i, **self.text_kwargs).scale(.3)
            category.set_y(starting_y)
            category.set_x(starting_x + category.get_width()/2)
            self.categories.add(category)
            starting_y -= .6
        self.categories.set_xy(starting_x, starting_y)
        total_color = "#cd8585"
        total = Text("Total", font="DDTW00-CondensedBoldItalic", color=total_color).scale(.35)
        total.set_y(starting_y - 1.2)
        total.set_x(starting_x - total.get_width())
        self.categories.add(total)
        #Thin line 
        self.box_divider = Line(np.array([6, 1.3, 0]), np.array([6, -1., 0]),
                                color="#979797", stroke_width=.5)
        #NumberAnimation objects
        self.numbers = VGroup()
        for i in range(3):
            spacing = 3. - self.categories[i].get_width()
            number = NumberAnimation(self.categories[i], spacing=spacing)
            self.numbers.add(number)
        #Not the greatest way to do it, but it works
        self.total_config = {
                "text_kwargs": {
                    "color": total_color,
                    },
                "scale_factor": .35,
                }
        total = NumberAnimation(self.categories[3], spacing = 2.2, **self.total_config)
        self.numbers.add(total)

class MainMapScene(NBAScene):
    CONFIG = {
            "text_kwargs": {
                "font": "DDT W00 Condensed Bold Italic",
                "color": BLACK,
                },
            "background": ASSETS_PATH + "background.png",
            }
    def construct(self):
        self.prepare()
        self.general_info()
        self.add_teams("ALL")
        self.teams_conferences()
        self.to_division()
    
    def prepare(self):
        self.map = MapUSA(ASSETS_PATH + "us.svg")
        self.map.set_x(-0.3)
        self.play(FadeIn(self.map))

    def general_info(self):
        """Give general information about the NBA, ie: number of teams,
        acronym signification, when did it start, ...
        """
        self.nba = Text("NBA", **self.text_kwargs).scale(.7).set_y(3.5)
        self.nba_extended = Text("NATIONAL BASKETBALL ASSOCIATION", **self.text_kwargs)
        self.nba_extended.scale(.5).set_y(3.5)
        self.play(Write(self.nba))
        self.wait()
        self.play(Transform(self.nba, self.nba_extended))
        self.wait()
        #Teams
        teams = Text("30 TEAMS", **self.text_kwargs).scale(.6).set_y(3.5)
        self.play(FadeOut(self.nba))
        self.play(FadeInFrom(teams, UP))
        conf_teams_west = Text("15 TEAMS", **self.text_kwargs).scale(.6).set_xy(5, -.5)
        conf_teams_east = conf_teams_west.copy().set_x(-5)
        conf_teams = VGroup(conf_teams_west, conf_teams_east)
        #coloring each conference
        self.map.color_east()
        self.map.color_west()
        self.wait()
        self.wait()
        self.play(Transform(teams, conf_teams))
        

    # def east_west(self):
    #     """Divide the US map into EASTERN & WESTERN conferences, and 
    #     give some info about both.
    #     """
    #     pass
    
    def teams_conferences(self):
        self.teams.set_x(-5) 
        self.teams.set_y(3.4)
        self.play(self.teams.arrange_in_grid,2, 15)
        self.wait()
        """Add each team to its conference"""

    def to_division(self):
        """Divide the map into the six (06) divisions"""
        pass

class Test(NBAScene):
    def construct(self):
        self.play(Write(self.title))
        self.play(ShowCreation(self.wireframe))
        self.play(ShowCreation(self.categories))
        self.play(ShowCreation(self.box_divider))
        self.play(ShowCreation(self.numbers))
        self.play(self.numbers[0].increment(20))
        self.wait()
