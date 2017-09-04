#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

struct A{
	char buf[128];
	char *ptr[10];
	char *cmd;
	int size;
};

struct A a;

void sh(char *c){
	system(c);
}

int main(){
	setvbuf(stdout, 0, _IONBF, 0);
	memset(a.ptr, 0, sizeof(a.ptr));
	a.cmd = a.buf;
	int n = 0;

	while(1){
		fgets(a.cmd, sizeof(a.buf), stdin);
		printf("got: %s\n", a.cmd);
		if (!strncmp(a.cmd, "push", 4)){
			if (n < 8){
				scanf("%d%*c", &a.size);
				a.ptr[n] = malloc(a.size);
				fgets(a.ptr[n], a.size, stdin);
				n++;
			} else{
				puts("stack is full");
			}
		} else if (!strncmp(a.cmd, "pop", 3)){
			if (n >= 0){
				n--;
				puts(a.ptr[n]);
				free(a.ptr[n]);
				a.ptr[n] = 0;
			} else{
				puts("stack is empty");
			}
		} else{
			puts("unknown command");
		}
	}
	
	return 0;
}
