from functools import reduce


def play_game(stack_1, stack_2):
    game_cache = set()

    while min(len(stack_1), len(stack_2)) > 0:
        if (tuple(stack_1), tuple(stack_2)) in game_cache:
            return stack_1, 'p1'

        game_cache.add((tuple(stack_1), tuple(stack_2)))
        a, s1 = stack_1[0], stack_1[1:]
        b, s2 = stack_2[0], stack_2[1:]

        if len(s1) >= a and len(s2) >= b:
            winning_stack, round_winner = play_game(s1[:a], s2[:b])
        else:
            if a > b:
                round_winner = 'p1'
            else:
                round_winner = 'p2'

        if round_winner == 'p1':
            stack_1 = s1 + [a, b]
            stack_2 = s2
        else:
            stack_1 = s1
            stack_2 = s2 + [b, a]

    if len(stack_1) > 0:
        return stack_1, 'p1'
    else:
        return stack_2, 'p2'


def get_score(stack):
    return reduce(int.__add__, [(i + 1) * value for i, value in enumerate(stack[::-1])])


with open('22.in') as f:
    p1, p2 = f.read().split('\n\n')
    p1 = [int(x) for x in p1.split('\n')[1:]]
    p2 = [int(x) for x in p2.split('\n')[1:]]

    winning, winner = play_game(p1, p2)
    print(get_score(winning))
