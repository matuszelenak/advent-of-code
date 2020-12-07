print(sum([len(__import__('functools').reduce(set.__and__, map(set, x.split('\n')))) for x in open('6.in').read().split('\n\n')]))
