#include <unistd.h>
#include <stdio.h>

int main(){
	//execve("/bin/sh", 0, 0);
	char s[1000];
	scanf("%s", s);
	printf("%x %x\n", s[0], s[1]);
}
