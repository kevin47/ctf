#include <stdio.h>
#include <sys/mman.h>

int main(){
	printf("%d\n", PROT_NONE);
	printf("%d\n", PROT_READ);
	printf("%d\n", PROT_WRITE);
	printf("%d\n", PROT_EXEC);
}
