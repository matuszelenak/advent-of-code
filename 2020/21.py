import re
from collections import defaultdict
from functools import reduce

with open('21.in') as f:
    allergen_contained_in = defaultdict(list)
    ingredient_lists = []
    ingredient_occurrences = defaultdict(int)
    for line in f.readlines():
        ingredients, allergens = re.match(r'([\w ]+)\(contains ([\w, ]+)\)', line).groups()
        ingredients = set(ingredients.strip().split(' '))
        for ingredient in ingredients:
            ingredient_occurrences[ingredient] += 1

        allergens = allergens.strip().split(', ')
        ingredient_lists.append(ingredients)
        for allergen in allergens:
            allergen_contained_in[allergen].append(ingredients)

    determined = {}
    undetermined_allergens = set(allergen_contained_in.keys())
    while True:
        if len(undetermined_allergens) == 0:
            break

        for allergen in undetermined_allergens:
            reduced = reduce(set.__and__, allergen_contained_in[allergen])
            if len(reduced) == 1:
                determined_ingredient = next(iter(reduced))
                undetermined_allergens.discard(allergen)
                determined[determined_ingredient] = allergen

                for ingredient_list in ingredient_lists:
                    ingredient_list.discard(determined_ingredient)

                break

    acc = 0
    for ingredient in set(ingredient_occurrences.keys()) - set(determined.keys()):
        acc += ingredient_occurrences[ingredient]
    print(acc)

    print(','.join(list(sorted(determined.keys(), key=lambda x: determined[x]))))
