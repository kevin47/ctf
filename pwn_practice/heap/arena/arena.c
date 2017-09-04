#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void sh(char *c){
	system(c);
}

char cmd[1024];

int main(){
	char *ptr[8];
	char magic[32];
	int size, n;

	setvbuf(stdout, 0, _IONBF, 0);
	memset(ptr, 0, sizeof(ptr));

	gets(magic);

	while(1){
		fgets(cmd, 1024, stdin);
		printf("got: %s\n", cmd);
		if (!strncmp(cmd, "add", 3)){
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
		} else if (!strncmp(cmd, "print", 5)){
			printf("Index: ");
			scanf("%d", &n);
			if (n >= 0 && n < 8 && ptr[n]){
				printf("Size: ");
				scanf("%d%*c", &size);
				write(1, ptr[n], size);
			} else{
				puts("nothing here");
			}
		} else if (!strncmp(cmd, "exit", 4)){
			break;	
		} else{
			puts("unknown command");
		}
	}
	
	return 0;
}
