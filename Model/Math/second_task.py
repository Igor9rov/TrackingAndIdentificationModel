count_of_people = int(input())
people_list = list(map(int, input().split(" ")))

set_companies = set(people_list)


def any_people_is_near(comp, other_comp):
    for index, person in enumerate(people_list):
        try:
            next_person = people_list[index+1]
        except IndexError:
            next_person = people_list[0]
        try:
            back_person = people_list[index-1]
        except IndexError:
            back_person = people_list[count_of_people]
        return (person == comp) and (next_person or back_person) == other_comp


micro_count = 1
copy_people_list = people_list[:]
for comp in set_companies:
    for other_comp in set_companies:
        if comp == other_comp:
            pass
        else:
            if any_people_is_near(comp, other_comp):
                for people in copy_people_list:
                    if people == comp:
                        people = micro_count
                micro_count += 1
                for people in copy_people_list:
                    if people == other_comp:
                        people = micro_count
            else:
                for people in copy_people_list:
                    if people == comp or people == other_comp:
                        people = micro_count
if len(set_companies) == 1:
    print("1")
    print(" ".join(map(str, [1]*count_of_people)))
else:
    print(str(len(set(copy_people_list))))
    print(" ".join(map(str, copy_people_list)))
