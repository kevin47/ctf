#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>

int main(){
	setvbuf(stdout, 0, 2, 0);
	int a;
	puts("len:");
	scanf("%d", &a);
	char *p = malloc(a);
	puts("content:");
	read(0, p, a);
	puts("done");
}
