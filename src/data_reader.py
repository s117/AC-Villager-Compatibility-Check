from typing import (
    List, Optional, Dict, Any
)
import datetime

from src.utils import get_data_dir_path
from src.data_model import VillagerData, Personality, Species


class VillagerDataReader:
    def get_data_by_villager_id(self, villager_id):
        # type: (str) -> Optional[VillagerData]
        raise NotImplementedError


class AcListerVillagerDataReader(VillagerDataReader):
    class AcListerVillagerData(VillagerData):
        def parse_name(self, name):
            # type: (str) -> None
            self._name = name

        def parse_villager_id(self, villager_id):
            # type: (str) -> None
            self._villager_id = villager_id

        def parse_species(self, species):
            # type: (str) -> None
            self._species = getattr(Species, species, None)

        def parse_personality(self, personality):
            # type: (str) -> None
            self._personality = getattr(Personality, personality, None)

        def parse_coffee(self, coffee):
            # type: (str) -> None
            self._coffee = coffee

        def parse_birthday(self, birthday):
            # type: (str) -> None
            def validate_date(y, m, d):
                # type: (int, int, int) -> bool
                is_valid = False
                try:
                    datetime.datetime(int(y), int(m), int(d))
                    is_valid = True
                except ValueError:
                    pass
                return is_valid

            month_convert_tbl = {
                "January": 1,
                "February": 2,
                "March": 3,
                "April": 4,
                "May": 5,
                "June": 6,
                "July": 7,
                "August": 8,
                "September": 9,
                "October": 10,
                "November": 11,
                "December": 12
            }
            split_result = birthday.split(' ')
            if len(split_result) == 1:
                self._birthday = None
            else:
                month_str, day_str = split_result[0], split_result[1]
                assert month_str in month_convert_tbl.keys()
                month_int = month_convert_tbl[month_str]
                day_int = int(day_str)
                if validate_date(2000, month_int, day_int):
                    self._birthday = (month_int, day_int)
                else:
                    self._birthday = None

        def parse_wiki(self, wiki):
            # type: (str) -> None
            self._wiki = wiki

    def __init__(self, aclister_loc=None):
        if not aclister_loc:
            import os
            data_dir_path = get_data_dir_path()
            aclister_loc = os.path.join(data_dir_path, "villager.json")
        with open(aclister_loc, "r") as fp_data:
            import json
            self.raw_data = json.load(fp_data)  # type: List[Dict[str,str]]

        self._villager_id_to_idx_tbl = dict()

        for idx, villager_data in enumerate(self.raw_data):
            assert villager_data['id'] not in self._villager_id_to_idx_tbl.keys()
            self._villager_id_to_idx_tbl[villager_data['id']] = idx

    def get_data_by_villager_id(self, villager_id):
        if villager_id not in self._villager_id_to_idx_tbl.keys():
            return None
        villager_raw_dat = self.raw_data[self._villager_id_to_idx_tbl[villager_id]]

        villager_dat = AcListerVillagerDataReader.AcListerVillagerData()

        villager_dat.parse_name(villager_raw_dat['name'])
        villager_dat.parse_villager_id(villager_raw_dat['id'])
        villager_dat.parse_species(villager_raw_dat['species'])
        villager_dat.parse_personality(villager_raw_dat['personality'])
        villager_dat.parse_coffee(villager_raw_dat['coffee'])
        villager_dat.parse_birthday(villager_raw_dat['birthday'])
        villager_dat.parse_wiki(villager_raw_dat['wiki'])

        return villager_dat

    def get_raw_data_by_villager_id(self, villager_id):
        # type: (str) -> Optional[Dict[str, Any]]
        if villager_id not in self._villager_id_to_idx_tbl.keys():
            return None

        return self.raw_data[self._villager_id_to_idx_tbl[villager_id]]
