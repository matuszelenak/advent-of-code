memory = [int(x) for x in input().split(',')]

ops = {
    1: lambda x, y: x + y,
    2: lambda x, y: x * y
}
pc = 0
while pc < len(memory):
    instruction = memory[pc]
    if instruction not in ops:
        break
    op1 = memory[memory[pc + 1]]
    op2 = memory[memory[pc + 2]]
    memory[memory[pc + 3]] = ops[instruction](op1, op2)
    pc += 4

print(memory)
