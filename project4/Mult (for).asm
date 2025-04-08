// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
// The algorithm is based on repetitive addition.

@i
M=0
@R2
M=0
@R0
D=M
@val
M=D
@R1
D=M
@n
M=D

@LOOP
D;JGE

@n
M=-M
@val
M=-M

(LOOP)
@i
D=M
@n
D=D-M
@END
D;JGE

@val
D=M
@R2
M=D+M

@i
M=M+1
@LOOP
0;JMP

(END)
@END
0;JMP

