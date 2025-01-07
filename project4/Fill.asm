// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

//State: state=1 -> black else white
@24575
D=A
@SCREEN_END
M=D

(START)
@SCREEN
D=A
@pointer
M=D
@KBD
D=M
@LOOP_BLACK
D;JNE
@LOOP_WHITE
0;JMP

(LOOP_BLACK)
@pointer
A=M
M=-1
@SCREEN_END
D=M
@pointer
M=M+1
D=D-M
@START
D;JLT
@LOOP_BLACK
0;JMP

(LOOP_WHITE)
@pointer
A=M
M=0
@SCREEN_END
D=M
@pointer
M=M+1
D=D-M
@START
D;JLT
@LOOP_WHITE
0;JMP

