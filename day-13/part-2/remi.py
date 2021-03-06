from tool.runners.python import SubmissionPy

from itertools import permutations

palette = {0: " ", 1: "#", 2: "x", 3: "_", 4: "o"}


class RemiSubmission(SubmissionPy):
    def run(self, s):
        p = [int(n) for n in s.split(",")]
        p[0] = 2

        width = 100
        height = 100

        score = 0
        ball = 0
        paddle = 0

        screen = [[0 for j in range(width)] for i in range(height)]
        cabinet = IntCode(p)
        while not cabinet.exited:
            cabinet.execute()
            while len(cabinet.p_output) >= 3:
                tile = cabinet.p_output.pop()
                y = cabinet.p_output.pop()
                x = cabinet.p_output.pop()
                if x == -1 and y == 0:
                    score = tile
                    continue
                if tile == 3:
                    paddle = x
                elif tile == 4:
                    ball = x
                screen[y][x] = tile

            inpu = 0
            if ball > paddle:
                inpu = 1
            elif ball < paddle:
                inpu = -1
            cabinet.p_input.append(inpu)

        return score

    def display_screen(self, screen):
        for line in screen:
            print("".join(palette[p] for p in line))


class IntCode:
    def __init__(self, p):
        self.p = [0] * (10 * len(p))
        for i, b in enumerate(p):
            self.p[i] = b

        self.pc = 0
        self.p_input = []
        self.p_output = []
        self.exited = False
        self.relative_base = 0

    def get_param_p(self, index):
        param = self.p[self.pc + index + 1]
        opcode = self.p[self.pc]
        modes = opcode // 100
        for _ in range(index):
            modes //= 10
        mode = modes % 10

        if mode == 0:
            return param
        elif mode == 1:
            return None
        elif mode == 2:
            return param + self.relative_base

    def get_param(self, index):
        d = self.get_param_p(index)
        if d is not None:
            return self.p[d]
        else:
            # for immediate mode
            return self.p[self.pc + index + 1]

    def execute(self):
        if self.exited:
            return

        while True:
            opcode = self.p[self.pc]
            if opcode % 100 == 1:
                a = self.get_param(0)
                b = self.get_param(1)
                c = self.get_param_p(2)
                self.p[c] = a + b
                self.pc += 4

            elif opcode % 100 == 2:
                a = self.get_param(0)
                b = self.get_param(1)
                c = self.get_param_p(2)
                self.p[c] = a * b
                self.pc += 4

            elif opcode % 100 == 3:
                try:
                    a = self.get_param_p(0)
                    self.p[a] = self.p_input[0]
                    self.p_input = self.p_input[1:]
                except:
                    return
                self.pc += 2

            elif opcode % 100 == 4:
                self.p_output.append(self.get_param(0))
                self.pc += 2

            elif opcode % 100 == 5:
                a = self.get_param(0)
                b = self.get_param(1)
                if a != 0:
                    self.pc = b
                    continue
                self.pc += 3

            elif opcode % 100 == 6:
                a = self.get_param(0)
                b = self.get_param(1)
                if a == 0:
                    self.pc = b
                    continue
                self.pc += 3

            elif opcode % 100 == 7:
                a = self.get_param(0)
                b = self.get_param(1)
                c = self.get_param_p(2)
                if a < b:
                    self.p[c] = 1
                else:
                    self.p[c] = 0
                self.pc += 4

            elif opcode % 100 == 8:
                a = self.get_param(0)
                b = self.get_param(1)
                c = self.get_param_p(2)
                if a == b:
                    self.p[c] = 1
                else:
                    self.p[c] = 0
                self.pc += 4

            elif opcode % 100 == 9:
                a = self.get_param(0)
                self.relative_base += a
                self.pc += 2

            elif opcode % 100 == 99:
                self.exited = True
                break

        return
