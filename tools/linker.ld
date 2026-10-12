ENTRY(__start)
SECTIONS
{
    .text 0x00400000 : { KEEP(*(.text.start)) *(.text .text.*) . = ALIGN(4); }
    .rodata 0x00800000 : { *(.rodata .rodata.*) . = ALIGN(4); }
    .data 0x10010000 : {
        *(.data .data.* .sdata .sdata.*)
        *(.bss .bss.* .sbss .sbss.*) *(COMMON)
        /* Force a loadable section, including zero-filled globals. */
        BYTE(0)
        . = ALIGN(4);
    }
    /DISCARD/ : { *(.MIPS.abiflags .reginfo .pdr .comment .note* .eh_frame*) }
}
