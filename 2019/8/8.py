pixels = list(map(int, input()))
layers = [pixels[i: i + 25*6] for i in range(0, len(pixels), 25*6)]
with_zero_count = list(map(lambda x: (sum(pixel == 0 for pixel in x), x), layers))
best = sorted(with_zero_count)[0][1]
print(sum(pixel == 1 for pixel in best) * sum(pixel == 2 for pixel in best))
