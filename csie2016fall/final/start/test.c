#include <unistd.h>

int main(){
	char buf[128];
	for (int i = 0; i < 3; ++i){
		read(0, buf, 64);
		write(1, buf, 64);
	}
}
