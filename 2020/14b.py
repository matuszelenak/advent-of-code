import re
import itertools

with open('14.in') as f:
    mask = ['0'] * 36
    x_positions = []
    memory = {}
    for line in f.readlines():
        mask_re = re.match(r'mask = ([01X]+)', line)
        write_re = re.match(r'mem\[(\d+)] = (\d+)', line)
        if mask_re:
            mask = [c for c in mask_re.groups()[0]]
            x_positions = [i for i, c in enumerate(mask) if c == 'X']
        elif write_re:
            pointer, value = int(write_re.groups()[0]), int(write_re.groups()[1])
            bin_pointer = [c for c in f'{pointer:036b}']

            for i, c in enumerate(mask):
                if c == '1':
                    bin_pointer[i] = '1'

            x_count = len([c for c in mask if c == 'X'])
            for bit_group in itertools.product(['0', '1'], repeat=x_count):
                modified_bin_pointer = bin_pointer[::]
                for x_pos, set_bit in zip(x_positions, bit_group):
                    modified_bin_pointer[x_pos] = set_bit

                write_pointer = int(''.join(modified_bin_pointer), 2)
                memory[write_pointer] = value

    print(sum(memory.values()))