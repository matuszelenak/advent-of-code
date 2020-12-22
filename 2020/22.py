from functools import reduce

with open('22.in') as f:
    p1, p2 = f.read().split('\n\n')
    p1 = [int(x) for x in p1.split('\n')[1:]]
    p2 = [int(x) for x in p2.split('\n')[1:]]

    while min(len(p1), len(p2)) > 0:
        p1_card, p1_rest = p1[0], p1[1:]
        p2_card, p2_rest = p2[0], p2[1:]
        if p1_card > p2_card:
            p1 = p1_rest + [p1_card, p2_card]
            p2 = p2_rest
        else:
            p2 = p2_rest + [p2_card, p1_card]
            p1 = p1_rest

    print(p1)
    print(p2)

    winning_stack = (p1 or p2)[::-1]
    score = reduce(int.__add__, [(i + 1) * value for i, value in enumerate(winning_stack)])
    print(score)