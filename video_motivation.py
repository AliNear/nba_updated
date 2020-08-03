from manimlib.imports import *
import os
import re
ASSETS_PATH = os.getcwd() + '/projects/nba_update_project/assets/'


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
        self.play(self.world_map.color_country, "DZ")
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
        "stroke_width": 1,
        "stroke_color": BLACK,
    }

    def __init__(self, file_name="dz.svg", **kwargs):
        self.parts_named = False
        self.svg_file = file_name
        SVGMobject.__init__(self, file_name=self.svg_file, **kwargs)
        self.countries = get_index_world()

    def name_parts(self):
        self.parts = self.submobjects
        self.parts_named = True

    def copy(self):
        copy_mobject = SVGMobject.copy(self)
        copy_mobject.name_parts()
        return copy_mobject

    def init_colors(self):
        SVGMobject.init_colors(self)
        if not self.parts_named:
            self.name_parts()
        for i in self.parts:
            # i.set_color(RED)
            self.set_opacity(1)
        return self

    def color_country(self, country_code, color=RED):
        country_index = self.countries[country_code]
        self.parts[country_index].set_color(color)
