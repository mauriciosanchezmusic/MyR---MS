import sys
sys.path.insert(0,"../..")

import MyRLex
import MyRParse

while 1:
    try:
        line = input("[MyR] > ")
    except EOFError:
        raise SystemExit
    if not line: continue
    line += "\n"
    prog = MyRParse.parse(line)
    if not prog: continue
