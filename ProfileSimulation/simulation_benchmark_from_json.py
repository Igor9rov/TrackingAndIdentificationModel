"""Файл предназначен для профилирования процесса моделирования, объекты подгружаем из json"""

import json
import sys

from generated_variant import GeneratedVariant
from load_variant_function_for_json import object_pairs_hook

if __name__ == "__main__":
    try:
        # Откроем вариант моделирования
        with open("TestVariant.json", "r") as read_file:
            # Сгенерили вариант
            variant = GeneratedVariant(json.load(read_file, object_pairs_hook=object_pairs_hook))
    except FileNotFoundError:
        print("Нет файла с вариантом моделирования, выкачайте его из SVN, или создайте в GUI.")
        sys.exit(-1)
    except Exception as e:
        print(e)
        sys.exit(-1)

    # Объекты
    target_list, mfr_list, command_post = variant.objects

    # Не имеет смысла профилировать многократное моделирование одного и того же, поэтому цикл только один
    for time in range(20 * variant.modelling_time):
        # Моделирование
        for target in target_list:
            target.operate(time)
        for mfr in mfr_list:
            mfr.operate(time)
        command_post.operate(time)
