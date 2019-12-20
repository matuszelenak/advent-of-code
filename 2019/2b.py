def perform_computation(memory):
	ops = {
	1: lambda x,y: x + y,
	2: lambda x,y: x * y
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

	return memory

initial_memory = [int(x) for x in input().split(',')]
for noun in range(100):
	for verb in range(100):
		modified_memory = initial_memory[::]
		modified_memory[1] = noun
		modified_memory[2] = verb

		computed = perform_computation(modified_memory)
		if computed[0] == 19690720:
			print(noun, verb, 100 * noun + verb)
			exit()
