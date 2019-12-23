It is a system program which translates the source code to object code in a single pass.It reads the source file only once. The whole process of scanning, parsing, and object code conversion is done in single pass, the assembler handles both label definitions and assembly.

One-pass assemblers are used when

•	It is necessary or desirable to avoid a second pass over the source program.

•	External working storage devices are not available or too slow(to store the immediate file bthis etween two passes).

This assembler takes SIC source code and operand table as input and it generates the object program at the end of the pass by dumping all the object codes to an output file. The symbol table is also generated in a file.
