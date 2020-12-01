d = {
    0: '.',
    1: '#'
}
pixels = list(map(int, input()))
stacks = [list(filter(lambda pixel: pixel != 2, [pixels[base + i * 25 * 6] for i in range(100)]))[0] for base in range(25 * 6)]
for row in range(6):
    print(''.join(map(lambda p: d[p], stacks[row * 25: (row + 1) * 25])))
