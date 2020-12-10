with open('10.in') as f:
    adapters = sorted([int(x.strip()) for x in f.readlines()])
    adapters = [0] + adapters + [max(adapters) + 3]

    d = {1: 0, 3: 0}
    for curr, _next in zip(adapters, adapters[1:]):
        d[_next - curr] += 1
    print(d[1] * d[3])
