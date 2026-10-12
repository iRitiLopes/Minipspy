.set noreorder
.section .text.start,"ax",@progbits
.globl __start
.ent __start
__start:
    jal main
    nop
    addiu $v0, $zero, 10
    syscall
.end __start
