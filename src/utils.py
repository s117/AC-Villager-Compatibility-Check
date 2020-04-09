from collections import defaultdict
from typing import (
    FrozenSet, Iterable, List, Optional, Set, Text, Tuple, Union, Any, Dict, Callable
)

import json
import os

from src.data_model import StarSigns, CompatibilityScoreMark, Personality, Species, VillagerData, Compatibility
from src.data_reader import AcListerVillagerDataReader

_personality_comp_score_matrix = defaultdict(dict)


def get_star_sign_by_birthday(birth):
    # type: (Tuple[int, int]) -> StarSigns
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
    # type: (str) -> CompatibilityScoreMark
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
    # type: (Personality, Personality) -> CompatibilityScoreMark
    return _personality_comp_score_matrix[p1][p2]


def calculate_compatibility_score_by_species(s1, s2):
    # type: (Species, Species) -> CompatibilityScoreMark
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


_star_sign_group_idx = {
    StarSigns.Aries: 1,
    StarSigns.Leo: 1,
    StarSigns.Sagittarius: 1,

    StarSigns.Taurus: 2,
    StarSigns.Virgo: 2,
    StarSigns.Capricorn: 2,

    StarSigns.Gemini: 3,
    StarSigns.Libra: 3,
    StarSigns.Aquarius: 3,

    StarSigns.Cancer: 4,
    StarSigns.Scorpio: 4,
    StarSigns.Pisces: 4,
}


def calculate_compatibility_score_by_star_signs(ss1, ss2):
    # type: (StarSigns, StarSigns) -> CompatibilityScoreMark
    ss1_gid = _star_sign_group_idx[ss1]
    ss2_gid = _star_sign_group_idx[ss2]
    if ss1_gid == ss2_gid:
        return CompatibilityScoreMark.HEART
    elif (ss1_gid == 1 and ss2_gid == 4) or \
            (ss1_gid == 4 and ss2_gid == 1) or \
            (ss1_gid == 2 and ss2_gid == 3) or \
            (ss1_gid == 3 and ss2_gid == 2):
        return CompatibilityScoreMark.CROSS
    else:
        return CompatibilityScoreMark.DIAMOND


def calc_villager_compatibility(villager_a, villager_b):
    # type: (VillagerData, VillagerData) -> Optional[Dict[str, CompatibilityScoreMark]]
    if not villager_a.birthday or not villager_b.birthday or \
            not villager_a.personality or not villager_b.personality or \
            not villager_a.species or not villager_b.species:
        return None
    villager_a_star_sign = get_star_sign_by_birthday(villager_a.birthday)
    villager_b_star_sign = get_star_sign_by_birthday(villager_b.birthday)
    return {
        "personality": calculate_compatibility_score_by_personality(
            villager_a.personality, villager_b.personality
        ),
        "species": calculate_compatibility_score_by_species(
            villager_a.species, villager_b.species
        ),
        "star_sign": calculate_compatibility_score_by_star_signs(
            villager_a_star_sign, villager_b_star_sign
        )
    }


def calculate_compatibility_matrix(villagers_list, data_src):
    # type: (List[str], AcListerVillagerDataReader) -> List[List[Dict]]

    comp_matrix = []

    def query_nth_villager_data(idx):
        dat = data_src.get_data_by_villager_id(villagers_list[idx])
        if not dat:
            raise ValueError(
                "Failed to query the information for the {}th villager: no villager with id {} in the database".format(
                    idx + 1, villagers_list[idx]
                )
            )

        return dat

    for i in range(len(villagers_list)):
        va = query_nth_villager_data(i)
        curr_row = []
        for j in range(len(villagers_list)):
            vb = query_nth_villager_data(j)
            curr_row.append(calc_villager_compatibility(va, vb))
        comp_matrix.append(curr_row)

    return comp_matrix


def evaluate_compatibility(comp_mark):
    # type: (List[CompatibilityScoreMark]) -> Compatibility
    from collections import Counter
    assert len(comp_mark) == 3
    counts = Counter(comp_mark)

    def test_good_compatibility():
        return (
                (
                        counts[CompatibilityScoreMark.HEART] >= 2
                ) or (
                        counts[CompatibilityScoreMark.HEART] == 1 and
                        counts[CompatibilityScoreMark.DIAMOND] == 1 and
                        counts[CompatibilityScoreMark.CLOVER] == 1
                ) or (
                        counts[CompatibilityScoreMark.HEART] == 1 and
                        counts[CompatibilityScoreMark.DIAMOND] == 2
                )
        )

    def test_bad_compatibility():
        return counts[CompatibilityScoreMark.CROSS] >= 2

    if test_good_compatibility():
        return Compatibility.GOOD
    elif test_bad_compatibility():
        return Compatibility.BAD
    else:
        return Compatibility.AVERAGE


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
