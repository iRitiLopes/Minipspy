#include "minips.h"

int main()
{
    int n = read_int();

    // float x = 1;
    // float fator = -1;
    // for (int i = 1; i < n; i++)
    // {
    //     p_str("iteration: ");
    //     p_int(i);
    //     p_char('\n');
    //     float termo = 1.0 / ((2.0 * i) + 1.0);
    //     x += fator * termo;
    //     fator *= -1;
    // }
    // x *= 4;

    // p_str("Pi Float: ");
    // p_float(x);
    // p_char('\n');

    // p_str("------------");
    double y = 1;
    double fator_d = -1;
    for (int i = 1; i < n; i++)
    {
        y =  ((2.0 * i) / 2.0) + 1.5;
        fator_d *= -1;
        p_double(2.0);
        p_str(" * ");
        p_double(i);
        p_str(" / ");
        p_double(2.0);
        p_str(" = ");
        p_double(y);
        p_str("\n");
    }
    p_str("\n");
    halt();
    return 0; //Linha inalcançável
}