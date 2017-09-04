#include <stdio.h>

int main(){
	char a = 'a';
	int n = 1;
	printf("\n%d\n", n);
	printf("%256c%hhn", a, &n);
	printf("\n%d\n", n);
}
