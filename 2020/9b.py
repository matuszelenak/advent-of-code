import itertools

with open('9.in') as f:
    numbers = [int(x.strip()) for x in f.readlines()]
    prefix_sum = []
    acc = 0
    for num in numbers:
        prefix_sum.append(acc)
        acc += num

    wrong = None
    for i in range(25, len(numbers)):
        s = numbers[i - 25:i]
        combs = [int.__add__(*x) for x in itertools.combinations(s, 2)]
        if numbers[i] not in combs:
            wrong = numbers[i]
            break

    for start, end in itertools.combinations(list(range(len(numbers))), 2):
        if prefix_sum[end] - prefix_sum[start] == wrong:
            print(max(numbers[start:end]) + min(numbers[start:end]))
            break

        if start > end:
            continue
