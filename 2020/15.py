from collections import defaultdict

spoken = [19, 0, 5, 1, 10, 13]

spoken_on_turn = defaultdict(list)
for t, number in enumerate(spoken):
    spoken_on_turn[number].append(t + 1)

turn = len(spoken) + 1
while turn <= 30000000:
    last_spoken = spoken[-1]
    if len(spoken_on_turn[last_spoken]) == 1:
        spoken_on_turn[0].append(turn)
        spoken.append(0)
    else:
        a, b = spoken_on_turn[last_spoken][-2:]
        spoken_on_turn[b - a].append(turn)
        spoken.append(b - a)

    turn += 1

print(spoken[-1])
