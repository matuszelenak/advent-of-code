def fuel_mass(fuel):
    partial = fuel // 3 - 2
    if partial > 0:
        return partial + fuel_mass(partial)
    return 0


print(sum(map(lambda l: fuel_mass(int(l.strip())), open('1.in').readlines())))
