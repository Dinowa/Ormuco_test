def compareVersion(version1: str, version2: str) -> str:
    v1, v2 = version1.split('.'), version2.split('.')
    d1, d2 = {}, {}
    for i in range(len(v1)):
        d1[i] = int(v1[i])
    for i in range(len(v2)):
        d2[i] = int(v2[i])
    for i in range(max(len(d1), len(d2))):
        tmp = d1.get(i, 0) - d2.get(i, 0)
        if tmp > 0:
            return f'{version1} is larger than {version2}'
        elif tmp < 0:
            return f'{version1} is smaller than {version2}'
    return f'{version1} is the same as {version2}'