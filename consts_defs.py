from manimlib.imports import *
#This will be changed with re scrapping the svg file
STATES = {
    "MA": 0,
    "MN": 1,
    "MT": 2,
    "ND": 3,
    "HI": 4,
    "ID": 5,
    "WA": 6,
    "AZ": 7,
    "CA": 8,
    "CO": 9,
    "NV": 10,
    "NM": 11,
    "OR": 12,
    "UT": 13,
    "WY": 14,
    "AR": 15,
    "IA": 16,
    "KS": 17,
    "MO": 18,
    "NE": 19,
    "OK": 20,
    "SD": 21,
    "LA": 22,
    "TX": 23,
    "CT": 24,
    "NH": 25,
    "RI": 26,
    "VT": 27,
    "AL": 28,
    "FL": 29,
    "GA": 30,
    "MS": 31,
    "SC": 32,
    "IL": 33,
    "IN": 34,
    "KY": 35,
    "NC": 36,
    "OH": 37,
    "TN": 38,
    "VA": 39,
    "WI": 40,
    "WV": 41,
    "DE": 42,
    "DC": 43,
    "MD": 44,
    "NJ": 45,
    "NY": 46,
    "PA": 47,
    "ME": 48,
    "MI": 49,
}


PACIFIC = ["CA", "AZ", "NV"]
SOUTHWEST = ["TX", "NM", "MS", "TN", "LA", "AR"]
NORTHWEST = [
    "WA",
    "OR",
    "ID",
    "WY",
    "ND",
    "MT",
    "MN",
    "OK",
    "KS",
    "NE",
    "UT",
    "SD",
    "CO",
]
CENTRAL = ["WI", "IA", "MI", "IN", "IL", "OH", "MO"]
ATLANTIC = ["ME", "NH", "VT", "CT", "RI", "MA", "NY", "NJ", "PA"]
SOUTHEAST = ["MD", "WV", "VA", "NC", "KY", "SC", "GA", "FL", "AL"]

SCORES = {
    "Blazers": "LWLW",
    "Lakers": "WLWW",
    "Heat": "WL",
    "Thunder": "WWL",
    "76ers": "WL",
    "Rockets": "WLLL",
    "Timberwolves": "WLWW",
    "Spurs": "LLW",
    "Hornets": "WW",
    "Magic": "LW",
    "Grizzlies": "WWWL",
    "Pelicans": "WWW",
    "Jazz": "WWL",
    "Nuggets": "WWLW",
    "Knicks": "WW",
    "Nets": "WW",
    "Bulls": "WW",
    "Clippers": "LWWW",
    "Mavericks": "LLWW",
    "Raptors": "LL",
    "Pistons": "WL",
    "Hawks": "WW",
    "Cavaliers": "WW",
    "Kings": "WWWW",
    "Bucks": "LW",
    "Suns": "LWWW",
    "Wizards": "WW",
    "Celtics": "LW",
    "Pacers": "WW",
}
EAST = CENTRAL + ATLANTIC + SOUTHEAST
WEST = SOUTHWEST + NORTHWEST + PACIFIC
EAST_COLOR = "#1c3f87"
WEST_COLOR = "#b8002c"

class TeamData:
    def __init__(self, pos, division):
        self.pos = pos
        self.division = division

