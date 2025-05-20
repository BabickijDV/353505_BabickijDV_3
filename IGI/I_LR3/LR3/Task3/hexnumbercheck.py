def check(str):
    """Check str on hex number

    Return boolean
    """
    for c in str:
        if not (c >= "0" and c <= "9" or c >= "A" and c <= "F"):
            return False
    return True