import os

import pytest
from hack_assembler import HackAssembler

input_dir = "./in_asm"
output_dir = "./out_hack"
test_dir = "./tests_hack"


@pytest.mark.parametrize(
    "filename", [f for f in os.listdir(input_dir) if f.endswith(".asm")]
)
def test_assembler(filename: str):
    file_base_name, _ = os.path.splitext(filename)

    in_file_path = f"{input_dir}/{file_base_name}.asm"
    out_file_path = f"{output_dir}/{file_base_name}.hack"
    tests_file_path = f"{test_dir}/{file_base_name}.hack"

    HackAssembler().compile(in_file_path, out_file_path)

    with open(out_file_path) as f1, open(tests_file_path) as f2:
        assert f1.read() == f2.read(), f"Files for {file_base_name} are not equal!"
