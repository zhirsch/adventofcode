#!/usr/bin/python3


def exactly2(n):
    for x in range(10):
        if str(x) * 2 not in n:
            continue
        if str(x) * 3 in n:
            continue
        if str(x) * 4 in n:
            continue
        if str(x) * 5 in n:
            continue
        if str(x) * 6 in n:
            continue
        return True
    return False


def ok(n):
    n = str(n)
    if len(n) != 6:
        return False
    if not exactly2(n):
        return False
    if not all(n[i] <= n[i + 1] for i in range(5)):
        return False
    return True

# print(ok(112233))
# print(ok(123444))
# print(ok(111122))


lb = 172930
ub = 683082

count = 0
for n in range(lb, ub + 1):
    if ok(n):
        count += 1
print(count)
