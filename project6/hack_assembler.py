import argparse
import os
from typing import TextIO

class HackAssembler:
    def __init__(self):
        self.__MACHINE_WORD = 16
        self.__START_VAR_ADDR = 16

        self.__A = "@"
        self.__LABEL = "("
        self.__COMMENT = "//"

        self.__COMP = {
            "0":   "0101010",
            "1":   "0111111",
            "-1":  "0111010",
            "D":   "0001100",
            "A":   "0110000", "M":   "1110000",
            "!D":  "0001101",
            "!A":  "0110001", "!M":  "1110001",
            "-D":  "0001111",
            "-A":  "0110011", "-M":  "1110011",
            "D+1": "0011111",
            "A+1": "0110111", "M+1": "1110111",
            "D-1": "0001110",
            "A-1": "0110010", "M-1": "1110010",
            "D+A": "0000010", "D+M": "1000010",
            "D-A": "0010011", "D-M": "1010011",
            "A-D": "0000111", "M-D": "1000111",
            "D&A": "0000000", "D&M": "1000000",
            "D|A": "0010101", "D|M": "1010101"
        }

        self.__DEST = {
            "null": "000",
            "M":    "001", "D":  "010", "DM": "011",
            "A":    "100", "AM": "101", "AD": "110",
            "ADM":  "111"
        }

        self.__JUMP = {
            "null": "000",
            "JGT":  "001", "JEQ": "010", "JGE": "011",
            "JLT":  "100", "JNE": "101", "JLE": "110",
            "JMP":  "111"
        }

        self.__C_TABLE = {
            "dest": self.__DEST,
            "comp": self.__COMP,
            "jump": self.__JUMP,
        }

        self.__symbol_table = {
            "R0":  0,  "R1":   1,  "R2":  2,  "R3":  3,
            "R4":  4,  "R5":   5,  "R6":  6,  "R7":  7,
            "R8":  8,  "R9":   9,  "R10": 10, "R11": 11,
            "R12": 12, "R13":  13, "R14": 14, "R15": 15,
            "SCREEN": 16384, "KBD": 24576,
            "SP":  0,  "LCL":  1,  "ARG": 2,
            "THIS": 3, "THAT": 4
        }

    def __is_starts_with(self, line: str, symb: str) -> bool:
        return line.strip().startswith(symb)

    def __skip_line(self, line: str) -> bool:
        return (
            not line.strip()
            or self.__is_starts_with(line, self.__COMMENT)
        )

    def __clean_line(self, line: str) -> str:
        return line.split(self.__COMMENT, 1)[0].strip()

    def __handle_label(self, line: str, line_number: int) -> None:
        label = line[1:-1]
        if label not in self.__symbol_table:
            self.__symbol_table[label] = line_number

    def __preprocess(self, asm_file: TextIO) -> list[str]:
        line_number = 0
        inter_code = []

        for line in asm_file:
            if self.__is_starts_with(line, self.__LABEL):
                self.__handle_label(
                    self.__clean_line(line),
                    line_number
                )
            elif not self.__skip_line(line):
                inter_code.append(self.__clean_line(line))
                line_number += 1

        return inter_code

    def __handle_A_instruction(
        self,
        line: str,
        var_addr: list[int]
    ) -> str:
        a_instr = line[1:]

        if a_instr.isdigit():
            return bin(
                int(a_instr)
            )[2:].zfill(self.__MACHINE_WORD)
        elif a_instr not in self.__symbol_table:
            self.__symbol_table[a_instr] = var_addr[0]
            var_addr[0] += 1

        return bin(
            self.__symbol_table[a_instr]
        )[2:].zfill(self.__MACHINE_WORD)

    def __parse(self, line: str) -> str:
        dest_idx, jump_idx = line.find("="), line.find(";")
        is_dest_find, is_jump_find = dest_idx != -1, jump_idx != -1

        dest = self.__C_TABLE["dest"]["null"]
        jump = self.__C_TABLE["jump"]["null"]
        comp = ""

        if not is_dest_find and not is_jump_find:
            raise Exception("Compile error!")

        if is_dest_find:
            dest = self.__C_TABLE["dest"][line[:dest_idx]]
        if is_jump_find:
            jump = self.__C_TABLE["jump"][line[jump_idx+1:]]

        if is_dest_find and is_jump_find:
            comp = self.__C_TABLE["comp"][line[dest_idx+1:jump_idx]]
        elif not is_dest_find and is_jump_find:
            comp = self.__C_TABLE["comp"][line[:jump_idx]]
        else:
            comp = self.__C_TABLE["comp"][line[dest_idx+1:]]

        return f"111{comp}{dest}{jump}"

    def __handle_C_instruction(self, line: str) -> str:
        return self.__parse(line)

    def __compile(
        self,
        inter_code: list[str],
        bin_file: TextIO
    ) -> None:
        var_addr = [self.__START_VAR_ADDR]

        for instr in inter_code:
            res = ""

            if self.__is_starts_with(instr, self.__A):
                res = self.__handle_A_instruction(instr, var_addr)
            else:
                res = self.__handle_C_instruction(instr)

            print(res, file=bin_file)

    def Compile(
        self,
        in_file_path: str,
        out_file_path: str = ""
    ) -> None:
        if out_file_path == "":
            file_name = os.path.basename(in_file_path)
            file_base_name, _ = os.path.splitext(file_name)
            out_file_path = f"./{file_base_name}.hack"

        inter_code = []
        with open(in_file_path, "r") as asm_file:
            inter_code = self.__preprocess(asm_file)
        with open(out_file_path, "w") as bin_file:
            self.__compile(inter_code, bin_file)

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Hack Assembler for .asm files"
    )
    parser.add_argument(
        "inFile",
        type=str,
        help="Path to the input .asm file"
    )
    parser.add_argument(
        "-o",
        "--outFile",
        type=str,
        help="Path to the output .hack file",
        default=""
    )

    return parser.parse_args()

def main():
    args = parse_arguments()
    HackAssembler().Compile(args.inFile, args.outFile)

if __name__ == "__main__":
    main()
