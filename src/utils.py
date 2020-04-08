from collections import defaultdict
from typing import (
    FrozenSet, Iterable, List, Optional, Set, Text, Tuple, Union, Any, Dict, Callable
)

import json
import os

from src.data_model import StarSigns, CompatibilityScoreMark, Personality, Species

_personality_comp_score_matrix = defaultdict(dict)


def get_star_sign_by_birthday(birth):
    # type: (Tuple[int, int]) -> Optional[StarSigns]
    def birth_to_int(m, d):
        return (m << 8) | d

    star_sign_def = [
        (((1, 1), (1, 19)), StarSigns.Capricorn),
        (((1, 20), (2, 18)), StarSigns.Aquarius),
        (((2, 19), (3, 20)), StarSigns.Pisces),
        (((3, 21), (4, 19)), StarSigns.Aries),
        (((4, 20), (5, 20)), StarSigns.Taurus),
        (((5, 21), (6, 20)), StarSigns.Gemini),
        (((6, 21), (7, 22)), StarSigns.Cancer),
        (((7, 23), (8, 22)), StarSigns.Leo),
        (((8, 23), (9, 22)), StarSigns.Virgo),
        (((9, 23), (10, 22)), StarSigns.Libra),
        (((10, 23), (11, 21)), StarSigns.Scorpio),
        (((11, 22), (12, 21)), StarSigns.Sagittarius),
        (((12, 22), (12, 31)), StarSigns.Capricorn),
    ]

    convert_list = map(
        lambda ss_def: (range(birth_to_int(*ss_def[0][0]), birth_to_int(*ss_def[0][1]) + 1), ss_def[1]),
        star_sign_def
    )
    birth_int = birth_to_int(*birth)

    for tuple_range_ss in convert_list:
        if birth_int in tuple_range_ss[0]:
            return tuple_range_ss[1]
    raise ValueError("Invalid birthday")


def get_compatibility_score_by_unicode_sign(sign):
    if sign == "♥":
        return CompatibilityScoreMark.HEART
    elif sign == "♦":
        return CompatibilityScoreMark.DIAMOND
    elif sign == "♣":
        return CompatibilityScoreMark.CLOVER
    elif sign == "×":
        return CompatibilityScoreMark.CROSS
    else:
        raise ValueError("Sign must be either ♥, ♦, ♣, or ×")


def calculate_compatibility_score_by_personality(p1, p2):
    return _personality_comp_score_matrix[p1][p2]


def calculate_compatibility_score_by_species(s1, s2):
    def check_species(chk1, chk2):
        return (s1 == chk1 and s2 == chk2) or (s2 == chk1 and s1 == chk2)

    if check_species(Species.Bear, Species.Cub) or \
            check_species(Species.Bull, Species.Cow) or \
            check_species(Species.Cat, Species.Tiger) or \
            check_species(Species.Dog, Species.Wolf) or \
            check_species(Species.Goat, Species.Sheep) or \
            check_species(Species.Kangaroo, Species.Koala):
        return CompatibilityScoreMark.HEART
    elif s1 == s2 or \
            check_species(Species.Deer, Species.Horse) or \
            check_species(Species.Hamster, Species.Squirrel) or \
            check_species(Species.Hamster, Species.Mouse) or \
            check_species(Species.Mouse, Species.Squirrel):
        return CompatibilityScoreMark.DIAMOND
    elif check_species(Species.Cat, Species.Mouse) or \
            check_species(Species.Cat, Species.Hamster) or \
            check_species(Species.Dog, Species.Gorilla) or \
            check_species(Species.Dog, Species.Monkey) or \
            check_species(Species.Sheep, Species.Wolf):
        return CompatibilityScoreMark.CROSS
    else:
        return CompatibilityScoreMark.CLOVER


def load_personality_compatibility_data():
    data_dir_path = os.path.join(os.path.dirname(__file__), os.path.pardir, "data")
    with open(os.path.join(data_dir_path, "personality_compatibility.json"), "r") as _fp:
        data = json.load(_fp)  # type: Dict[str,Dict[str,str]]
        for p1, p2_comp in data.items():
            p1_enum = getattr(Personality, p1)
            assert p1_enum
            for p2, comp in p2_comp.items():
                p2_enum = getattr(Personality, p2)
                assert p2_enum
                _personality_comp_score_matrix[p1_enum][p2_enum] = get_compatibility_score_by_unicode_sign(comp)


load_personality_compatibility_data()
