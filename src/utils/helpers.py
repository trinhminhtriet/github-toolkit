def convert_to_int(value: str) -> int:
    if "k" in value.lower():
        return int(float(value.lower().replace("k", "")) * 1000)
    elif "m" in value.lower():
        return int(float(value.lower().replace("m", "")) * 1000000)
    return int(str(value).replace(",", ""))
