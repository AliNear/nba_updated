from manimlib.imports import *
import os
import re

ASSETS_PATH = os.getcwd() + '/projects/nba_update_project/assets/'

EUROPE = [
    "BE", "GR", "LT", "PT",
    "BG", "ES", "LU", "RO",
    "CZ", "FR", "HU", "SI",
    "DK", "HR", "MT", "SK",
    "DE", "IT", "NL", "FI",
    "EE", "CY", "AT", "SE",
    "IE", "LV", "PL",
]


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


class MotivationScene(MovingCameraScene):

    def construct(self):
        self.prepare()
        self.draw_map()
        self.show_different_formats()
        self.focus_on_europe()
        self.back_to_us()

    def prepare(self):
        """Assests prepation (mainly the world map and a backgroudn?)
        """
        self.world_map = AvatarSVG(ASSETS_PATH + "main_world.svg")
        self.world_map.scale(2)
        self.play(ShowCreation(self.world_map))
        self.play(self.world_map.color_countries, EUROPE)
        self.wait()

    def draw_map(self):
        """Draw the world map"""
        pass

    def show_different_formats(self):
        """Show the different regions (Europe/Asia/Africa/... vs North America)"""
        pass

    def focus_on_europe(self):
        """Show how chamionships are played (and won) in european countries (football)"""
        pass

    def back_to_us(self):
        """Show why it can't be done in the us (big country)"""
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

    def color_countries(self, countries_codes, color=RED):
        for i in countries_codes:
            self.color_country(i, color=color)
