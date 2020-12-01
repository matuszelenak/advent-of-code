from collections import defaultdict
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
    OP_REL = 9
    OP_HALT = 99

    def __init__(self, memory, inputs, outputs):
        self.memory = memory
        self.inputs = inputs
        self.outputs = outputs
        self.halted = False
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
            },
            self.OP_REL: {
                'param_count': 1,
                'function': self.relative_base
            }
        }

    def memory_read(self, value, mode):
        if mode == 0:
            return self.memory[value]
        if mode == 1:
            return value
        if mode == 2:
            return self.memory[self.base + value]
        raise RuntimeError

    def memory_write(self, value, address, mode):
        if mode == 0:
            self.memory[address] = value
            return
        if mode == 2:
            self.memory[address + self.base] = value
            return
        raise RuntimeError

    def relative_base(self, params, modes):
        self.base += self.memory_read(params[0], modes[0])
        self.ip += 2

    def jump_if_true(self, params, modes):
        if self.memory_read(params[0], modes[0]) != 0:
            self.ip = self.memory_read(params[1], modes[1])
        else:
            self.ip += 3

    def jump_if_false(self, params, modes):
        if self.memory_read(params[0], modes[0]) == 0:
            self.ip = self.memory_read(params[1], modes[1])
        else:
            self.ip += 3

    def less_than(self, params, modes):
        if self.memory_read(params[0], modes[0]) < self.memory_read(params[1], modes[1]):
            self.memory_write(1, params[2], modes[2])
        else:
            self.memory_write(0, params[2], modes[2])
        self.ip += 4

    def equals(self, params, modes):
        if self.memory_read(params[0], modes[0]) == self.memory_read(params[1], modes[1]):
            self.memory_write(1, params[2], modes[2])
        else:
            self.memory_write(0, params[2], modes[2])
        self.ip += 4

    def summation(self, params, modes):
        result = self.memory_read(params[0], modes[0]) + self.memory_read(params[1], modes[1])
        self.memory_write(result, params[2], modes[2])
        self.ip += 4

    def multiplication(self, params, modes):
        result = self.memory_read(params[0], modes[0]) * self.memory_read(params[1], modes[1])
        self.memory_write(result, params[2], modes[2])
        self.ip += 4

    def input(self, params, modes):
        self.memory_write(self.inputs.get(), params[0], modes[0])
        self.ip += 2

    def output(self, params, modes):
        self.outputs.put(self.memory_read(params[0], modes[0]))
        self.ip += 2

    def run(self) -> None:
        self.ip = 0
        self.base = 0
        while True:
            instruction = str(self.memory[self.ip])
            opcode, modes = int(instruction[-2:]), list(map(int, instruction[:-2][::-1]))
            if opcode == self.OP_HALT:
                self.halted = True
                return

            operation = self.ops[opcode]
            modes = modes + [0 for _ in range(operation['param_count'] - len(modes))]
            params = self.memory[self.ip + 1: self.ip + 1 + operation['param_count']]
            # print(opcode, modes, params)
            operation['function'](params, modes)


robot_x, robot_y = 0, 0
directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
current_direction = 0
grid = defaultdict(lambda: 0)

memory = [int(x) for x in input().split(',')] + [0 for _ in range(1000000)]
inp = Queue()
out = Queue()
c = IntComputer(memory, inp, out)
c.start()
inp.put(1)
while not c.halted:
    color = c.outputs.get()
    turn = c.outputs.get()
    if turn == 0:  # Turn left
        current_direction = (current_direction - 1 + len(directions)) % len(directions)
    else:  # Turn right
        current_direction = (current_direction + 1 + len(directions)) % len(directions)

    grid[f'{robot_x},{robot_y}'] = color

    robot_x += directions[current_direction][0]
    robot_y += directions[current_direction][1]

    inp.put(grid[f'{robot_x},{robot_y}'])

c.join()

print(len(grid))

grid_list = [list(map(int, coordinates.split(','))) for coordinates, color in grid.items()]
min_x, max_x = min(map(lambda c: c[0], grid_list)), max(map(lambda c: c[0], grid_list))
min_y, max_y = min(map(lambda c: c[1], grid_list)), max(map(lambda c: c[1], grid_list))
for y in range(min_y, max_y + 1):
    for x in range(min_x, max_x + 1):
        cell = grid[f'{x},{y}']
        if cell == 0:
            print(' ', end='')
        else:
            print('#', end='')
    print()
# print(list(c.outputs.queue))
