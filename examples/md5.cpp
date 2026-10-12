// Streaming MD5, following RFC 1321: https://www.rfc-editor.org/rfc/rfc1321
// Build yourself: make build SOURCE=examples/md5.cpp
// Enter hashes the UTF-8 input bytes before the newline; spaces are preserved.
#include "minips.h"

typedef unsigned int U32;
static_assert(sizeof(U32) == 4, "MD5 requires 32-bit words");

static int read_character() {
#ifdef __mips__
    int value;
    asm volatile("li $v0, 12; syscall; move %0, $v0;"
                 : "=r" (value) : : "$v0");
    return value;
#else
    return getchar();
#endif
}

// Constant rotations and word buffers avoid variable shifts and byte stores.
#define F(b, c, d) ((d) ^ ((b) & ((c) ^ (d))))
#define G(b, c, d) ((c) ^ ((d) & ((b) ^ (c))))
#define H(b, c, d) ((b) ^ (c) ^ (d))
#define I(b, c, d) ((c) ^ ((b) | ~(d)))
#define STEP(fn, a, b, c, d, k, s, t) do { \
    U32 value = (a) + fn(b, c, d) + block[k] + (t); \
    (a) = (b) + ((value << (s)) | (value >> (32 - (s)))); \
} while (0)

class Md5 {
    U32 state[4];
    U32 block[16];
    U32 bit_count_low;
    U32 bit_count_high;
    int used;

    void clear_block() {
        for (int i = 0; i < 16; ++i)
            block[i] = 0;
        used = 0;
    }

    void transform() {
        U32 a = state[0], b = state[1], c = state[2], d = state[3];
        STEP(F, a, b, c, d, 0, 7, 0xd76aa478u);
        STEP(F, d, a, b, c, 1, 12, 0xe8c7b756u);
        STEP(F, c, d, a, b, 2, 17, 0x242070dbu);
        STEP(F, b, c, d, a, 3, 22, 0xc1bdceeeu);
        STEP(F, a, b, c, d, 4, 7, 0xf57c0fafu);
        STEP(F, d, a, b, c, 5, 12, 0x4787c62au);
        STEP(F, c, d, a, b, 6, 17, 0xa8304613u);
        STEP(F, b, c, d, a, 7, 22, 0xfd469501u);
        STEP(F, a, b, c, d, 8, 7, 0x698098d8u);
        STEP(F, d, a, b, c, 9, 12, 0x8b44f7afu);
        STEP(F, c, d, a, b, 10, 17, 0xffff5bb1u);
        STEP(F, b, c, d, a, 11, 22, 0x895cd7beu);
        STEP(F, a, b, c, d, 12, 7, 0x6b901122u);
        STEP(F, d, a, b, c, 13, 12, 0xfd987193u);
        STEP(F, c, d, a, b, 14, 17, 0xa679438eu);
        STEP(F, b, c, d, a, 15, 22, 0x49b40821u);
        STEP(G, a, b, c, d, 1, 5, 0xf61e2562u);
        STEP(G, d, a, b, c, 6, 9, 0xc040b340u);
        STEP(G, c, d, a, b, 11, 14, 0x265e5a51u);
        STEP(G, b, c, d, a, 0, 20, 0xe9b6c7aau);
        STEP(G, a, b, c, d, 5, 5, 0xd62f105du);
        STEP(G, d, a, b, c, 10, 9, 0x02441453u);
        STEP(G, c, d, a, b, 15, 14, 0xd8a1e681u);
        STEP(G, b, c, d, a, 4, 20, 0xe7d3fbc8u);
        STEP(G, a, b, c, d, 9, 5, 0x21e1cde6u);
        STEP(G, d, a, b, c, 14, 9, 0xc33707d6u);
        STEP(G, c, d, a, b, 3, 14, 0xf4d50d87u);
        STEP(G, b, c, d, a, 8, 20, 0x455a14edu);
        STEP(G, a, b, c, d, 13, 5, 0xa9e3e905u);
        STEP(G, d, a, b, c, 2, 9, 0xfcefa3f8u);
        STEP(G, c, d, a, b, 7, 14, 0x676f02d9u);
        STEP(G, b, c, d, a, 12, 20, 0x8d2a4c8au);
        STEP(H, a, b, c, d, 5, 4, 0xfffa3942u);
        STEP(H, d, a, b, c, 8, 11, 0x8771f681u);
        STEP(H, c, d, a, b, 11, 16, 0x6d9d6122u);
        STEP(H, b, c, d, a, 14, 23, 0xfde5380cu);
        STEP(H, a, b, c, d, 1, 4, 0xa4beea44u);
        STEP(H, d, a, b, c, 4, 11, 0x4bdecfa9u);
        STEP(H, c, d, a, b, 7, 16, 0xf6bb4b60u);
        STEP(H, b, c, d, a, 10, 23, 0xbebfbc70u);
        STEP(H, a, b, c, d, 13, 4, 0x289b7ec6u);
        STEP(H, d, a, b, c, 0, 11, 0xeaa127fau);
        STEP(H, c, d, a, b, 3, 16, 0xd4ef3085u);
        STEP(H, b, c, d, a, 6, 23, 0x04881d05u);
        STEP(H, a, b, c, d, 9, 4, 0xd9d4d039u);
        STEP(H, d, a, b, c, 12, 11, 0xe6db99e5u);
        STEP(H, c, d, a, b, 15, 16, 0x1fa27cf8u);
        STEP(H, b, c, d, a, 2, 23, 0xc4ac5665u);
        STEP(I, a, b, c, d, 0, 6, 0xf4292244u);
        STEP(I, d, a, b, c, 7, 10, 0x432aff97u);
        STEP(I, c, d, a, b, 14, 15, 0xab9423a7u);
        STEP(I, b, c, d, a, 5, 21, 0xfc93a039u);
        STEP(I, a, b, c, d, 12, 6, 0x655b59c3u);
        STEP(I, d, a, b, c, 3, 10, 0x8f0ccc92u);
        STEP(I, c, d, a, b, 10, 15, 0xffeff47du);
        STEP(I, b, c, d, a, 1, 21, 0x85845dd1u);
        STEP(I, a, b, c, d, 8, 6, 0x6fa87e4fu);
        STEP(I, d, a, b, c, 15, 10, 0xfe2ce6e0u);
        STEP(I, c, d, a, b, 6, 15, 0xa3014314u);
        STEP(I, b, c, d, a, 13, 21, 0x4e0811a1u);
        STEP(I, a, b, c, d, 4, 6, 0xf7537e82u);
        STEP(I, d, a, b, c, 11, 10, 0xbd3af235u);
        STEP(I, c, d, a, b, 2, 15, 0x2ad7d2bbu);
        STEP(I, b, c, d, a, 9, 21, 0xeb86d391u);
        state[0] += a;
        state[1] += b;
        state[2] += c;
        state[3] += d;
    }

