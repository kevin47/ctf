#include <stdio.h>
#include <stdlib.h>

char flag[50] = "FLAG{Y0u_c4nt_s33_me}";

int main(){
	int n;
	char *p[1000];
	puts("Hello, give me a number:");
	scanf("%d", &n);
	for (int i = 0; i < n; ++i)
		p[i] = malloc(100);
	for (int i = 0; i < n; ++i)
		free(p[i]);
}
