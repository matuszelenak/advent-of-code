import re
import copy

with open('8.in') as f:
    original_instructions = [list(re.match(r'(acc|jmp|nop) ([+\-][\d]+)', x.strip()).groups()) for x in f.readlines()]
    swap = {'jmp': 'nop', 'nop': 'jmp'}
    jmp_or_nop = [pos for pos, cmd in enumerate(original_instructions) if cmd[0] in swap.keys()]

    for swap_position in jmp_or_nop:
        instructions = copy.deepcopy(original_instructions)
        instructions[swap_position][0] = swap[instructions[swap_position][0]]

        acc, ip, executed = 0, 0, set()
        while ip < len(instructions) and ip not in executed:
            executed.add(ip)
            cmd, val = instructions[ip]
            val = int(val)
            if cmd == 'acc':
                acc += val
            elif cmd == 'jmp':
                ip += val
                continue

            ip += 1

        if ip == len(instructions):
            print(acc)
