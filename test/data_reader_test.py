import os
import sys
import unittest
from src.data_reader import VillagerDataReader, AcListerVillagerDataReader
from src.data_model import Species
from src.data_model import Personality
from src.utils import get_data_dir_path


class DebuggableTestCase(unittest.TestCase):
    def __add_error_replacement(self, _, err):
        value, traceback = err[1:]
        raise value.with_traceback(traceback)

    def run(self, result=None):
        if result and sys.gettrace() is not None:
            result.addError = self.__add_error_replacement
        super().run(result)


class AcListerVillagerDataReaderTestCase(DebuggableTestCase):
    def test_a_cls_init(self):
        villager_reader = AcListerVillagerDataReader()
        self.assertIsInstance(villager_reader, VillagerDataReader)

    def test_b_get_few_villager_by_id(self):
        tested_subjects = [
            {
                "name": "Ace",
                "id": "Ace",
                "species": "Bird",
                "personality": "Jock",
                "coffee": "",
                "birthday": "March 13",
                "wiki": "http://animalcrossing.wikia.com/wiki/Ace",
                "store": "https://www.redbubble.com/people/purplepixel/",
                "hasProfileImage": False,
                "hasIconImage": True
            }, {
                "name": "Jakey",
                "id": "Jakey",
                "species": "Bird",
                "personality": "Lazy",
                "coffee": "Mocha - A Little Milk - 1 Sugar",
                "birthday": "August 24",
                "wiki": "http://animalcrossing.wikia.com/wiki/Jacob",
                "store": "https://www.redbubble.com/people/purplepixel/works/30508140-jacob-animal-crossing",
                "hasProfileImage": True,
                "hasIconImage": True
            },
            {
                "name": "Candi",
                "id": "Candi",
                "species": "Mouse",
                "personality": "Peppy",
                "coffee": "Kilimanjaro - Lots of Milk - 3 Sugars",
                "birthday": "April 13",
                "wiki": "http://animalcrossing.wikia.com/wiki/Candi",
                "store": "https://www.redbubble.com/people/purplepixel/works/23778232-candi-animal-crossing",
                "hasProfileImage": True,
                "hasIconImage": True
            },
            {
                "name": "Carmen",
                "id": "Carmen (2)",
                "species": "Mouse",
                "personality": "Snooty",
                "coffee": "",
                "birthday": "March 24",
                "wiki": "http://animalcrossing.wikia.com/wiki/Carmen_(mouse)",
                "store": "https://www.redbubble.com/people/purplepixel/",
                "hasProfileImage": False,
                "hasIconImage": True
            },
            {
                "name": "Carmen",
                "id": "Carmen",
                "species": "Rabbit",
                "personality": "Peppy",
                "coffee": "Blue Mountain - Lots of Milk - 3 Sugars",
                "birthday": "January 6",
                "wiki": "http://animalcrossing.wikia.com/wiki/Carmen_(rabbit)",
                "store": "https://www.redbubble.com/people/purplepixel/works/15934499-carmen-animal-crossing",
                "hasProfileImage": True,
                "hasIconImage": True
            },
            {
                "name": "Verdun",
                "id": "Verdun",
                "species": "Bull",
                "personality": "Lazy",
                "coffee": "",
                "birthday": "",
                "wiki": "http://animalcrossing.wikia.com/wiki/Verdun",
                "store": "https://www.redbubble.com/people/purplepixel/",
                "hasProfileImage": False,
                "hasIconImage": True
            },
        ]
        expected_parsed_tested_subjects = {
            "Ace": {
                "species": Species.Bird,
                "personality": Personality.Jock,
                "birthday": (3, 13)
            },
            "Jakey": {
                "species": Species.Bird,
                "personality": Personality.Lazy,
                "birthday": (8, 24)
            },
            "Candi": {
                "species": Species.Mouse,
                "personality": Personality.Peppy,
                "birthday": (4, 13)
            },
            "Carmen (2)": {
                "species": Species.Mouse,
                "personality": Personality.Snooty,
                "birthday": (3, 24)
            },
            "Carmen": {
                "species": Species.Rabbit,
                "personality": Personality.Peppy,
                "birthday": (1, 6)
            },
            "Verdun": {
                "species": Species.Bull,
                "personality": Personality.Lazy,
                "birthday": None
            }
        }

        villager_reader = AcListerVillagerDataReader(
            aclister_loc="../data/villager.json")

        for test_subject in tested_subjects:
            test_subject_id = test_subject['id']
            raw_data = villager_reader.get_raw_data_by_villager_id(test_subject_id)
            self.assertEqual(test_subject, raw_data)

            parsed_data = villager_reader.get_data_by_villager_id(test_subject_id)
            self.assertEqual(test_subject["name"], parsed_data.name)
            self.assertEqual(test_subject["id"], parsed_data.villager_id)
            self.assertEqual(expected_parsed_tested_subjects[test_subject_id]['species'], parsed_data.species)
            self.assertEqual(expected_parsed_tested_subjects[test_subject_id]['personality'], parsed_data.personality)
            self.assertEqual(expected_parsed_tested_subjects[test_subject_id]['birthday'], parsed_data.birthday)
            self.assertEqual(test_subject["coffee"], parsed_data.coffee)
            self.assertEqual(test_subject["wiki"], parsed_data.wiki)

    def test_c_acnh_new_chara_completeness(self):
        def load_acnh_complete_villager_species_dataset():
            acnh_all_villagers_and_species = dict()
            acnh_villager_complete_list = os.path.join(get_data_dir_path(), "test", "acnh_villager")

            with open(acnh_villager_complete_list, "r") as fp:  # load data from data/acnh_villager
                for line in fp:
                    v_id, v_species = line.split('/')
                    if v_species[-1] == '\n':
                        v_species = v_species[:-1]
                    acnh_all_villagers_and_species[v_id] = v_species
            return acnh_all_villagers_and_species

        CUT = AcListerVillagerDataReader()

        acnh_villagers_species = load_acnh_complete_villager_species_dataset()

        for villager_id in acnh_villagers_species.keys():
            ac_lister_raw_dat = CUT.get_raw_data_by_villager_id(villager_id)
            self.assertTrue(ac_lister_raw_dat, "{} is missing from the database".format(villager_id))

            expected_species = acnh_villagers_species[villager_id]
            actual_species = ac_lister_raw_dat['species']
            self.assertEqual(expected_species, actual_species, "{} spices mismatch".format(villager_id))

    def test_d_invalid_villager_id(self):
        villager_reader = AcListerVillagerDataReader(
            aclister_loc="../data/villager.json")
        self.assertEqual(None, villager_reader.get_data_by_villager_id("qwertyQWERTY"))
        self.assertEqual(None, villager_reader.get_raw_data_by_villager_id("qwertyQWERTY"))


if __name__ == '__main__':
    unittest.main()
