#include "algo.h"

void free_desk(unsigned char **desk) {
	unsigned char **to_delete = desk;
	while (*desk) {
		free(*desk);
		++desk;
	}
	free(to_delete);
}

void print_desk(struct game_env* env) {
	for (ssize_t i = 0; i < env->size; ++i) {
		for (ssize_t j = 0; j < env->size; ++j) {
			printf("%d ", env->desk[i][j]);
		}
		printf("\n");
	}
	printf("\n");
}
