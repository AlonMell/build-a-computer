// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
// The algorithm is based on repetitive addition.


@R2
M=0

@R0 //Some comment
D=M
@val
M=D //Some comment

@R1
D=M
@i
M=D

@LOOP
D;JGE

@i //Some comment
M=-M
@val
M=-M

(LOOP) //Some comment
@i
M=M-1
D=M
@END
D;JLT

@val
D=M
@R2
M=D+M //Some comment

@LOOP
0;JMP

(END)
@END
0;JMP
