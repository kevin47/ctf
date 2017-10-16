#include <stdio.h>
#include <unistd.h>
#include <string.h>

char buf[1000000];

void jizz(){
	write(1, "a", 1);
}

int main(){
	char local[10];
	int len = read(0, buf, sizeof(buf));
	memcpy(local, buf, len);
	return 0;
}
