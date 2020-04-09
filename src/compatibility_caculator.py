from tabulate import tabulate
from src.utils import *


def compatibility_calculator(villager):
    data_src = AcListerVillagerDataReader()

    def print_villager_details():
        tabulate_content = []
        tabulate_header = ["Id", "Species", "Personality", "Birthday", "Star Sign"]
        for v in villager:
            curr_row = [v]
            v_data = data_src.get_data_by_villager_id(v)

            if v_data:
                v_species_str = v_data.species.name if v_data.species.name else "N/A"
                v_personality_str = v_data.personality.name if v_data.species.name else "N/A"
                v_birthday_str = "{}/{}".format(*v_data.birthday) if v_data.birthday else "N/A"
                v_star_sign = get_star_sign_by_birthday(v_data.birthday).name if v_data.birthday else "N/A"
                curr_row.append(v_species_str)
                curr_row.append(v_personality_str)
                curr_row.append(v_birthday_str)
                curr_row.append(v_star_sign)
            else:
                curr_row.append("N/A")
                curr_row.append("N/A")
                curr_row.append("N/A")
                curr_row.append("N/A")
            tabulate_content.append(curr_row)
        print(tabulate(tabulate_content, headers=tabulate_header, tablefmt="psql"))

    def print_villager_compatibility():
        comp_matrix = calculate_compatibility_matrix(villager, data_src)

        tabulate_content = list(
            map(
                lambda d: [d[0]] + list(
                    map(
                        lambda c: "/".join(
                            map(lambda _: str(_), [c['species'], c['personality'], c['star_sign']])
                        ) + " | " + str(evaluate_compatibility(c.values())),
                        d[1]
                    )
                )
                ,
                zip(villager, comp_matrix)
            )
        )
        print(tabulate(
            tabulate_content,
            headers=[""] + villager,
            tablefmt='fancy_grid'
        ))

    print("Islander basic information:")
    print_villager_details()
    print()
    print("Islander compatibility (Species/Personality/StarSign | Result):")
    print_villager_compatibility()


def main():
    compatibility_calculator(['Alice', 'Bob', 'Bree', 'Chow', 'Felicity'])


if __name__ == '__main__':
    main()
