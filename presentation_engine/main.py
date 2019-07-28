import sys
from FlyIoTLParser import *


filepath = sys.argv[1]

if filepath:
    parser = FlyIoTLParser(filepath)
    parser.syntax_validate()
    parser.semantic_validate()
