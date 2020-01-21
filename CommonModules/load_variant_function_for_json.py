def object_pairs_hook(list_of_pairs) -> dict:
    """Модифицированный обработчик для json файла, нужен чтобы ключи в json, которые не могут быть числами
    (они автоматически конвертируются в строки) стали снова целыми числами при загрузке данных в переменные

    :param list_of_pairs: Массив с парами ключ значение из json файла
    :return: Словарь с ключом и значением
    :rtype: dict
    """
    try:
        # Если ключ конвертится в int, то это либо номер МФР, либо номер цели
        return {int(pair[0]): pair[1] for pair in list_of_pairs}
    except ValueError:
        return dict(list_of_pairs)
