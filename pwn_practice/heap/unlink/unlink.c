#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

struct A{
	char *buf[3];
	char *cmd;
};
struct A a;

void sh(char *c){
	system(c);
}

int main(){
	char *ptr[8];
	int size, n;

	setvbuf(stdout, 0, _IONBF, 0);
	memset(ptr, 0, sizeof(ptr));
	a.cmd = malloc(128);

	while(1){
		fgets(a.cmd, 128, stdin);
		printf("got: %s\n", a.cmd);
		if (!strncmp(a.cmd, "add", 3)){
			printf("Index: ");
			scanf("%d", &n);
			printf("%d\n", n);
			if (n >= 0 && n < 8){
				printf("Size: ");
				scanf("%d%*c", &size);
				printf("%d\n", size);
				ptr[n] = malloc(size);

				printf("Data: ");
				gets(ptr[n]);
			} else{
				puts("out of bound");
			}
		} else if (!strncmp(a.cmd, "remove", 6)){
			printf("Index: ");
			scanf("%d", &n);
			if (n >= 0 && n < 8 && ptr[n]){
				puts(ptr[n]);
				free(ptr[n]);
				ptr[n] = 0;
			} else{
				puts("nothing here");
			}
		} else{
			puts("unknown command");
		}
	}
	
	return 0;
}
