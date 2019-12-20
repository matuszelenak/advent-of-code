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
			5: {
				'param_count': 2,
				'function': self.jump_if_true 
			},
			6: {
				'param_count': 2,
				'function': self.jump_if_false
			},
			7: {
				'param_count': 3,
				'function': self.less_than
			},
			8: {
				'param_count': 3,
				'function': self.equals
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

	def jump_if_true(self, params, modes):
		if self.memory_access(params[0], modes[0]) != 0:
			self.ip = self.memory_access(params[1], modes[1])
		else:
			self.ip += 3

	def jump_if_false(self, params, modes):
		if self.memory_access(params[0], modes[0]) == 0:
			self.ip = self.memory_access(params[1], modes[1])
		else:
			self.ip += 3

	def less_than(self, params, modes):
		if self.memory_access(params[0], modes[0]) < self.memory_access(params[1], modes[1]):
			self.memory[params[2]] = 1
		else:
			self.memory[params[2]] = 0
		self.ip += 4

	def equals(self, params, modes):
		if self.memory_access(params[0], modes[0]) == self.memory_access(params[1], modes[1]):
			self.memory[params[2]] = 1
		else:
			self.memory[params[2]] = 0
		self.ip += 4

	def summation(self, params, modes):
		self.memory[params[2]] = self.memory_access(params[0], modes[0]) + self.memory_access(params[1], modes[1])
		self.ip += 4

	def multiplication(self, params, modes):
		self.memory[params[2]] = self.memory_access(params[0], modes[0]) * self.memory_access(params[1], modes[1])
		self.ip += 4

	def input(self, params, modes):
		self.memory[params[0]] = int(input())
		self.ip += 2

	def output(self, params, modes):
		print(self.memory_access(params[0], modes[0]))
		self.ip += 2

	def halt(self, *args):
		print(self.memory)
		exit()

	def compute(self):
		self.ip = 0
		while True:
			instruction = str(self.memory[self.ip])
			opcode, modes = int(instruction[-2:]), instruction[:-2][::-1]
			operation = self.ops[opcode]
			modes = modes + ''.join(['0' for _ in range(operation['param_count'] - len(modes))])
			params = memory[self.ip + 1: self.ip + 1 + operation['param_count']]
			# print()
			# print(self.memory)
			# print(f'IP is {self.ip}')
			# print(opcode, modes, params)
			operation['function'](params, modes)
			# print()


memory = [int(x) for x in input().split(',')]
computer = IntComputer(memory)
computer.compute()
