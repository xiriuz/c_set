#include <stdio.h>

#define A                                                                                          \
    int ab;                                                                                        \
    int bc;                                                                                        \
    int cccc;

#define HELLO            1
#define SHORT_NAME       42
#define LONGER_NAME      0x007f
#define EVEN_LONGER_NAME (2)
#define foo(x)           (x * x)
#define bar(y, z)        (y + z)
void formatted_code;
// clang-format off
        void    unformatted_code;
// clang-format on

typedef struct
{
    int a : 1;
} A;

int main()
{
    int * c;
    int   a     = 0;
    float b[10] = 0;

    if (a >= b[0])
    {
        /* Do Something */
    }
    else
    {
    }

    switch (a)
    {
    case 1:
        break;
    default:
        break;
    }
    printf("Hi\n");
    return 0;
}

void font()
{
    if (a == b)
        if (a >= b)
            a != b a = > b
}