from manimlib.imports import *
import os
import re
from projects.project_one.custom_mobjects import *

ASSETS_PATH = os.getcwd() + '/projects/nba_update_project/assets/'
LOADING_COLOR = "#efeff0"

EUROPE = [
    "BE", "GR", "LT", "PT",
    "BG", "ES", "LU", "RO",
    "CZ", "FR", "HU", "SI",
    "DK", "HR", "MT", "SK",
    "DE", "IT", "NL", "FI",
    "EE", "CY", "AT", "SE",
    "IE", "LV", "PL",
]

FOUR_NATIONS = ["FR", "IT", "ES", "GB"]

def create_line_table(text):
    circle = Circle(radius=.15, fill_color=LOADING_COLOR, fill_opacity=1, stroke_width=0)
    circle.set_xy(-.85, 1.75)
    stats_rect = Rectangle(width=1.5, height=.2, fill_color=LOADING_COLOR, fill_opacity=1)
    stats_rect.next_to(circle, RIGHT, buff=.1)
    text = Text(text, font="DDTW00-Italic", color=BLACK).scale(.2)
    text.next_to(circle, LEFT, buff=.1)
    club_line = VGroup(circle, stats_rect, text)
    return club_line  

def get_index_world():
    """This function gets all countries initials (regex), then creates a dict
    with integers (0 - len(initials)) as keys
    """
    expression = "\"[A-Z]{2}\""
    data = open(ASSETS_PATH + "main_world.svg").read()
    matches = re.findall(expression, data)
    initials = [matches[i].strip('"')
                for i in range(len(matches)) if i % 2 == 0]

    return dict(zip(initials, range(len(initials))))

class RankingTable(Mobject):

    def __init__(self, image_name, texts, **kwargs):
        VMobject.__init__(self, **kwargs)
        main_rect = Rectangle(width=2.8, height=4, color=LOADING_COLOR, stroke_width=1)
        icon = Avatar(ASSETS_PATH + 'leagues/' + image_name, 0, 0, .5)
        self.clubs = Group(*[create_line_table(i) for i in texts])
        self.clubs.set_y(1.7)
        self.clubs.arrange_submobjects(DOWN, False, False, buff=.2)
        self.add(self.clubs)
        self.add(main_rect)
        self.add(icon)
    def surround_club(self, index=0, color=RED):
        width = self.clubs[index].get_width()
        height = self.clubs[index].get_height()
        surrounding_rect = Rectangle(width=width, height=height, color=color)
        surrounding_rect.move_to(self.clubs[index])
        return surrounding_rect
    def surround_winner(self):
        return self.surround_club(0, GREEN)
    def surround_losers(self):
        return VGroup(*[self.surround_club(i, RED) for i in range(5, 8)])

        
class MotivationScene(MovingCameraScene):

    def construct(self):
        self.prepare()
        self.draw_map()
        self.show_different_formats()
        self.explanation_soccer_format()
        self.focus_on_europe()
        self.back_to_us()

    def prepare(self):
        """Assests prepation (mainly the world map and a backgroudn?)
        """
        self.world_map = AvatarSVG(ASSETS_PATH + "main_world.svg")
        self.world_map.scale(2)
        self.wait()

    def draw_map(self):
        """Draw the world map"""
        self.play(ShowCreation(self.world_map))

    def show_different_formats(self):
        """Show the different regions (Europe/Asia/Africa/... vs North America)"""
        self.play(self.world_map.color_countries, FOUR_NATIONS)
        texts = ["1", "2", ".", ".", ".", "18", "19", "20"]
        images = os.listdir(ASSETS_PATH + "leagues")
        images.pop(0)
        j = 0
        start = np.array([-4, -2, 0])
        self.rects_winners = VGroup()
        self.rects_losers = VGroup()
        for i in images:
            table = RankingTable(i, texts).scale(.05)
            country = self.world_map.get_country(FOUR_NATIONS[j])
            table.move_to(self.world_map.get_country(FOUR_NATIONS[j]))
            self.play(table.scale, 8,
                      table.move_to, start + 2.7 * j * RIGHT)
            self.rects_winners.add(table.surround_winner())
            self.rects_losers.add(table.surround_losers())
            self.wait()
            j += 1
    
    def explanation_soccer_format(self):
        self.play(ShowCreation(self.rects_winners))
        self.wait()
        self.play(ShowCreation(self.rects_losers))

    def focus_on_europe(self):
        """Show how chamionships are played (and won) in european countries (football)"""
        pass

    def back_to_us(self):
        """Show why it can't be done in the us (big country)"""
        pass

class Test(Scene):

    def construct(self):
        pass


class AvatarSVG(SVGMobject):
    CONFIG = {
        "fill_opacity": 1.0,
        "height": 3,
        "close_new_points": True,
        "stroke_width": .6,
        "stroke_color": BLACK,
    }

    def __init__(self, svg_file="dz.svg", **kwargs):
        self.parts_named = False
        SVGMobject.__init__(self, file_name=svg_file, **kwargs)
        self.countries = get_index_world()

    def name_parts(self):
        self.parts = self.submobjects
        self.parts_named = True

    def copy(self):
        copy_mobject = SVGMobject.copy(self)
        copy_mobject.name_parts()
        return copy_mobject

    def init_colors(self):
        """color initialization for the svg object, can set colors of 
        submobjects too.
        Note: stroke should be set for each submobjet.

        """
        SVGMobject.init_colors(self)
        if not self.parts_named:
            self.name_parts()
        for i in self.parts:
            i.set_color("#f2f2f2")
            i.set_stroke(color=self.stroke_color, width=self.stroke_width)
            self.set_opacity(.5)
        return self

    def color_country(self, country_code, color=RED):
        country_index = self.countries[country_code]
        self.parts[country_index].set_color(color)
    def get_country(self, country_code):
        index = self.countries[country_code]
        return self.parts[index]
    def color_countries(self, countries_codes, color=RED):
        for i in countries_codes:
            self.color_country(i, color=color)
