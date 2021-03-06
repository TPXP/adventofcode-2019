from tool.runners.python import SubmissionPy


class JonSubmission(SubmissionPy):

    def run(self, s):
        code = [int(v) for v in s.strip().split(",")]

        pos_x, pos_y = (0, 0)
        dir_x, dir_y = (0, 1)

        painted = {(0, 0): 1}

        inputs = [0]
        computer = compute(code, inputs)

        try:
            while True:
                pos = (pos_x, pos_y)
                inputs[0] = painted.get(pos, 0)
                painted[pos] = next(computer)
                turn = next(computer)
                if turn == 0:  # left
                    dir_x, dir_y = -dir_y, dir_x
                elif turn == 1:  # right
                    dir_x, dir_y = dir_y, -dir_x
                pos_x, pos_y = pos_x + dir_x, pos_y + dir_y
        except StopIteration:
            pass

        whites = {p for p, color in painted.items() if color == 1}

        y_max = max(y for _, y in whites)
        y_min = min(y for _, y in whites)
        x_max = max(x for x, _ in whites)
        x_min = min(x for x, _ in whites)

        x_max = max(x_max, x_min + 40 - 1)  # Impose min output width (parser wants 40)

        s = ""
        for y in range(y_max, y_min-1, -1):
            s += "".join("1" if (x, y) in whites else "0" for x in range(x_min, x_max+1)) + "\n"

        # print(s)
        return s


def compute(code, inputs):
    mem = {}
    pc = 0
    relative_base = 0

    def p(i):
        if i in mem:
            return mem[i]
        if 0 <= i < len(code):
            return code[i]
        # raise Exception("Reading uninitialized memory addr={} pc={}".format(i, pc))
        return 0

    def index(pos):
        mode = (p(pc) // 10 ** (1 + pos)) % 10
        if mode == 0:
            return p(pc + pos)
        if mode == 1:
            return pc + pos
        if mode == 2:
            return relative_base + p(pc + pos)
        raise Exception("Bad param mode")

    def param(pos):
        return p(index(pos))

    input_index = 0

    while True:
        op = p(pc) % 100

        if op == 1:
            mem[index(3)] = param(1) + param(2)
            pc += 4
        elif op == 2:
            mem[index(3)] = param(1) * param(2)
            pc += 4
        elif op == 3:
            mem[index(1)] = inputs[input_index]
            # input_index += 1
            pc += 2
        elif op == 4:
            yield param(1)
            pc += 2
        elif op == 5:
            pc = param(2) if param(1) != 0 else pc + 3
        elif op == 6:
            pc = param(2) if param(1) == 0 else pc + 3
        elif op == 7:
            mem[index(3)] = 1 if param(1) < param(2) else 0
            pc += 4
        elif op == 8:
            mem[index(3)] = 1 if param(1) == param(2) else 0
            pc += 4
        elif op == 9:
            relative_base += param(1)
            pc += 2
        elif op == 99:
            break
        else:
            raise Exception("Unknown op code")
