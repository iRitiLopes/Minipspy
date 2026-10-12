#include "minips.h"

// Freestanding C++: templates and classes work without a standard library.
template <int N> struct Buffer {
    int values[N];
    int checksum() const {
        int result = 0;
        for (int i = 0; i < N; ++i)
            result += values[i];
        return result;
    }
};

Buffer<256> buffer;

int main() {
    for (int i = 0; i < 256; ++i)
        buffer.values[i] = i;
    p_int(buffer.checksum());
    p_char('\n');
    return 0;
}
