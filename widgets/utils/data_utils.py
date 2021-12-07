def get_save_data_from_lineedit(lineedit, value_type=int):
    try:
        value_type = value_type(lineedit.text())
        return value_type
    except ValueError:
        return value_type()


def get_save_data_array_from_lineedit(lineedit, delimiter=' ', value_type=int):
    try:
        values_type = [value_type(item) for item in lineedit.text().split(delimiter)]
        return values_type
    except ValueError:
        return [value_type()]