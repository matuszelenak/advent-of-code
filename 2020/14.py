import re

with open('14.in') as f:
    mask = ['X'] * 36
    memory = {}
    for line in f.readlines():
        mask_re = re.match(r'mask = ([01X]+)', line)
        write_re = re.match(r'mem\[(\d+)] = (\d+)', line)
        if mask_re:
            mask = [c for c in mask_re.groups()[0]]
        elif write_re:
            pointer, value = int(write_re.groups()[0]), int(write_re.groups()[1])
            bin_value = [c for c in f'{value:036b}']
            for i, m in enumerate(mask):
                if m in ('0', '1'):
                    bin_value[i] = m
            written = int(''.join(bin_value), 2)
            memory[pointer] = written

    print(sum(memory.values()))