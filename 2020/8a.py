import re

with open('8.in') as f:
    instructions = [x.strip() for x in f.readlines()]
    acc, ip, executed = 0, 0, set()
    while True:
        if ip in executed:
            print(acc)
            break
        executed.add(ip)
        cmd, val = re.match(r'(acc|jmp|nop) ([+\-][\d]+)', instructions[ip]).groups()
        val = int(val)
        if cmd == 'acc':
            acc += val
        elif cmd == 'jmp':
            ip += val
            continue

        ip += 1
