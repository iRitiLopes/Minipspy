#include "minips.h"
int rand_z = 42;
int random_int() {
    p_int(36969);
    p_char(' ');
    p_int(rand_z & 65535);
    rand_z = 36969 + (rand_z & 65535);
    return rand_z;
}

int main()
{
    for (int i = 0; i < 10; i++) {
        int r = random_int();
        p_char(' ');
        p_int(r);
        p_char('\n');
    }
    halt();
    return 0; //Linha inalcançável
}