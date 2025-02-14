import os
from pathlib import Path

import pytest
from hack_assembler import HackAssembler

PROJECT_DIR = Path(__file__).resolve().parent

input_dir = PROJECT_DIR / "in_asm"
output_dir = PROJECT_DIR / "out_hack"
test_dir = PROJECT_DIR / "tests_hack"


@pytest.mark.parametrize(
    "filename", [f for f in os.listdir(input_dir) if f.endswith(".asm")]
)
def test_assembler(filename: str) -> None:
    base_name = Path(filename).stem

    input_path = input_dir / f"{base_name}.asm"
    output_path = output_dir / f"{base_name}.hack"
    expected_path = test_dir / f"{base_name}.hack"

    HackAssembler().compile(input_path, output_path)

    with open(output_path) as f1, open(expected_path) as f2:
        assert f1.read() == f2.read(), f"Files for {base_name} are not equal!"
