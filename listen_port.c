#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>

int main(int argc, char *argv[]){
	if (argc < 2 || 3 < argc){
		fprintf(stderr, "Usage: ./listen [executable] [port (default 7122)]\n");
		exit(0);
	}
	int port;
	if (argc == 3) port = atoi(argv[2]);
	else port = 7122;

	setvbuf(stdin, 0, _IONBF, 0);
	setvbuf(stdout, 0, _IONBF, 0);

	int sockfd = socket(AF_INET, SOCK_STREAM, 0);
	if (sockfd < 0){
		perror("Socket failed: ");
		exit(1);
	}
	
	struct sockaddr_in server, client;
	server.sin_family = AF_INET;
	server.sin_port = htons(port);
	inet_aton("127.0.0.1", &server.sin_addr.s_addr);
	if (bind(sockfd, (struct sockaddr *)&server, sizeof(server)) < 0){
		perror("Bind failed: ");
		exit(1);
	}

	if (listen(sockfd, 3) < 0){
		perror("Listen failed:");
		exit(1);
	}

	client = accept(socket_desc, (struct sockaddr *)&client, (socklen_t*)&c);
}

