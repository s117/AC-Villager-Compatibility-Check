import sys
import unittest
from src.data_reader import VillagerDataReader, AcListerVillagerDataReader
from src.data_model import Species
from src.data_model import Personality


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
        villager_reader = AcListerVillagerDataReader(aclister_loc="../data/villager.json")
        self.assertIsInstance(villager_reader, VillagerDataReader)

    def test_b_get_few_villager_by_id(self):
        test_subjects = [
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
        expected_parsed_test_subjects = {
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

        for test_subject in test_subjects:
            test_subject_id = test_subject['id']
            raw_data = villager_reader.get_raw_data_by_villager_id(test_subject_id)
            self.assertEqual(test_subject, raw_data)

            parsed_data = villager_reader.get_data_by_villager_id(test_subject_id)
            self.assertEqual(parsed_data.name, test_subject["name"])
            self.assertEqual(parsed_data.villager_id, test_subject["id"])
            self.assertEqual(parsed_data.species, expected_parsed_test_subjects[test_subject_id]['species'])
            self.assertEqual(parsed_data.personality, expected_parsed_test_subjects[test_subject_id]['personality'])
            self.assertEqual(parsed_data.birthday, expected_parsed_test_subjects[test_subject_id]['birthday'])
            self.assertEqual(parsed_data.coffee, test_subject["coffee"])
            self.assertEqual(parsed_data.wiki, test_subject["wiki"])

    def test_c_acnh_new_chara_complete_test(self):
        def do_verify(ac_lister_path, acnh_villager_path):
            acnh_villagers_species = dict()
            with open(acnh_villager_path, "r") as fp:  # load data from data/acnh_villager
                for line in fp:
                    name, spec = line.split('/')
                    if spec[-1] == '\n':
                        spec = spec[:-1]
                    acnh_villagers_species[name] = spec
            data_src = AcListerVillagerDataReader(aclister_loc=ac_lister_path)

            for acnh_name in acnh_villagers_species.keys():
                ac_lister_raw_dat = data_src.get_raw_data_by_villager_id(acnh_name)
                acnh_spec = acnh_villagers_species[acnh_name]

                self.assertTrue(ac_lister_raw_dat, "{} is missing from the database".format(acnh_name))
                aclister_spec = ac_lister_raw_dat['species']
                self.assertEqual(aclister_spec, acnh_spec, "{} spices mismatch".format(acnh_name))

        do_verify("../data/villager.json",
                  "../data/acnh_villager")


if __name__ == '__main__':
    unittest.main()
