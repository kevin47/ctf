#include <stdio.h>
#include <math.h>

float round_3(float f){
	return floor(f*1000+0.5)/1000;
}

int main(){
	//unsigned char str[1024] = "\x3f\x9d\x70\xa4hri\x01\x01\x81\x34$\x01\x01\x01\x01\x31\xd2Rj\x08ZH\x01\xe2RH\x89\xe2jhH\xb8/bin///sPj;XH\x89\xe7H\x89\xd6\x99\x0f\x05";
	unsigned char str[1024] = "";
	while(~scanf("%s", str)){
		/*for (int i = 0; str[i]; i += 4){
			unsigned int sum = 0; 
			for (int j = 0; j < 4; ++j){
				sum <<= 8;
				sum += (unsigned int)str[i+j];
			}
			float f = *((float *)&sum);
			printf("%02x%02x%02x%02x is %u in dec, %f in float, and f is %x in hex\n", str[i], str[i+1], str[i+2], str[i+3], sum, f, f);
		}*/
		unsigned int num;
		sscanf(str, "%x", &num);
		float f = *((float *)&num);
		float f2= round_3(f);
		printf("%u in dec, %f in float. %f -> %x\n", num, f, f2, *((int *)&f2));
		//scanf("%f", &f);
		//printf("%f -> %x\n", f, *((int *)&f));
	}
	puts("");

	//float f = 0.000;
	//while (f <= 3){
	//	printf("%f -> %x\n", f, *((int *)&f));
	//	f += 0.001;
	//}
}
