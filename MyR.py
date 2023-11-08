import sys
sys.path.insert(0,"../..")

import MyRLex
import MyRCubo
import MyRParse

fileToRead = sys.argv[1]
file = open(fileToRead, 'r')
data = file.read()

prog = MyRParse.parse(data)

file.close()
