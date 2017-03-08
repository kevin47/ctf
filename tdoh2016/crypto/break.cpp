#include <cstdio>

int main(){
	char cipher[] = "LWIC{ZYDSBT_MX_WZXEO_BT_OFM}";
	for (int i = 0; i < 26; ++i){
		for (int j = 0; cipher[j]; ++j){
			if ('A' <= cipher[j] && cipher[j] <= 'Z')
				printf("%c", (cipher[j]-'A'+i-j+26)%26+'A');
			else printf("%c", cipher[j]);
		}
		puts("");
	}
}
