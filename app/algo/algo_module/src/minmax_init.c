#include "algo.h"

void free_frames(fframe* steps_frames) {
	fframe* to_delete = steps_frames;
	while (steps_frames) {
		free(steps_frames->possibly_moves);
		++steps_frames;
	}
	if (steps_frames->estimate)
		free(steps_frames->estimate);
	free(to_delete);
}

int init_frame(fframe* frame, int size) {
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
			free_frames(steps_frames);
			return NULL;
		}
	}
	return steps_frames;
}


