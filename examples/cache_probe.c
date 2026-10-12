#include "minips.h"

volatile int values[1024];

int main(void) {
    int sum = 0;
    for (int i = 0; i < 1024; ++i)
        values[i] = i;
    for (int i = 0; i < 1024; ++i)
        sum += values[i];
    p_int(sum);
    p_char('\n');
    return 0;
}
