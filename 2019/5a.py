import itertools

class IntComputer:
	def __init__(self, memory):
		self.memory = memory
		self.ops = ops = {
			1: {
				'param_count': 3,
				'function': self.summation
			},
			2:{
				'param_count': 3,
				'function': self.multiplication
			},
			3: {
				'param_count': 1,
				'function': self.input
			},
			4: {
				'param_count': 1,
				'function': self.output
			},
			99: {
				'param_count': 0,
				'function': self.halt
			}
		}

	def memory_access(self, value, mode):
		if mode == '0':
			return self.memory[value]
		return value

	def summation(self, params, modes):
		self.memory[params[2]] = self.memory_access(params[0], modes[0]) + self.memory_access(params[1], modes[1])

	def multiplication(self, params, modes):
		self.memory[params[2]] = self.memory_access(params[0], modes[0]) * self.memory_access(params[1], modes[1])

	def input(self, params, modes):
		self.memory[params[0]] = int(input())

	def output(self, params, modes):
		print(self.memory[params[0]])

	def halt(self, *args):
		print(self.memory)
		exit()

	def compute(self):
		ip = 0
		while ip < len(self.memory):
			instruction = str(self.memory[ip])
			opcode, modes = int(instruction[-2:]), instruction[:-2][::-1]
			operation = self.ops[opcode]
			modes = modes + ''.join(['0' for _ in range(operation['param_count'] - len(modes))])

			operation['function'](memory[ip + 1: ip + 1 + operation['param_count']], modes)

			ip += (1 + len(modes))


memory = [int(x) for x in input().split(',')]
computer = IntComputer(memory)
computer.compute()
