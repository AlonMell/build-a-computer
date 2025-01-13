import sys
import os
from typing import TextIO

"""TODO List:
Probably put tables in separate file
Enhancement preCompile
Handle comments in the instrucation,
    probably do intermediate view with "clean" string
In-depth Exceptions
Probably use argparse
Short comments near hard logic
Tests
"""

class HackAssembler:
    def __init__(self):
        self.__symbolTable = {
            "R0": 0,
            "R1": 1,
            "R2": 2,
            "R3": 3,
            "R4": 4,
            "R5": 5,
            "R6": 6,
            "R7": 7,
            "R8": 8,
            "R9": 9,
            "R10": 10,
            "R11": 11,
            "R12": 12,
            "R13": 13,
            "R14": 14,
            "R15": 15,
            "SCREEN": 16384,
            "KBD": 24576,
            "SP": 0,
            "LCL": 1,
            "ARG": 2,
            "THIS": 3,
            "THAT": 4
        }

        self.__dest = {
            "null": "000",
            "M": "001",
            "D": "010",
            "DM": "011",
            "A": "100",
            "AM": "101",
            "AD": "110",
            "ADM": "111"
        }

        self.__comp = {
            "0": "0101010",
            "1": "0111111",
            "-1": "0111010",
            "D": "0001100",
            "A": "0110000",
            "M": "1110000",
            "!D": "0001101",
            "!A": "0110001",
            "!M": "1110001",
            "-D": "0001111",
            "-A": "0110011",
            "-M": "1110011",
            "D+1": "0011111",
            "A+1": "0110111",
            "M+1": "1110111",
            "D-1": "0001110",
            "A-1": "0110010",
            "M-1": "1110010",
            "D+A": "0000010",
            "D+M": "1000010",
            "D-A": "0010011",
            "D-M": "1010011",
            "A-D": "0000111",
            "M-D": "1000111",
            "D&A": "0000000",
            "D&M": "1000000",
            "D|A": "0010101",
            "D|M": "1010101"
        }

        self.__jump = {
            "null": "000",
            "JGT": "001",
            "JEQ": "010",
            "JGE": "011",
            "JLT": "100",
            "JNE": "101",
            "JLE": "110",
            "JMP": "111"
        }

        self.__cTable = {
            "dest": self.__dest,
            "comp": self.__comp,
            "jump": self.__jump,
        }

        self.__MACHINE_WORD = 16
        self.__START_VAR_ADDR = 16

        self.__A = "@"
        self.__LABEL = "("
        self.__COMMENT = "//"

    def __skipLine(self, line: str) -> bool:
        return (not line.strip()
                or self.__isStartsWith(line, self.__COMMENT))

    def __isStartsWith(self, line: str, symb: str) -> bool:
        return line.strip().startswith(symb)

    def __handleLabel(self, line: str, lineNumber: int) -> None:
        label = line.strip()[1:-1]
        if label not in self.__symbolTable:
            self.__symbolTable[label] = lineNumber

    #TODO: Handle comments
    def __preCompile(self, asmFile: TextIO) -> None:
        lineNumber = 0

        for line in asmFile:
            if self.__skipLine(line):
                continue
            elif self.__isStartsWith(line, self.__LABEL):
                self.__handleLabel(line, lineNumber)
                continue
            lineNumber += 1

    def __handleAInstruction(
        self,
        line: str,
        varAddr: list[int]
    ) -> str:
        aInstr = line.strip()[1:]

        if aInstr.isdigit():
            return bin(int(aInstr))[2:].zfill(self.__MACHINE_WORD)
        elif aInstr not in self.__symbolTable:
            self.__symbolTable[aInstr] = varAddr[0]
            varAddr[0] += 1

        return bin(self.__symbolTable[aInstr])[2:].zfill(self.__MACHINE_WORD)

    def __parse(self, line: str) -> str:
        firstLexIdx, secondLexIdx = line.find("="), line.find(";")
        isFirstFind, isSecondFind = firstLexIdx != -1, secondLexIdx != -1

        dest = self.__cTable["dest"]["null"]
        jump = self.__cTable["jump"]["null"]
        comp = ""

        if isFirstFind:
            dest = self.__cTable["dest"][line[:firstLexIdx]]
        if isSecondFind:
            jump = self.__cTable["jump"][line[secondLexIdx+1:]]

        if isFirstFind and isSecondFind:
            comp = self.__cTable["comp"][line[firstLexIdx+1:secondLexIdx]]
        elif not isFirstFind and isSecondFind:
            comp = self.__cTable["comp"][line[:secondLexIdx]]
        elif isFirstFind and not isSecondFind:
            comp = self.__cTable["comp"][line[firstLexIdx+1:]]
        else:
            raise Exception("Compile error!")

        return f"111{comp}{dest}{jump}"

    def __handleCInstruction(self, line: str) -> str:
        return self.__parse(line.strip())

    def __compile(self, asmFile: TextIO, binFile: TextIO) -> None:
        lineNumber = 0
        varAddr = [self.__START_VAR_ADDR]

        for line in asmFile:
            if (self.__skipLine(line)
                or self.__isStartsWith(line, self.__LABEL)
            ):
                continue
            elif self.__isStartsWith(line, self.__A):
                res = self.__handleAInstruction(line, varAddr)
            else:
                res = self.__handleCInstruction(line)

            lineNumber += 1
            print(res, file=binFile)

    def Run(self, inFilePath: str, outFilePath: str = "") -> None:
        if outFilePath == "":
            fileName = os.path.splitext(os.path.basename(inFilePath))[0]
            outFilePath = f"./{fileName}.hack"

        with (
            open(inFilePath, "r") as asmFile,
            open(outFilePath, "w") as binFile
        ):
            self.__preCompile(asmFile)
            asmFile.seek(0)
            self.__compile(asmFile, binFile)

def main():
    if len(sys.argv) != 2:
        print("Usage: python hackAssembler <path to .asm file>")
        sys.exit(1)
    path = sys.argv[1]
    HackAssembler().Run(path)

if __name__ == "__main__":
    main()
