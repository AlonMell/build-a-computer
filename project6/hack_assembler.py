import cProfile
import os
import pstats
from typing import TextIO

from tables import C_TABLE, SYMBOLS


class HackAssembler:
    _MACHINE_WORD = 16
    _START_VAR_ADDR = 16

    _A = "@"
    _LABEL = "("
    _COMMENT = "//"

    _PREDEFINED_SYMBOLS: dict[str, int] = SYMBOLS
    _C_TABLE: dict[str, dict[str, str]] = C_TABLE

    def __init__(self) -> None:
        self._symbol_table: dict[str, int] = HackAssembler._PREDEFINED_SYMBOLS.copy()

    def _is_starts_with(self, line: str, symb: str) -> bool:
        return line.strip().startswith(symb)

    def _skip_line(self, line: str) -> bool:
        cleaned_line = line.strip()

        return not cleaned_line or cleaned_line.startswith(HackAssembler._COMMENT)

    def _clean_line(self, line: str) -> str:
        return line.split(HackAssembler._COMMENT, 1)[0].strip()

    def _handle_label(self, line: str, line_number: int) -> None:
        label = line[1:-1]
        if label not in self._symbol_table:
            self._symbol_table[label] = line_number

    def _preprocess(self, asm_file: TextIO) -> list[str]:
        line_number = 0
        inter_code = []

        for line in asm_file:
            if self._is_starts_with(line, HackAssembler._LABEL):
                self._handle_label(self._clean_line(line), line_number)
            elif not self._skip_line(line):
                inter_code.append(self._clean_line(line))
                line_number += 1

        return inter_code

    def _handle_a_instruction(self, line: str, var_addr: list[int]) -> str:
        a_instr = line[1:]

        if a_instr.isdigit():
            return f"{int(a_instr):0{HackAssembler._MACHINE_WORD}b}"
        elif a_instr not in self._symbol_table:
            self._symbol_table[a_instr] = var_addr[0]
            var_addr[0] += 1

        return f"{self._symbol_table[a_instr]:0{HackAssembler._MACHINE_WORD}b}"

    def _parse(self, line: str) -> str:
        dest_idx, jump_idx = line.find("="), line.find(";")
        is_dest_find, is_jump_find = dest_idx != -1, jump_idx != -1

        dest = HackAssembler._C_TABLE["dest"]["null"]
        jump = HackAssembler._C_TABLE["jump"]["null"]
        comp = ""

        if not is_dest_find and not is_jump_find:
            raise Exception("Compile error!")

        if is_dest_find:
            dest = HackAssembler._C_TABLE["dest"][line[:dest_idx]]
        if is_jump_find:
            jump = HackAssembler._C_TABLE["jump"][line[jump_idx + 1 :]]

        if is_dest_find and is_jump_find:
            comp = HackAssembler._C_TABLE["comp"][line[dest_idx + 1 : jump_idx]]
        elif not is_dest_find and is_jump_find:
            comp = HackAssembler._C_TABLE["comp"][line[:jump_idx]]
        else:
            comp = HackAssembler._C_TABLE["comp"][line[dest_idx + 1 :]]

        return f"111{comp}{dest}{jump}"

    def _handle_c_instruction(self, line: str) -> str:
        return self._parse(line)

    def _compile(self, inter_code: list[str], bin_file: TextIO) -> None:
        var_addr = [HackAssembler._START_VAR_ADDR]

        for instr in inter_code:
            res = ""

            if self._is_starts_with(instr, HackAssembler._A):
                res = self._handle_a_instruction(instr, var_addr)
            else:
                res = self._handle_c_instruction(instr)

            print(res, file=bin_file)

    def compile(self, in_file_path: str, out_file_path: str = "") -> None:
        if out_file_path == "":
            file_name = os.path.basename(in_file_path)
            file_base_name, _ = os.path.splitext(file_name)
            out_file_path = f"./{file_base_name}.hack"

        inter_code = []
        with open(in_file_path) as asm_file:
            inter_code = self._preprocess(asm_file)
        with open(out_file_path, "w") as bin_file:
            self._compile(inter_code, bin_file)


def parse_arguments():
    import argparse

    parser = argparse.ArgumentParser(description="Hack Assembler for .asm files")
    parser.add_argument("inFile", type=str, help="Path to the input .asm file")
    parser.add_argument(
        "-o",
        "--outFile",
        type=str,
        help="Path to the output .hack file",
        default="",
    )
    parser.add_argument(
        "-p", "--profiling", action="store_true", help="Enable profiling"
    )

    return parser.parse_args()


def run_profiler(args):
    with cProfile.Profile() as profile:
        HackAssembler().compile(args.inFile, args.outFile)

    results = pstats.Stats(profile)
    results.dump_stats("results.prof")


def main():
    args = parse_arguments()

    if args.profiling:
        run_profiler(args)
        return

    HackAssembler().compile(args.inFile, args.outFile)


if __name__ == "__main__":
    main()
