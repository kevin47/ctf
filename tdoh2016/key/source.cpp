#include <stdint.h>
#include <stdio.h>
#include <iostream>

int main(void)
{

        int8_t buff[256] = "";
	int32_t db[] = {0x484f4454,0x5f2a2f7b,0x4854304E,0x5f474e49,0x464e3043,0x53455355,0x2121555f,0x7d2f2a5f};
	int32_t *dif = db, *arr = (int32_t*)buff, value = 0;        
        scanf("%255s", buff);
	while (*arr && *dif)
		value += (*arr++ ^ *dif++) ;
        puts(value ? "It's not right key." : "You got it!");
        return 0;
}

