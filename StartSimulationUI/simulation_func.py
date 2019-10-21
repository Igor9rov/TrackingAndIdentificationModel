def simulation(simulation_variant):
    """
    Тело функции, исполненное процессом, должно быть объявлено на верхнем уровне модуля
    Функция запускает цикл по времени для моделируемых объектов
    :param simulation_variant: Вариант моделирования
    :return: None
    """
    # Распаковка
    _, modelling_time, target_list, mfr_list, command_post = simulation_variant
    # Внутренний цикл по времени
    for time in range(20 * modelling_time):
        # Моделирование
        for target in target_list:
            target.operate(time)
        for mfr in mfr_list:
            mfr.operate(time)
        command_post.operate(time)
