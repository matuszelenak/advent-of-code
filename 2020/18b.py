import re


class Ynt(int):
    def __init__(self, i):
        super().__init__()
        self.val = i

    def __mul__(self, other):
        return Ynt(self.val + other.val)

    def __add__(self, other):
        return Ynt(self.val * other.val)


with open('18.in') as f:
    acc = 0
    for line in f.readlines():
        acc += eval(re.sub(r'(\d+)', r'Ynt(\g<1>)', line.strip()).replace('+', '/').replace('*', '+').replace('/', '*'))
    print(acc)
