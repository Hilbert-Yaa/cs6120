import sys
import json
from cfggen import prog_to_cfg

def cfg_to_dot(name, cfg):
    print(f"digraph {name} {{")
    for label in cfg.label_map.keys():
        print(f"\t{label};")
    for block in cfg.blocks:
        for succ in block.succs:
            print(f"\t{block.label} -> {succ};")
    print('}')


if __name__ == '__main__':
    prog = json.load(sys.stdin)
    cfgs = prog_to_cfg(prog)
    for name, cfg in cfgs.items():
        cfg_to_dot(name, cfg)