    void push_byte(U32 byte) {
        byte &= 255u;
        int index = used >> 2;
        int offset = used & 3;
        if (offset == 0)
            block[index] |= byte;
        else if (offset == 1)
            block[index] |= byte << 8;
        else if (offset == 2)
            block[index] |= byte << 16;
        else
            block[index] |= byte << 24;
        ++used;
        if (used == 64) {
            transform();
            clear_block();
        }
    }

    static void print_nibble(int nibble) {
        if (nibble < 10)
            p_char('0' + nibble);
        else
            p_char('a' + nibble - 10);
    }

public:
    Md5() : bit_count_low(0), bit_count_high(0), used(0) {
        state[0] = 0x67452301u;
        state[1] = 0xefcdab89u;
        state[2] = 0x98badcfeu;
        state[3] = 0x10325476u;
        clear_block();
    }

    void append(U32 byte) {
        bit_count_low += 8u;
        if (bit_count_low == 0)
            ++bit_count_high;
        push_byte(byte);
    }

    void finish_and_print() {
        push_byte(0x80u);
        while (used != 56)
            push_byte(0);
        block[14] = bit_count_low;
        block[15] = bit_count_high;
        transform();
        for (int i = 0; i < 4; ++i) {
            U32 word = state[i];
            for (int byte = 0; byte < 4; ++byte) {
                print_nibble(static_cast<int>((word >> 4) & 15u));
                print_nibble(static_cast<int>(word & 15u));
                word >>= 8;
            }
        }
        p_char('\n');
    }
};

int main() {
    Md5 md5;
    int character;
    while ((character = read_character()) != '\n' && character != -1)
        md5.append(static_cast<U32>(character));
    md5.finish_and_print();
    return 0;
}

#undef STEP
#undef F
#undef G
#undef H
#undef I
