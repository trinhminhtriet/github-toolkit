def convert_to_int(value):
    return int(str(value).replace(",", ""))


def intval_star(value):
    if "," in str(value):
        value = str(value).replace(",", "")
    if "k" in value:
        return int(float(value.replace("k", "")) * 1000)
    elif "m" in value:
        return int(float(value.replace("m", "")) * 1000000)
    else:
        return int(value)
