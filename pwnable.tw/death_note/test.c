#include <stdio.h>
#include <stdlib.h>

int main(){
	char s[20] = "-2147483649";
	int a = atoi(s);
	printf("%d\n", a);
}
