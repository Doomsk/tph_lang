from tph_lang.interpreter.structures import Symbol


def check_int(data):
    return int(data)


def check_float(data):
    return float(data)


def check_str(data):
    if data.isnumeric():
        return int(data)
    return data


literals_types = {int: check_int, float: check_float, str: check_str}


def no_literal(data):
    return False


def check_literal(data):
    if isinstance(data, Symbol):
        return literals_types.get(type(data.value), no_literal)(data.value)
    raise ValueError(f"cannot check literal '{data}' of type {type(data)}.")
