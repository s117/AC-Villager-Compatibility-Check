from enum import Enum, auto
from typing import (
    FrozenSet, Iterable, List, Optional, Set, Text, Tuple, Union, Any, Dict, Callable
)


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
