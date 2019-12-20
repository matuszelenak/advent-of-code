import itertools
from queue import Queue
from threading import Thread


class IntComputer(Thread):
    OP_SUM = 1
    OP_MULT = 2
    OP_IN = 3
    OP_OUT = 4
    OP_JIT = 5
    OP_JIF = 6
    OP_LT = 7
    OP_EQ = 8
    OP_HALT = 99

    def __init__(self, memory, inputs, outputs):
        self.memory = memory
        self.inputs = inputs
        self.outputs = outputs
        super().__init__()
        self.ops = {
            self.OP_SUM: {
                'param_count': 3,
                'function': self.summation
            },
            self.OP_MULT: {
                'param_count': 3,
                'function': self.multiplication
            },
            self.OP_IN: {
                'param_count': 1,
                'function': self.input
            },
            self.OP_OUT: {
                'param_count': 1,
                'function': self.output
            },
            self.OP_JIT: {
                'param_count': 2,
                'function': self.jump_if_true
            },
            self.OP_JIF: {
                'param_count': 2,
                'function': self.jump_if_false
            },
            self.OP_LT: {
                'param_count': 3,
                'function': self.less_than
            },
            self.OP_EQ: {
                'param_count': 3,
                'function': self.equals
            }
        }

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
        self.memory[params[0]] = self.inputs.get()
        self.ip += 2

    def output(self, params, modes):
        self.outputs.put(self.memory_access(params[0], modes[0]))
        self.ip += 2

    def memory_access(self, value, mode):
        if mode == '0':
            return self.memory[value]
        return value

    def run(self) -> None:
        self.ip = 0
        while True:
            instruction = str(self.memory[self.ip])
            opcode, modes = int(instruction[-2:]), instruction[:-2][::-1]
            if opcode == self.OP_HALT:
                return

            operation = self.ops[opcode]
            modes = modes + ''.join(['0' for _ in range(operation['param_count'] - len(modes))])
            params = self.memory[self.ip + 1: self.ip + 1 + operation['param_count']]
            operation['function'](params, modes)


memory = [int(x) for x in input().split(',')]

signals = []
for configuration in itertools.permutations(range(5, 10)):
    queues = [Queue() for _ in configuration]
    [q.put(phase) for q, phase in zip(queues, configuration)]
    computers = [IntComputer(memory[::], in_queue, out_queue) for in_queue, out_queue in zip(queues, queues[1:] + [queues[0]])]
    queues[0].put(0)
    [x.start() for x in computers]
    computers[-1].join()

    signals.append(list(computers[-1].outputs.queue)[0])

print(max(signals))
