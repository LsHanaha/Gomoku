#include "algo.h"

void free_frames(fframe* steps_frames, struct game_env* env) {
	for (ssize_t i = 0; i < env->deep + 1; ++i) {
		fframe* to_delete = steps_frames + i;
		free(to_delete->possibly_moves);
		if (to_delete->estimate)
			free(to_delete->estimate);
	}
	free(steps_frames);
}

int init_frame(fframe* frame, size_t size) {
	frame->possibly_moves = (ppoint*)calloc(size * size, sizeof(ppoint));
	frame->estimate = (double*)calloc(size * size, sizeof(double));
	// printf("ALLOCATED SIZE: %i\n", size * size);
	if (!frame->possibly_moves) {
		return 1;
	}
	frame->moves_quantity = 0;
	return 0;
}

fframe* create_frames(struct game_env* env) {
	fframe* steps_frames;
	steps_frames = (fframe*)calloc(env->deep + 2, sizeof(fframe));
	if (!steps_frames)
		return NULL;
	for (ssize_t i = 0; i < env->deep + 1; ++i) {
		if (init_frame(steps_frames + i, env->size)) {
			free_frames(steps_frames, env);
			return NULL;
		}
	}
	return steps_frames;
}


