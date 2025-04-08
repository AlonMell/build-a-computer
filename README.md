# Nand2Tetris Project Implementation

This repository contains a comprehensive implementation of projects from the [Nand2Tetris](https://www.nand2tetris.org/) course, based on the book "The Elements of Computing Systems" by Noam Nisan and Shimon Schocken. The course guides students through building a modern computer system from first principles - starting with basic logic gates (NAND) and eventually creating a full hardware platform and software hierarchy.

## Repository Structure

The repository is organized into separate projects, each representing a different layer in the computer architecture:

```
nand2tetris/
├── project1/  # Boolean Logic
├── project2/  # Boolean Arithmetic
├── project3/  # Sequential Logic
├── project4/  # Machine Language
├── project5/  # Computer Architecture
└── project6/  # Assembler
```

## Project Descriptions

### Project 1: Boolean Logic
Implementation of elementary logic gates using NAND gates as the primitive building block:

* **And.hdl** - AND gate implementation using NAND
* **And16.hdl** - 16-bit AND gate
* **DMux.hdl** - Demultiplexor
* **DMux4Way.hdl** - 4-way demultiplexor
* **DMux8Way.hdl** - 8-way demultiplexor
* **Mux.hdl** - Multiplexor
* **Mux16.hdl** - 16-bit multiplexor
* **Mux4Way16.hdl** - 4-way 16-bit multiplexor
* **Mux8Way16.hdl** - 8-way 16-bit multiplexor
* **Not.hdl** - NOT gate implementation using NAND
* **Not16.hdl** - 16-bit NOT gate
* **Or.hdl** - OR gate implementation using NAND
* **Or16.hdl** - 16-bit OR gate
* **Or8Way.hdl** - 8-way OR gate
* **Xor.hdl** - XOR gate implementation

### Project 2: Boolean Arithmetic
Implementation of arithmetic logic units (ALU) and arithmetic operations:

* **ALU.hdl** - The Arithmetic Logic Unit
* **Add16.hdl** - 16-bit adder
* **FullAdder.hdl** - Full adder (adds 3 bits)
* **HalfAdder.hdl** - Half adder (adds 2 bits)
* **Inc16.hdl** - 16-bit incrementer

### Project 3: Sequential Logic
Implementation of memory components using D flip-flops:

* **Bit.hdl** - 1-bit register
* **PC.hdl** - Program Counter
* **RAM16K.hdl** - 16K RAM
* **RAM4K.hdl** - 4K RAM
* **RAM512.hdl** - 512 RAM
* **RAM64.hdl** - 64 RAM
* **RAM8.hdl** - 8 RAM
* **Register.hdl** - 16-bit register

### Project 4: Machine Language
Assembly language programs written for the Hack platform:

* **Fill.asm** - Program that fills the screen when a key is pressed
* **Mult.asm** - Program that multiplies two numbers
* **Mult_for.asm** - Alternative implementation of multiplication

### Project 5: Computer Architecture
Implementation of the Hack computer CPU and memory system:

* **CPU.hdl** - Central Processing Unit
* **Computer.hdl** - The Hack computer
* **Memory.hdl** - Memory system including RAM and memory-mapped I/O

### Project 6: Assembler
A Python implementation of an assembler for the Hack platform that translates assembly language to binary machine code:

* **hack_assembler.py** - Main assembler implementation
* **tables.py** - Lookup tables for instruction translation
* **test_hack_assembler.py** - Test suite for the assembler
* **requirements.txt** - Python dependencies

## Hack Computer Architecture

The Hack computer is a 16-bit von Neumann platform with:
- A 16-bit instruction set
- Separate instruction memory (ROM) and data memory (RAM)
- Memory-mapped I/O for screen and keyboard
- Two types of instructions:
  - A-instruction: `@value` (loads a value into the A register)
  - C-instruction: `dest=comp;jump` (computation followed by optional storage and jump)

## Assembler Usage

The assembler in project6 translates Hack assembly language (.asm files) into binary machine code (.hack files):

```bash
cd project6
pip install -r requirements.txt
python hack_assembler.py input_file.asm [-o output_file.hack] [-p]
```

### Options:
- `-o, --outFile`: Specify the output file path
- `-p, --profiling`: Enable profiling (outputs performance metrics to `results.prof`)

### Testing:
```bash
cd project6
pytest
```

## Implementation Details

### Hardware Description Language (HDL)
The hardware components in projects 1-5 are implemented using a custom Hardware Description Language. Each .hdl file specifies:

1. The chip interface (inputs and outputs)
2. The internal implementation using other, previously built chips

### Hack Assembly Language
The assembly language has several key features:
- Symbol support (variables and labels)
- Two instruction types (A and C)
- Built-in symbols for registers (R0-R15), screen, keyboard, etc.
- Comment support using `//`

## Resources

- [Nand2Tetris Official Website](https://www.nand2tetris.org/)
- [The Elements of Computing Systems Book](https://mitpress.mit.edu/books/elements-computing-systems)
- [Nand2Tetris Software Suite](https://www.nand2tetris.org/software)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.