count_of_days = int(input())
temperature_in_days = list(map(int, input().split(" ")))

current_min = count_of_days + 1
for index_current, temp_current in enumerate(temperature_in_days):
    needed_diff = []
    for other_index, other_temp in enumerate(temperature_in_days):
        if index_current == other_index:
            pass
        else:
            if -6 < temp_current - other_temp < 6:
                min_range = abs(index_current - other_index)-1
                if min_range < current_min:
                    current_min = min_range
if current_min == count_of_days + 1:
    print(-1)
else:
    print(current_min)

