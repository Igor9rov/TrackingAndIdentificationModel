"""Модуль определяет жёстко связанные с результатом моделирования функции для записи в csv файл
При изменении структуры возвращаемого функцией моделирования значения требует рефакторинга."""
import csv


def write_cp_registration(registration: list, path: str):
    """Записывает в файл регистрацию от ПБУ

    :param registration: Регистрация в виде списка списков
    :param path: Путь к файлу, где будут храниться данные

    :return: None
    """
    with open(path, "w", newline="") as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        # Первый цикл идёт по различным итерациям
        for index_of_iteration, one_iteration in enumerate(registration):
            # В каждой итерации в нулевом элементе лежит регистрация ПБУ
            cp_registration = one_iteration[0]
            # Одна строчка из регистрации ПБУ составляет строчку в csv файле
            for line in cp_registration:
                # Добавление последнего столбца с номером выполненной итерации
                line.append(index_of_iteration)
                writer.writerow(line)


def write_mfr_registration(registration: list, path: str):
    """Записывает в файл регистрацию от всех МФР

    :param registration: Регистрация в виде списка списков
    :param path: Путь к файлу, где будут храниться данные

    :return: None
    """
    with open(path, "w", newline="") as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        # Первый цикл идёт по различным итерациям
        for index_of_iteration, one_iteration in enumerate(registration):
            # В каждой итерации в первом элементе лежит регистрация МФР в виде списка из регистраций каждого МФР
            all_mfr_registration = one_iteration[1]
            # Для регистрации от каждого МФР
            for one_mfr_registration in all_mfr_registration:
                # Одна строчка из регистрации МФР составляет строчку в csv файле
                for line in one_mfr_registration:
                    # Добавление последнего столбца с номером выполненной итерации
                    line.append(index_of_iteration)
                    writer.writerow(line)
