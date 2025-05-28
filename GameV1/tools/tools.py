

def any_true(items, tests: int | list):
    if tests.__class__ == list:
        for t in tests:
            if items[t]:
                return True
    else:
        if items[tests]:
            return True
    return False

