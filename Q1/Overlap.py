def overlap(l1, l2):
    """return True if two lines overlap else False """
    l1, l2 = list(l1), list(l2)
    l1.sort()
    l2.sort()
    lines = [l1, l2]
    lines.sort(key=lambda x: x[0])
    if lines[0][1] >= lines[1][0]:
        return True
    return False

