#include <stdio.h>
#include <unistd.h>

void b(){
	char buf[88];
	fgets(buf, sizeof(buf), stdin);
	printf(buf);
	_exit(0);
}

void a(){
	b();
}

int main(){
	setvbuf(stdout, 0, _IONBF, 0);
	a();
	return 0;
}
