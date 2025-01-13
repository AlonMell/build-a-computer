import sys
from hackAssembler import HackAssembler

assembler = HackAssembler()
assembler.Run(f"./{sys.argv[1]}.asm")

with open(f"./{sys.argv[1]}.hack", "r") as f1, open(f"./tests/{sys.argv[1]}.hack", "r") as f2:
    if f1.read() != f2.read():
        raise Exception("Files not equal!")

print("Test successfull!")
