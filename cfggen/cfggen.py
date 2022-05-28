import json
import sys
from pprint import pprint
from collections import OrderedDict

TERMINATORS = 'jmp', 'br', 'ret'
NAME_PREFIX = 'anon'


class CFGBasicBlock(object):
    def __init__(self, label, instrs):
        self.label = label
        self.instrs = instrs
        self.preds = []
        self.succs = []

    def __len__(self):
        return len(self.instrs)

    def __getitem__(self, key):
        return self.instrs[key]

    def __repr__(self):
        return f"block <{self.label}> of size {len(self.instrs)}"


class CFG(object):
    def __init__(self, blocks):
        self.blocks = blocks
        self.label_map = {}
        for idx, block in enumerate(blocks):
            self.label_map[block.label] = idx
        self.build_graph()

    def build_graph(self):
        for cur_idx, cur_block in enumerate(self.blocks):
            last_instr = cur_block[-1]
            if 'labels' in last_instr:
                # a branching instruction
                cur_block.succs = last_instr['labels']
                for succ in cur_block.succs:
                    succ_idx = self.label_map[succ]
                    self.blocks[succ_idx].preds.append(cur_block.label)
            elif last_instr['op'] == 'ret':
                # end of the function body
                pass
            else:
                # a fall-through block
                if cur_idx == len(self.blocks) - 1:
                    pass
                else:
                    next_block = self.blocks[cur_idx + 1]
                    cur_block.succs.append(next_block.label)
                    next_block.preds.append(cur_block.label)

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


def label_gen():
    cnt = 0
    while True:
        yield f"{NAME_PREFIX}{cnt}"
        cnt += 1


def map_blocks(blocks):
    labeled_blocks = []
    anon_label = label_gen()

    for block in blocks:
        if 'label' in block[0]:
            # a labeled block
            label = block[0]['label']
            cur_block = CFGBasicBlock(label, block[1:])
            labeled_blocks.append(cur_block)
        else:
            # an anonymous block
            label = next(anon_label)
            cur_block = CFGBasicBlock(label, block)
            labeled_blocks.append(cur_block)
    return labeled_blocks


def form_cfg(labeled_blocks):
    cfg = CFG(labeled_blocks)
    return cfg


def prog_to_cfg(prog):
    for func in prog['functions']:
        blocks = list(form_blocks(func))
        labeled_blocks = map_blocks(blocks)
        # pprint(block_map)
        cfg = form_cfg(labeled_blocks)


if __name__ == '__main__':
    prog = json.load(sys.stdin)
    prog_to_cfg(prog)
