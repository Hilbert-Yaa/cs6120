import json
import sys
from pprint import pprint

TERMINATORS = 'jmp', 'br', 'ret'
NAME_PREFIX = 'anon'


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


def form_blocks(func):
    cur_block = []
    for instr in func['instrs']:
        if 'op' in instr:
            # an actual instruction
            cur_block.append(instr)
            if instr['op'] in TERMINATORS and cur_block:
                yield cur_block
                cur_block = []
        else:
            # a label statement
            if cur_block:
                yield cur_block
            cur_block = [instr, ]
    if cur_block:
        yield cur_block


def name_gen():
    cnt = 0
    while True:
        yield f"{NAME_PREFIX}{cnt}"
        cnt += 1


def map_blocks(blocks):
    block_map = {}
    anon_name = name_gen()

    for block in blocks:
        if 'label' in block[0]:
            # a labeled block
            name = block[0]['label']
            block_map[name] = block[1:]
        else:
            # an anonymous block
            name = next(anon_name)
            block_map[name] = block
    return block_map


def prog_to_cfg(prog):
    for func in prog['functions']:
        blocks = list(form_blocks(func))
        pprint(blocks)
        block_map = map_blocks(blocks)
        pprint(block_map)


if __name__ == '__main__':
    prog = json.load(sys.stdin)
    prog_to_cfg(prog)
