#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <stdio.h>
#include <unistd.h>

int main(){
	int fd = open("/home/pwn3/flag", 0, 0);
	printf("%d\n", fd);
	char buff[100];
	read(0, buff, 87);
	((void(*)())buff)();
}
