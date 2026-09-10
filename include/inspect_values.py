
def is_present(value):
    """
    define a function that decides if a value is present or missing
    """
    if value is None:
        return False
    if isinstance(value, str) and value.strip() == ".":
        return False
    if isinstance(value, str) and value.strip() == "":
        return False
    if isinstance(value, (list, dict)) and len(value) == 0:
        return False
    if isinstance(value, (int, float)) and value == 0:
        return False
    return True

def join_present(*args):
    """
    define a function that takes multiple values and coalasce them into a concatenated string
    """
    result = []
    for value in args:
        if is_present(value):
            result.append(str(value))
    return ", ".join(result)