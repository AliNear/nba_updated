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
            "font": "DDT W00 Condensed Bold Italic",
        },
        "scale_factor": .5,
        "animation_length": 1,

    }

    def __init__(self, next_to_object, spacing=.3, shift=np.zeros(3), direction=RIGHT, **kwargs):
        VMobject.__init__(self, **kwargs)
        self.current_value = 0
        self.number = Text("0", **self.text_kwargs)
        self.number.scale(self.scale_factor)
        self.number.next_to(next_to_object, direction, buff=spacing).shift(shift)
        self.next_to_object = next_to_object
        self.first = True
        self.spacing = spacing
        self.shift = shift
        self.direction = direction
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
            new_number.next_to(self.next_to_object, self.direction, buff=self.spacing).shift(self.shift)
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
        self.title = Text("REGULAR SEASON", **self.title_kwargs).scale(.8)
        self.title.set_xy(0, 3.5)
        self.add_wireframe()
        self.add_divison_title()
        self.add_games_count()
        self.add_win_losses()

    def add_teams(self, division, west=False):
        self.teams = Group()
        if west:
            self.teams_west = Group()
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
                    team.division = TEAMS_POSITIONS[team_name].division
                team.name = team_name
                if west:
                    self.teams_west.add(team)
                else:
                    self.teams.add(team)
                    
    def add_wireframe(self):
        """This method draws the lines that seperates different parts of the scene
        """
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

    def add_divison_title(self):
        self.box = Rectangle(width=3, height=.7, fill_color="#cd8585", fill_opacity=1).set_y(-3.7)
        self.box.set_stroke(width=0)
        self.division_name = Text("PACIFIC DIVISION", **self.text_kwargs).scale(.6)
        self.division_name.move_to(self.box)

    def add_games_count(self):
        """This method add a table like object to hold different games 
        count, ex: In Division, Other Division, ...

        """
        texts = ["In Division", "Other Division", "Other Conference"]
        texts = texts[:3]
        self.categories = VGroup()
        starting_x = 4.5
        starting_y = 2.6
        for i in texts:
            category = Text(i, **self.text_kwargs).scale(.5)
            category.set_y(starting_y)
            category.set_x(starting_x + category.get_width()/2)
            self.categories.add(category)
            starting_y -= .6
        self.categories.set_xy(starting_x, starting_y)
        total_color = "#cd8585"
        total = Text("Total", font="DDT W00 Condensed Bold Italic", color=total_color).scale(.55)
        total.set_y(starting_y - 1.2)
        total.set_x(starting_x - total.get_width())
        self.categories.add(total)
        #Thin line 
        self.box_divider = Line(np.array([6, 1.6, 0]), np.array([6, -0.6, 0]),
                                color="#979797", stroke_width=.5)
        #NumberAnimation objects
        self.numbers = VGroup()
        for i in range(3):
            spacing = 3. - self.categories[i].get_width()
            number = NumberAnimation(self.categories[i], spacing=spacing, animation_length=.3)
            self.numbers.add(number)
        #Not the greatest way to do it, but it works
        self.total_config = {
                "text_kwargs": {
                    "color": total_color,
                    },
                "scale_factor": .55,
                }
        total = NumberAnimation(self.categories[3], spacing = 2.2, animation_length=.3, shift=.13*RIGHT,**self.total_config)
        self.numbers.add(total)

    def updade_games_count(self, counts):
        animations = VGroup()
        for i in range(len(counts)):
            if counts[i] == 0:
                pass
            else:
                increment = self.numbers[i].increment(counts[i])
                animations.add(increment)
        return animations
    def add_win_losses(self):
        x = 3.5
        y = -1.8
        self.wins_text = Text("Wins", **self.text_kwargs).scale(.8)
        self.losses_text = Text("Losses", **self.text_kwargs).scale(.8)
        self.wins_text.set_xy(x + self.wins_text.get_width()/2, y) 
        self.losses_text.set_xy(x + self.losses_text.get_width()/2, y - .8) 
        self.wl_texts = VGroup(self.wins_text, self.losses_text)
        self.wins = NumberAnimation(self.wins_text, 2.2, scale_factor=.8, animation_length=.3)
        self.losses = NumberAnimation(self.losses_text, 1.85, scale_factor=.8, animation_length=.3)
        self.wl_divider = Line(np.array([6, y+.2, 0]), np.array([6, y-1, 0]),
                                color="#979797", stroke_width=.5)
        self.wl_h_divider = Line(np.array([x + .2, y + .7, 0]), np.array([x + 3, y + .7, 0]),
                                color="#979797", stroke_width=.9)
        #
    def update_win_losses(self, wins, losses):
        animations = VGroup()
        animations.add(self.wins.increment(wins))
        animations.add(self.losses.increment(losses))
        return animations

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
        # self.final_transition()
    
    def prepare(self):
        self.map = MapUSA(ASSETS_PATH + "us.svg")
        self.toronto_map = MapUSA(ASSETS_PATH + "toronto.svg").scale(.3)
        self.map.set_x(-0.3)
        self.toronto_map.set_x(5)
        self.toronto_map.set_y(2.8)

        self.play(FadeIn(self.map))
        self.wait()
        self.play(FadeInFrom(self.toronto_map, 4 * UP))

    def general_info(self):
        """Give general information about the NBA, ie: number of teams,
        acronym signification, when did it start, ...
        """
        self.nba = Text("NBA", **self.text_kwargs).scale(1.2).set_y(3.5)
        self.nba_extended = Text("NATIONAL BASKETBALL ASSOCIATION", **self.text_kwargs)
        self.nba_extended.scale(.7).set_y(3.5)
        self.play(Write(self.nba))
        self.wait()
        self.play(Transform(self.nba, self.nba_extended))
        self.wait()
        #Teams
        self.teams_text = Text("30 TEAMS", **self.text_kwargs).scale(.9).set_y(3.5)
        self.play(FadeOut(self.nba))
        self.play(FadeInFrom(self.teams_text, UP))
        self.conf_teams_west = Text("15 TEAMS", **self.text_kwargs).scale(.9).set_xy(5, -.5)
        self.conf_teams_east = self.conf_teams_west.copy().set_x(-5)
        self.conf_teams = VGroup(self.conf_teams_west, self.conf_teams_east)
        #coloring each conference
        self.map.color_east()
        self.toronto_map.color_all()
        self.map.color_west()
        self.wait()
        self.img_east = Avatar(ASSETS_PATH + "east.png", 5, .5, .5)
        self.img_west = Avatar(ASSETS_PATH + "west.png", -5,.5, .5)
        self.play(ApplyMethod(self.map.color_east),
                  ApplyMethod(self.map.color_west),
                  ShowCreation(self.img_east),
                  ShowCreation(self.img_west))
        self.play(Transform(self.teams_text, self.conf_teams))
    # def east_west(self):
    #     """Divide the US map into EASTERN & WESTERN conferences, and 
    #     give some info about both.
    #     """
    
    def teams_conferences(self):
        self.teams.set_x(-5) 
        self.teams.set_y(3.4)
        #Not the best solution, but I experienced a weird bug
        self.play(self.map.shift, 2*RIGHT,
                  FadeOut(self.teams_text),
                  FadeOut(self.conf_teams),
                  FadeOut(self.img_east),
                  FadeOut(self.img_west))
        #self.play(self.conf_teams_west.shift, 2*UP)
        #self.play(self.conf_teams.shift, 2*DOWN)
        self.teams.set_x(-2)
        self.play(self.teams.arrange_in_grid,
                self.teams.shift, 4*LEFT)
        self.wait()
        r = Rectangle(height=self.teams.get_height(), width=self.teams.get_width(),color=RED)
        r.move_to(self.teams)
        r.surround(self.teams, 1)
        self.play(ShowCreationThenDestruction(r), run_time=2)
        self.camera_frame = self.camera.frame
        self.camera_frame.save_state()
        self.play(
            self.camera_frame.set_width, self.teams.get_width()*1.1,
            self.camera_frame.set_height, self.teams.get_height()*1.1,
            self.camera_frame.move_to, self.teams
        )
        self.wait()
        self.play(Restore(self.camera_frame))
        self.wait()

        """Add each team to its conference"""
        for i in range(0, 25, 6): 
            animation = [ApplyMethod(i.move_to, np.array([i.position[0]+2,i.position[1],0])) for i in self.teams[i:i+6]]
            self.play(*animation)
            # i.move_to(np.array([i.position[0]+2,i.position[1],0]))

        self.wait()
    def add_to_division(self):
        self.img_division = {
            "PACIFIC": Group(),
            "ATLANTIC": Group(),
            "CENTRAL": Group(),
            "SOUTHEAST": Group(),
            "SOUTHWEST": Group(),
            "NORTHWEST": Group(),
        }

        for i in self.teams:
            self.img_division[i.division].add(i)

    def to_division(self):
        """Divide the map into the six (06) divisions"""
        self.add_to_division()
        self.play(self.map.shift, 2 * LEFT,
                  self.teams.shift, 2 * LEFT,
                  self.toronto_map.shift, 2 * LEFT)
        amount = 1.8
        self.division_texts = VGroup()
        def move_division(division, direction, div_str):
            #Not really proud of this one
            text = Text(div_str + "\nDIVISION", **self.text_kwargs).scale(.6).move_to(1.85 * amount * direction)
            if div_str != "ATLANTIC":
                self.play(
                    self.map.move_portion, division, direction,
                    self.img_division[div_str].shift, direction,
                    Write(text)
                )
            else:
                self.play(
                    self.map.move_portion, division, direction,
                    self.img_division[div_str].shift, direction,
                    Write(text),
                    self.toronto_map.shift, .6 * UP + amount * RIGHT
                )
            if div_str != PACIFIC:
                self.division_texts.add(text)
        move_division(SOUTHEAST, DOWN + amount * RIGHT, "SOUTHEAST")
        move_division(SOUTHWEST, DOWN, "SOUTHWEST")
        move_division(PACIFIC, DOWN + amount * LEFT, "PACIFIC")
        move_division(NORTHWEST, UP + amount * LEFT, "NORTHWEST")
        move_division(CENTRAL, UP, "CENTRAL")
        move_division(ATLANTIC, UP + amount * RIGHT, "ATLANTIC")
    
    def final_transition(self):
        self.play(FadeOut(self.division_texts))
        removed_imgs = Group()
        self.pacific = Group()
        for i in self.img_division.keys():
            if i != "PACIFIC":
                removed_imgs.add(self.img_division[i])
            else:
                self.pacific.add(self.img_division[i])
        
        self.play(FadeOut(removed_imgs))
        self.play(FadeOut(self.map))
        self.pacific[0].set_xy(-6, 1)
        self.play(self.pacific[0].arrange_submobjects, DOWN, False, False, {"buff":.4})
        

class Test(Scene):
    def construct(self):
        line = Line(start=20*LEFT, end=20*RIGHT, color=BLACK)
        line = DashedVMobject(line, num_dashes = 130)
        l = Line(start=ORIGIN, end=4*RIGHT)
        self.play(ShowCreation(l))
        self.play(line.shift, 5 * RIGHT, run_time=4, rate_func=lambda t: t)
