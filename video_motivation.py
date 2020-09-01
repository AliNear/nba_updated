from manimlib.imports import *
import os
import re
from projects.project_one.custom_mobjects import *
from projects.nba_update_project.consts_defs import *

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

def create_line_table(text, color=LOADING_COLOR):
    circle = Circle(radius=.15, fill_color=color, fill_opacity=1, stroke_width=0)
    circle.set_xy(-.85, 1.75)
    stats_rect = Rectangle(width=1.5, height=.2, fill_color=color, fill_opacity=1, stroke_width=0)
    stats_rect.next_to(circle, RIGHT, buff=.1)
    text = Text(text, font="DDT W00 Italic", color=BLACK).scale(.2)
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
    CONFIG = {
            "main_rect_kwargs": {
                "color": LOADING_COLOR,
                "fill_color": LOADING_COLOR,
                "fill_opacity": 1,
                "stroke_width": 1
                },
            "clubs_color": "#cfcfcf"
            }
    def __init__(self, image_name, texts, **kwargs):
        VMobject.__init__(self, **kwargs)
        main_rect = Rectangle(width=2.8, height=4, **self.main_rect_kwargs)
        icon = Avatar(ASSETS_PATH + 'leagues/' + image_name, 0, 0, .5)
        self.clubs = Group(*[create_line_table(i, color=self.clubs_color) for i in texts])
        self.clubs.set_y(1.7)
        self.clubs.arrange_submobjects(DOWN, False, False, buff=.2)
        self.add(main_rect)
        self.add(self.clubs)
        self.add(icon)
    def surround_club(self, index=0, color=RED):
        width = self.clubs[index].get_width()
        height = self.clubs[index].get_height()
        surrounding_rect = Rectangle(width=width, height=height, color=color, stroke_width=1)
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
        self.back_to_us()
        self.draw_planes()

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
        self.tables = VGroup()
        for i in images:
            table = RankingTable(i, texts).scale(.05)
            country = self.world_map.get_country(FOUR_NATIONS[j])
            table.move_to(self.world_map.get_country(FOUR_NATIONS[j]))
            self.play(table.scale, 8,
                      table.move_to, start + 2.7 * j * RIGHT)
            self.rects_winners.add(table.surround_winner())
            self.rects_losers.add(table.surround_losers())
            self.tables.add(table)
            self.wait()
            j += 1
    
    def explanation_soccer_format(self):
        #TODO: Add medals (champions) + down arrows (relegated clubs)
        self.play(ShowCreation(self.rects_winners))
        self.wait()
        self.play(ShowCreation(self.rects_losers))

    def prepare_new_map(self):
        self.us = self.world_map.get_country("US")
        self.us_copy = self.us.copy()
        self.add(self.us_copy)
        self.usa_map = AvatarSVG(ASSETS_PATH + "us.svg").scale(.5)
        self.usa_map.move_to(self.us_copy)

    def back_to_us(self):
        """Show why it can't be done in the us (big country)"""
        self.play(FadeOut(self.rects_winners), FadeOut(self.rects_losers))
        self.play(FadeOut(self.tables), self.world_map.color_countries, FOUR_NATIONS, "#f2f2f2")
        self.play(self.world_map.shift, 4 * RIGHT)
        self.prepare_new_map()
        self.play(self.us_copy.set_color, RED)
        # self.camera_frame = self.camera.frame
        self.camera_frame.save_state()
        self.play(
            self.camera_frame.set_width, self.us_copy.get_width() * 1.0,
            self.camera_frame.set_height, self.us_copy.get_height() * 1.0,
            self.camera_frame.move_to, self.us_copy,
        )
        self.play(FadeOut(self.world_map))
        self.play(Transform(self.us_copy, self.usa_map), run_time=.5)
        la_city = self.usa_map.get_center() - (self.usa_map.get_width() * .34) * RIGHT
        mew_city = self.usa_map.get_center() + (self.usa_map.get_width() * .44) * RIGHT
        self.la_point = Dot(la_city, color=BLUE_D).scale(.3)
        self.mew_point = Dot(mew_city, color=BLUE_D).scale(.3)
        self.play(ShowCreation(self.la_point))
        self.play(ShowCreation(self.mew_point))
        self.wait()

        self.airplane = ImageMobject(ASSETS_PATH + "airplane.png").scale(.1)
        self.airplane.move_to(self.la_point)
        between_cities = ArcBetweenPoints(la_city, mew_city,angle=-PI/6, color=GREEN)
        self.between_cities_dashed = DashedVMobject(between_cities)
        self.play(ShowCreation(self.between_cities_dashed))
        self.play(FadeIn(self.airplane))
        self.play(self.airplane.rotate, -10 * DEGREES,
                  MoveAlongPath(self.airplane, between_cities), run_time=2, rate_func=linear)

    def draw_planes(self):
        self.play(FadeOut(self.airplane), FadeOut(self.between_cities_dashed), FadeOut(self.mew_point))
        center = self.usa_map.get_center()
        width = self.usa_map.get_width()
        height = self.usa_map.get_height()
        def to_new_coords(point, x_bias=.2):
            x = (point[0] + center[0]) / 2.6
            y = (point[1] + center[1]) / 2.4
            return np.array([x - x_bias, y + .9, 0])
        dots = VGroup()
        circles = VGroup()
        opacities = {"PACIFIC":1, "NORTHWEST": .6, "SOUTHWEST": .6, "ATLANTIC":.3, "SOUTHEAST": .3, "CENTRAL": .3}
        for i in TEAMS_POSITIONS:
            point = TEAMS_POSITIONS[i].pos
            if i == "PortlandTrailBlazers":
                res_point = to_new_coords(point, x_bias=0)
            elif i == "TorontoRaptors":
                pass
            else:
                res_point = to_new_coords(point)
            opacity = opacities[TEAMS_POSITIONS[i].division]
            c = Circle(fill_color="FF0000", fill_opacity=opacity, radius=.4).scale(.2)
            d = Dot(res_point, color=RED).scale(.3)
            c.set_stroke(width=0)
            c.move_to(res_point)
            dots.add(d)
            circles.add(c)
            print (res_point)

        rects = VGroup()
        texts_objects = VGroup()
        x = -2.2
        y = 2.5
        opacities = 1, .6, .3
        texts = ["Maximum", "Medium", "Low"]
        for i in range(3):
            r = Rectangle(fill_color="FF0000", fill_opacity=opacities[i]).scale(.05)
            t = Text(texts[i] + " Matchups", font="DDT W00 Regulat", color=BLACK).scale(.1)
            r.set_stroke(width=0)
            r.set_xy(x, y)
            y -= .2
            rects.add(r)
            t.next_to(r, direction=RIGHT, buff=.1)
            texts_objects.add(t)
        self.play(ShowCreation(dots))
        lines = VGroup()
        for i in [6, 7, 11, 14, 24]:
            between_cities = ArcBetweenPoints(self.la_point.get_center(), dots[i].get_center(),angle=-PI/6, color=GREEN)
            between_cities_dashed = DashedVMobject(between_cities)
            lines.add(between_cities_dashed)
            self.play(ShowCreation(between_cities_dashed), run_time=.5)
        self.wait()
        self.play(FadeOut(lines))
        self.wait()
        self.play(Transform(dots, circles))
        self.play(ShowCreation(rects), ShowCreation(texts_objects))
        # self.play(Restore(self.camera_frame))



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


class Test(Scene):
    def construct(self):
        airplane = ImageMobject(ASSETS_PATH + "airplane.png").scale(.5)
        arc = ArcBetweenPoints(DOWN + 2 * LEFT, UP + 2 * RIGHT, color=BLACK)
        self.add(airplane)
        self.play(FadeIn(arc))
        self.play(airplane.rotate, -30*DEGREES,
                MoveAlongPath(airplane, arc))
"""
class GiftScene(Scene):
    def construct(self):
        self.prepare()
        self.draw_maps()

    def prepare(self):
        self.dz = AvatarSVG(ASSETS_PATH + "dz.svg", fill_color=RED).scale(.5)
        self.dz.set_y(-1)
        self.fr = AvatarSVG(ASSETS_PATH + "fr.svg").scale(.5).set_y(1)

        self.plane = ImageMobject(ASSETS_PATH + "airplane.png").scale(.1)
        self.hamster = ImageMobject(ASSETS_PATH + "hamster.png").scale(.1)
        self.eiffel = ImageMobject(ASSETS_PATH + "paris.png").scale(.1)
    
    def draw_maps(self):
        self.play(ShowCreation(self.dz))
        self.play(ShowCreation(self.fr))

    def zoom_dz(self):
        pass
"""
