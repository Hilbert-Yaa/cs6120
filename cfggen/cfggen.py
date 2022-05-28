import json
import sys

TERMINATORS = 'jmp', 'br', 'ret'


class CFGBasicBlock(object):
    def __init__(self, instrs):
        self.instrs = instrs
        self.preds = []
        self.succs = []

    def __repr__(self):
        for instr in self.instrs:
            print(instr)


class CFG(object):
    def __init__(self, blocks):
        self.blocks = blocks

    def __repr__(self):
        pass


def form_blocks(prog):
    for instr in prog:
        pass


def map_blocks(prog, blocks):
    pass


def prog_to_cfg(prog):
    pass


def cfg():
    prog = json.load(sys.stdin)
    print(prog)


if __name__ == '__main__':
    cfg()
