from enum import Enum, auto
from typing import (
    FrozenSet, Iterable, List, Optional, Set, Text, Tuple, Union, Any, Dict, Callable
)


def check_console_escape_support():
    import sys, os, time, platform

    # sample_ansi = '\x1b[31mRED' + '\x1b[33mYELLOW' + '\x1b[32mGREEN' + '\x1b[35mPINK' + '\x1b[0m' + '\n'
    out_pipe_support = []
    for handle in [sys.stdout, sys.stderr]:
        if (hasattr(handle, "isatty") and handle.isatty()) or \
                ('TERM' in os.environ and os.environ['TERM'] == 'ANSI'):
            if platform.system() == 'Windows' and not ('TERM' in os.environ and os.environ['TERM'] == 'ANSI'):
                # handle.write("Windows console, no ANSI support.\n")
                out_pipe_support.append(False)
            else:
                # handle.write("ANSI output enabled.\n")
                # handle.write(sample_ansi)
                out_pipe_support.append(True)
        else:
            # handle.write("ANSI output disabled.\n")
            out_pipe_support.append(False)

        # handle.write("\n\n")
        # handle.flush()
        # time.sleep(0.2)

    return out_pipe_support[0] and out_pipe_support[1]


CONSOLE_ESCAPE_SUPPORT = check_console_escape_support()


class Personality(Enum):
    Normal = auto()
    Lazy = auto()
    Peppy = auto()
    Jock = auto()
    Snooty = auto()
    Cranky = auto()
    Smug = auto()
    Uchi = auto()


class Species(Enum):
    Alligator = auto()
    Anteater = auto()
    Bear = auto()
    Bird = auto()
    Bull = auto()
    Cat = auto()
    Chicken = auto()
    Cow = auto()
    Cub = auto()
    Deer = auto()
    Dog = auto()
    Duck = auto()
    Eagle = auto()
    Elephant = auto()
    Frog = auto()
    Goat = auto()
    Gorilla = auto()
    Hamster = auto()
    Hippo = auto()
    Horse = auto()
    Kangaroo = auto()
    Koala = auto()
    Lion = auto()
    Monkey = auto()
    Mouse = auto()
    Octopus = auto()
    Ostrich = auto()
    Penguin = auto()
    Pig = auto()
    Rabbit = auto()
    Rhino = auto()
    Sheep = auto()
    Squirrel = auto()
    Tiger = auto()
    Wolf = auto()


class StarSigns(Enum):
    Aries = auto()
    Taurus = auto()
    Gemini = auto()
    Cancer = auto()
    Leo = auto()
    Virgo = auto()
    Libra = auto()
    Scorpio = auto()
    Sagittarius = auto()
    Capricorn = auto()
    Aquarius = auto()
    Pisces = auto()


class CompatibilityScoreMark(Enum):
    HEART = 2
    DIAMOND = 1
    CLOVER = 0
    CROSS = -1

    def __str__(self):
        if CONSOLE_ESCAPE_SUPPORT:
            return self._get_color_text()
        else:
            return self._get_plain_text()

    def _get_plain_text(self):
        if self.value == CompatibilityScoreMark.HEART.value:
            return "♥"
        elif self.value == CompatibilityScoreMark.DIAMOND.value:
            return "♦"
        elif self.value == CompatibilityScoreMark.CLOVER.value:
            return "♣"
        elif self.value == CompatibilityScoreMark.CROSS.value:
            return "×"
        else:
            raise ValueError("Invalid instance")

    def _get_color_text(self):
        if self.value == CompatibilityScoreMark.HEART.value:
            return "\x1b[30;102m♥\x1b[0m"  # Green
        elif self.value == CompatibilityScoreMark.DIAMOND.value:
            return "\x1b[30;106m♦\x1b[0m"  # Cyan
        elif self.value == CompatibilityScoreMark.CLOVER.value:
            return "\x1b[30;103m♣\x1b[0m"  # Yellow
        elif self.value == CompatibilityScoreMark.CROSS.value:
            return "\x1b[30;101m×\x1b[0m"  # Red
        else:
            raise ValueError("Invalid instance")


class Compatibility(Enum):
    # Good Compatibility: 2 or more ♥, ♥♦♣, or ♥♦♦
    # Bad Compatibility: 2 or 3 ×
    # Average Compatibility: Any other combination.

    GOOD = 1
    AVERAGE = 0
    BAD = -1

    def __str__(self):
        if CONSOLE_ESCAPE_SUPPORT:
            return self._get_color_text()
        else:
            return self._get_plain_text()

    def _get_plain_text(self):
        if self.value == Compatibility.GOOD.value:
            return "Good"
        elif self.value == Compatibility.AVERAGE.value:
            return "Average"
        elif self.value == Compatibility.BAD.value:
            return "Bad"
        else:
            raise ValueError("Invalid instance")

    def _get_color_text(self):
        if self.value == Compatibility.GOOD.value:
            return "\x1b[32mGood\x1b[0m"  # Green
        elif self.value == Compatibility.AVERAGE.value:
            return "\x1b[33mAverage\x1b[0m"  # Yellow
        elif self.value == Compatibility.BAD.value:
            return "\x1b[31mBad\x1b[0m"  # Red
        else:
            raise ValueError("Invalid instance")


class VillagerData:
    def __init__(self):
        self._name = ""
        self._villager_id = ""
        self._species = None
        self._personality = None
        self._coffee = ""
        self._birthday = (0, 0)
        self._wiki = ""

    @property
    def name(self):
        # type: () -> str
        return self._name

    @property
    def villager_id(self):
        # type: () -> str
        return self._villager_id

    @property
    def species(self):
        # type: () -> Optional[Species]
        return self._species

    @property
    def personality(self):
        # type: () -> Optional[Personality]
        return self._personality

    @property
    def coffee(self):
        # type: () -> str
        return self._coffee

    @property
    def birthday(self):
        # type: () -> Optional[Tuple[int, int]]
        return self._birthday

    @property
    def wiki(self):
        # type: () -> str
        return self._wiki

    def __eq__(self, other):
        return self.name == other.name and \
               self.villager_id == other.villager_id and \
               self.species == other.species and \
               self.personality == other.personality and \
               self.coffee == other.coffee and \
               self.birthday == other.birthday and \
               self.wiki == other.wiki
