import sys
import os
from typing import TextIO

#TODO List:
    #Wrap it into a class
    #Probably put tables in separate file
    #Refactor parse
    #Enhancement preCompile
    #Handle comments in the instrucation, probably do intermediate view with "clean" string
    #In-depth Exceptions
    #Probably use argparse
    #Short comments near hard logic
    #Tests

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

        #Constants
        self.__A = "@"
        self.__LABEL = "("
        self.__COMMENT = "//"

    def __skipLine(self, line: str) -> bool:
        return not line.strip() or self.__isLineStartsWith(line, self.__COMMENT)

    def __isLineStartsWith(self, line: str, sym: str) -> bool:
        return line.strip().startswith(sym)

    #TODO: Handle comments
    def __preCompile(self, file: TextIO) -> None:
        counter = 0
        for line in file:
            if self.__skipLine(line):
                continue
            elif self.__isLineStartsWith(line, self.__LABEL):
                label = line.strip()[1:-1]
                if label not in self.__symbolTable:
                    self.__symbolTable[label] = counter
                continue
            counter += 1

    def __handleAInstruction(self, line: str, counter: list[int]) -> str:
        aInstr = line.strip()[1:]

        if aInstr.isdigit():
            return bin(int(aInstr))[2:].zfill(16)
        elif aInstr not in self.__symbolTable:
            self.__symbolTable[aInstr] = counter[0]
            counter[0] += 1

        return bin(self.__symbolTable[aInstr])[2:].zfill(16)

    def __parse(self, line: str) -> str:
        firstLexIdx, secondLexIdx = line.find("="), line.find(";")
        dest, comp, jump = "", "", ""

        if firstLexIdx != -1 and secondLexIdx != -1:
            dest = self.__cTable["dest"][line[:firstLexIdx]]
            comp = self.__cTable["comp"][line[firstLexIdx+1:secondLexIdx]]
            jump = self.__cTable["jump"][line[secondLexIdx:]]
        elif firstLexIdx == -1 and secondLexIdx != -1:
            dest = self.__cTable["dest"]["null"]
            comp = self.__cTable["comp"][line[:secondLexIdx]]
            jump = self.__cTable["jump"][line[secondLexIdx+1:]]
        elif firstLexIdx != -1 and secondLexIdx == -1:
            dest = self.__cTable["dest"][line[:firstLexIdx]]
            comp = self.__cTable["comp"][line[firstLexIdx+1:]]
            jump = self.__cTable["jump"]["null"]
        else:
            raise Exception("Compile error!")

        return f"111{comp}{dest}{jump}"

    def __handleCInstruction(self, line: str) -> str:
        return self.__parse(line.strip())

    def __compile(self, inFile: TextIO, outFile: TextIO) -> None:
        counter = 0
        varCounter = [16]

        for line in inFile:
            if self.__skipLine(line) or self.__isLineStartsWith(line, self.__LABEL):
                continue
            elif self.__isLineStartsWith(line, self.__A):
                res = self.__handleAInstruction(line, varCounter)
            else:
                res = self.__handleCInstruction(line)
            counter += 1
            print(res, file=outFile, end="\n")

    def Run(self, inFilePath: str, outFilePath: str = "") -> None:
        if outFilePath == "":
            fileName = os.path.splitext(os.path.basename(inFilePath))[0]
            outFilePath = f"./{fileName}.hack"

        with open(inFilePath, "r") as asmFile, open(outFilePath, "w") as binaryFile:
            self.__preCompile(asmFile)
            asmFile.seek(0)
            self.__compile(asmFile, binaryFile)

def main():
    if len(sys.argv) != 2:
        print("Usage: python hackAssembler <path to .asm file>")
        sys.exit(1)
    path = sys.argv[1]
    HackAssembler().Run(path)

if __name__ == "__main__":
    main()