TEAMS_POSITIONS = {
    "Houston_Rockets": TeamData((0.5, -1.5), "SOUTHWEST"),
    "San_Antonio_Spurs": TeamData((0, -1.5), "SOUTHWEST"),
    "WashingtonWizards": TeamData((2.4, 0.4), "SOUTHEAST"),
    "SacramentoKings": TeamData((-2.7, 0.5), "PACIFIC"),
    "UtahJazz": TeamData((-1.5, 0.35), "NORTHWEST"),
    "LosAngelesLakers": TeamData((-2.6, -0.4), "PACIFIC"),
    "ClevelandCavaliers": TeamData((2.2, 0.7), "CENTRAL"),
    "Boston_Celtics": TeamData((03.2, 1.1), "ATLANTIC"),
    "PhoenixSuns": TeamData((-1.5, -0.7), "PACIFIC"),
    "DallasMavericks": TeamData((0.4, -1), "SOUTHWEST"),
    "Memphis_Grizzlies": TeamData((1, -0.4), "SOUTHWEST"),
    "MiamiHeat": TeamData((02.5, -1.8), "SOUTHEAST"),
    "PortlandTrailBlazers": TeamData((-2.8, 01.3), "NORTHWEST"),
    "Denver_Nuggets": TeamData((-0.7, 0), "NORTHWEST"),
    "ChicagoBulls": TeamData((1.3, 0.6), "CENTRAL"),
    "Oklahoma_City_Thunder": TeamData((0.3, -0.5), "NORTHWEST"),
    "Indiana_Pacers": TeamData((1.4, 0.2), "CENTRAL"),
    "Philadelphia76ers": TeamData((2.6, 0.5), "ATLANTIC"),
    "Los_Angeles_Clippers": TeamData((-2.5, -0.5), "PACIFIC"),
    "OrlandoMagic": TeamData((2.5, -1.4), "SOUTHEAST"),
    "DetroitPistons": TeamData((1.8, 0.9), "CENTRAL"),
    "NewYork": TeamData((2.9, 0.9), "ATLANTIC"),
    "Charlotte_Hornets": TeamData((2.3, -0.3), "SOUTHEAST"),
    "MinnesotaTimberwolves": TeamData((0.6, 0.8), "NORTHWEST"),
    "MilwaukeeBucks": TeamData((1.1, 1), "CENTRAL"),
    "NewOrleans": TeamData((1.3, -1.4), "SOUTHWEST"),
    "AtlantaHawks": TeamData((1.8, -0.5), "SOUTHEAST"),
    "GoldenState": TeamData((-2.7, 0.2), "PACIFIC"),
    "TorontoRaptors": TeamData((3, 2.78), "ATLANTIC"),
    "BrooklynNets": TeamData((2.8, 0.8), "ATLANTIC"),
}


class MapUSA(SVGMobject):
    CONFIG = {
        "fill_opacity": 0.0,
        "height": 4,
        "close_new_points": True,
    }

    def __init__(self, file_name="testing.svg", **kwargs):
        self.parts_named = False
        svg_file = file_name
        SVGMobject.__init__(self, file_name=svg_file, **kwargs)
        self.name_parts()

    def name_parts(self):
        self.al = self.submobjects
        self.parts_named = True

    def copy(self):
        copy_mobject = SVGMobject.copy(self)
        copy_mobject.name_parts()
        return copy_mobject

    def init_colors(self):
        SVGMobject.init_colors(self)
        if not self.parts_named:
            self.name_parts()
        for i in self.al:
            i.set_color("#6D6E71")
            i.set_stroke(BLACK, width=1)
            self.set_opacity(1)
        return self

    def color_state(self, state, color=GREEN):
        i = STATES[state]
        self.al[i].set_fill(color)
        self.al[i].set_stroke(BLACK, width=2)
        self.al[i].set_opacity(1)

    def recolor(self, color):
        for i in self.al:
            i.set_fill(color)
            i.set_stroke(BLACK, width=2)
            i.set_opacity(1)

    def color_states(self, states, color=GREEN):
        for i in states:
            self.color_state(i, color)

    def color_west(self, color=WEST_COLOR):
        self.color_states(WEST, color)

    def color_east(self, color=EAST_COLOR):
        self.color_states(EAST, color)

    def color_division(self, division, color=YELLOW):
        self.color_states(DIVISIONS[division], color)

    def move_portion(self, portion, direction=RIGHT):
        for i in portion:
            j = STATES[i]
            self.al[j].shift(direction)


