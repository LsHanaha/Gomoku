#include "algo.h"

// static double estimate_diagonale(g_env* env, unsigned char for_player, int *have_five) {

// }

typedef struct estimate_counter {
	int free_accum;
	int prev_section_len;
	int prev_section_free;
	int section_len;
	int post_section_free;
	int post_section_len;
	///////
	double estimate;
	int find_five_in_row;
	///////
	int is_enemy_win;
	int is_player_move_next;
} e_counter;

static void clean(e_counter* c) {
	c->free_accum = 0;
	c->prev_section_len = 0;
	c->prev_section_free = 0;
	c->section_len = 0;
	c->post_section_free = 0;
	c->post_section_len = 0;
	c->estimate = 0.0;
	c->find_five_in_row = 0;
	c->is_enemy_win = 0;
}

// Вариант оценивания 2:
// оцениваем сегменты - непрерывные последовательности из шашек.
// Алгоритм однопроходный
// для каждой сегмента нужно знать:
// 0. Сколько было раньше свободных клеток? (нужно, чтобы в случае [.*.*.*.*.*] не пропустить сегмент)
// 1. количество шашек до секции
// 2. количество свободного места до
// 3. длину секции
// 4. количество свободного пространства после секции
// 5. количество своих шашек после секции
//          |- это центр сегмента
// [***....***....*****]
// [free_accum, prev_section_len, prev_section_free, section_len, post_section_free, post_section_len]

// каждый раз, когда заканчивается линия из наших шашек, а следующая точка - пустое пространство,
// вызывается функция end_segment
//	В ней:
	// - оцениваем сегмент
	// - сдвигаем его ( section_len становится prev_section_len, post_section_len становится section_len)

// каждый раз,когда
		// 		- Заканчивается линия
		// 		- Мы встречаем вражескую шашку
		// 		- Встречаем свободное пространство длиннее чем 4
	// вызывается функция end_line()


// [0, 0, 0, 4, 4] - конец первой последовательности. Если вызывается функция end_line - оцениваем позицию как [0, 4, 4, 0, 0] // СТАРТ
							// Если вызывается функция end_segment - ничего не оцениваем, только сдвигаем сегмент
							// [0, 4, 4, 0, 0]
//	Далее считаем свои камни, находим следующий конец сегмента:    [0, 4, 4, 3, 1]  // ШАГ АЛГОРИТМА
// 									Для любой функции: оцениваем сегмент.
//									Для end_line: сдвигаем сегмент (до [4, 3, 1, 0, 0])
//																	И оцениваем его еще раз







// [ ...*.***.*]
// [ ...*........***..........*]
// [*****] - выигрыш
// [.****.] - беспроигрышная позиция
// [.****] - есть шанс выиграть через ход (особенно если есть 2 такие штуки)
// [****.] - 
// [..***.] - можно выиграть
// [.***..] - 
// [.**..] - лучше 2 камня с пространством вокруг, чем 3 камня, прижатые к стенке 
// [***...] - блокируется в один ход
// [....*...] - лучше ставить фишку так, чтобы рядом было как можно больше свободного места.
// Максимум в одну сторону может быть 4 свободных места, больше - не влияет

// Алгоритм:
// если свободного места меньше 5 - не оцениваем 
// Если камней 3 и больше и есть свободное место с 2 сторон:


// Оценка сегмента:
// Камни с краев считаем за свободное место, так же даем за них бонусные баллы (длина * 100 - свободное пространство * 60)
// Если свободного места < 5: сразу ноль

// Если центр - выигрыш: +100,000 , но если у противника уже есть 5 подряд - 0 (так выигрыш не сбить)
// Если 4, свободное место с 2 сторон: + 10,000, если следующий ход игрока - *2
// Если 4, свободное место с одной стороны: + 5,000, если следующий ход игрока - *2
// Если 3, свободное место с обоих сторон, свободного места в сумме больше 3: + (2,000 ??? между 2500 и 1000), если следующий ход игорка - *2
// Если 3, свободное место с обоих стон, свободного места в сумме 2: + 1200 (если ход игрока - умножить на 2)
// Если 3, с одной стороны свободного места нет: +1000  (если ход игрока - умножить на 1.5)
//								Слишком сильное падение баллов?
// Если 2, свободное место с 2 сторон, в сумме свободного места больше 3: +200  (если ход игрока - умножить на 1.2)
// Если 2, свободное место с 2 сторон, в сумме свободного места = 3: +150 (если ход игрока - умножить на 1.2)
// Если 2, свободное место только с одной стороны, свободного места больше 3: + 74 // между 70 и 140 (если ход игрока - умножить на 1.2)
// Если 1, свободное место с 2 сторон, свободного места больше 4: +15  (если ход игрока - умножить на 1.2)
// Если 1, свободное место с 2 сторон, свободного места = 4: +5 // ну вообще без шансов (если ход игрока - умножить на 1.2)
// Если 1, свободное место с 1 сторон, свободного места = 4: +2 // ну воооообще без шансов (если ход игрока - умножить на 1.2)

// [free_accum, prev_section_len, prev_section_free, section_len, post_section_free, post_section_len]
static void estimate(e_counter* c) {
	int free_left = c->free_accum + c->prev_section_len + c->prev_section_free;
	int free_right = c->post_section_free + c->post_section_len;
	int free_sum_accum = free_left + free_right;

	if (free_sum_accum + c->section_len < 5) {
			return;
	}

	// Камни с краев считаем за свободное место, так же даем за них бонусные баллы (длина * 100 - свободное пространство * 40)
	c->estimate += MAX((c->prev_section_len + c->post_section_len) * 100 - (c->prev_section_free + c->post_section_free) * 40, 0);

	switch (c->section_len) {
		case 4:
			if (free_left > 0 && free_right > 0) {
				// [.****.] // Если 4, свободное место с 2 сторон: + 10,000, если следующий ход игрока - *2
				if (c->is_player_move_next) {
					c->estimate += 20000;
				} else {
					c->estimate += 10000;
				}
			} else {
				// [.****], [****.] // Если 4, свободное место с одной стороны: + 5,000, если следующий ход игрока - *2
				if (c->is_player_move_next) {
					c->estimate += 10000;
				} else {
					c->estimate += 5000;
				}
			}
			break;
		case 3:
			// Если 3, свободное место с обоих сторон, свободного места в сумме больше 3: + (2,000 ??? между 2500 и 1000), если следующий ход игорка - *2
			if (free_left > 0 && free_right > 0 && free_left + free_right > 2) { // > 2???
				if (c->is_player_move_next) {
					c->estimate += 4000;
				} else {
					c->estimate += 2000;
				}
			} else if (free_left > 0 && free_right > 0) {
				// Если 3, свободное место с обоих стон, свободного места в сумме 2: + 1200 (если ход игрока - умножить на 2)
				c->estimate += (c->is_player_move_next) ? 1900 : 1200;
			} else {
				// Если 3, с одной стороны свободного места нет: +1000  (если ход игрока - умножить на 1.5)
				c->estimate += (c->is_player_move_next) ? 1100 : 1000;
			}
			break;
		case 2:
			if (free_left > 0 && free_right > 0 && free_left + free_right > 3) {
				// Если 2, свободное место с 2 сторон, в сумме свободного места больше 3: +200  (если ход игрока - умножить на 1.2)
				c->estimate += (c->is_player_move_next) ? 240 : 200;
			} else if (free_left > 0 && free_right > 0) {
				// Если 2, свободное место с 2 сторон, в сумме свободного места = 3: +150 (если ход игрока - умножить на 1.2)
				c->estimate += (c->is_player_move_next) ? 180 : 150;
			} else {
				// Если 2, свободное место только с одной стороны: + 74 // между 70 и 140 (если ход игрока - умножить на 1.2)
				c->estimate += (c->is_player_move_next) ? 80 : 74;
			}
			break;
		case 1:
			if (free_left > 0 && free_right > 0 && free_left + free_right > 4) {
				// Если 1, свободное место с 2 сторон, свободного места больше 4: +15  (если ход игрока - умножить на 1.2)
				c->estimate += (c->is_player_move_next) ? 18 : 15;
			} else if (free_left > 0 && free_right > 0) { 
				// Если 1, свободное место с 2 сторон, свободного места = 4: +5 // ну вообще без шансов (если ход игрока - умножить на 1.2)
				c->estimate += 5;
			} else {
				// Если 1, свободное место с 1 сторон, свободного места = 4: +2 // ну воооообще без шансов (если ход игрока - умножить на 1.2)
				c->estimate += 5;
			}
			break;
		case 0:
			break;
		default: // 5 или больше
			if (c->section_len < 5) {
				printf("WTH??\n");
				exit(1);
				break;
			}
			c->find_five_in_row = 1;
			printf("FIND VICTORY!!\n");
			if (c->is_enemy_win) {
				c->estimate += 5000; // враг уже победил, так победу не сбить
			} else {
				c->estimate += 100000; // возможно, победа
			}
			break;
	}
}

// [0, 0, 0, 4, 4] - конец первой последовательности. Если вызывается функция end_line - оцениваем позицию как [0, 4, 4, 0, 0] // СТАРТ
							// Если вызывается функция end_segment - ничего не оцениваем, только сдвигаем сегмент : [0, 4, 4, 0, 0]
//	Далее считаем свои камни, находим следующий конец сегмента:    [0, 4, 4, 3, 1]  // ШАГ АЛГОРИТМА
// 									Для любой функции: оцениваем сегмент, сдвигаем его
//									
//
//									Для end_line: сдвигаем сегмент (до [4, 3, 1, 0, 0])
//																	И оцениваем его еще раз
static void end_segment(e_counter* c) {
	if (c->section_len) {
		estimate(c);
	}
	// оцениваем тут??

	c->free_accum += c->prev_section_len + c->prev_section_free;
	c->prev_section_len = c->section_len;
	c->prev_section_free = c->post_section_free;
	c->section_len = c->post_section_len;
	c->post_section_free = 0;
	c->post_section_len = 0;
}

// commit read line
static void end_line(e_counter* c) {
	// c->estimate += estimate(c->counter, c->free_spaces_in_row - c->free_accum, c->free_spaces);
	end_segment(c); // оцениваем текущий сегмент
	end_segment(c); // сдвигаем и оцениваем крайний сегмент
	c->free_accum = 0;
	c->prev_section_len = 0;
	c->prev_section_free = 0;
	c->section_len = 0;
	c->post_section_free = 0;
	c->post_section_len = 0;
}


// Check():
// функция вызывается для каждой клетки
// В функции check меняем только последние 2 переменные - post_section_free, post_section_len
// Если видим свою шашку, а переменная post_section_free > 0:    (если post_section_free==0  - что-то пошло не так, такого не должно быть никогда)
// 		++post_section_len;
// Если видим свободное место, а post_section_len==0:
//		 ++post_section_free
// Если видим свободное место, а post_section_len > 0:
// 		Сегмент закончился, вызываем end_segment(), post_section_free=1
// Если видим чужую шашку (или из функции выше вызывается end_line):
//		end_line()
// [free_accum, prev_section_len, prev_section_free, section_len, post_section_free, post_section_len]
// [. . . 0 0]
// 			if is_free and post_section_len == 0:
//				post_section_free++
//			else 

static void check(e_counter* c, int is_free, int is_player) {

	if (is_player) {
		++(c->post_section_len);
	} else if (is_free && c->post_section_len == 0) {
		++(c->post_section_free);
	} else if (is_free && c->post_section_len > 0) {
		end_segment(c); // оценка и сдвиг сегмента
		c->post_section_free = 1;
	} else {
		if (is_free || is_player) {
			printf("WTH22??\n");
			exit(1);
		}
		end_line(c);
	}
}

// проходим по линиям
static double estimate_check_line(g_env* env, unsigned char for_player, int *have_five, int is_player_next_move) {
	e_counter counter;

	clean(&counter);
	counter.is_player_move_next = is_player_next_move;
	for (long x = 0; x < env->size; ++x) {
		for (long y = 0; y < env->size; ++y) {
			check(&counter, env->desk[x][y] == EMPTY, env->desk[x][y] == for_player);
		}
		end_line(&counter);
	}
	*have_five = MAX(*have_five, counter.find_five_in_row);
	return counter.estimate;
}

// проходим по столбцам
static double estimate_check_column(g_env* env, unsigned char for_player, int *have_five, int is_player_next_move) {
	e_counter counter;

	clean(&counter);
	counter.is_player_move_next = is_player_next_move;
	for (long x = 0; x < env->size; ++x) {
		for (long y = 0; y < env->size; ++y) {
			check(&counter, env->desk[y][x] == EMPTY, env->desk[y][x] == for_player);
		}
		end_line(&counter);
	}
	*have_five = MAX(*have_five, counter.find_five_in_row);
	return counter.estimate;
}

// диагональ вправо вниз
static double estimate_diagonale(g_env* env, unsigned char for_player, int *have_five, int is_player_next_move) {
	e_counter counter;

	clean(&counter);
	counter.is_player_move_next = is_player_next_move;
	for (long i = env->size - 1; i > -env->size; --i) {
		long first_y = ABS(MIN(0, i));
		long first_x = MAX(0, i);
		for (long j = 0; j < env->size; ++j) {
			if (first_y + j >= env->size || first_x + j >= env->size){
				break;
			}
			check(&counter, env->desk[first_y + j][first_x + j] == EMPTY, env->desk[first_y + j][first_x + j] == for_player);
		}
		end_line(&counter);
	}
	*have_five = MAX(*have_five, counter.find_five_in_row);
	return counter.estimate;
}

// диагональ влево вниз
static double estimate_diagonale_2(g_env* env, unsigned char for_player, int *have_five, int is_player_next_move) {
	e_counter counter;

	clean(&counter);
	counter.is_player_move_next = is_player_next_move;
	for (long i = 0; i < env->size * 2 - 1 ; ++i) {
		long first_y = MIN(i, env->size - 1);
		long first_x = MAX(0, i - (env->size - 1));
		for (long j = 0; j < env->size; ++j) {
			if (first_y - j < 0 || first_x + j >= env->size){
				break;
			}
			check(&counter, env->desk[first_y - j][first_x + j] == EMPTY, env->desk[first_y - j][first_x + j] == for_player);
		}
		end_line(&counter);
	}
	*have_five = MAX(*have_five, counter.find_five_in_row);
	return counter.estimate;
}

// int is_game_finished(g_env* env, int is_player_move) {
// 	if (env->enemy_capture >= MAX_CAPTURES || env->player_capture >= MAX_CAPTURES) {
// 		return true;
// 	}
// 	int five_in_row = 0;
// 	// int player = is_player_move ? PLAYER : ENEMY;
// 	estimate_check_line(env, PLAYER, &five_in_row);
// 	estimate_check_column(env, PLAYER, &five_in_row);
// 	estimate_diagonale(env, PLAYER, &five_in_row);
// 	estimate_diagonale_2(env, PLAYER, &five_in_row);
// 	estimate_check_line(env, ENEMY, &five_in_row);
// 	estimate_check_column(env, ENEMY, &five_in_row);
// 	estimate_diagonale(env, ENEMY, &five_in_row);
// 	estimate_diagonale_2(env, ENEMY, &five_in_row);
// 	// TODO:
// 	// Находим 5 камней подряд
// 	// Рассматриваем все возможные ходы
// 	// если есть ход, где выигрывает другой игрок -игра не закончена


// 	return five_in_row;
// }

double estimate_position(g_env* env, int* five_in_row, int player) {
	int is_player_next_move = 0;
	// double mult = 1.0; //(player == PLAYER) ? 1.01 : 0.99
	if (player == PLAYER) {
		is_player_next_move = 1; // Только что закончил ход игрок. Сейчас ходит игрок, у него есть преимущество
	}
	double estimate = estimate_check_line(env, PLAYER, five_in_row, is_player_next_move) + 
			estimate_check_column(env, PLAYER, five_in_row, is_player_next_move) + 
			estimate_diagonale(env, PLAYER, five_in_row, is_player_next_move) + 
			estimate_diagonale_2(env, PLAYER, five_in_row, is_player_next_move) - 
			estimate_check_line(env, ENEMY, five_in_row, !is_player_next_move) -
			estimate_check_column(env, ENEMY, five_in_row, !is_player_next_move) -
			estimate_diagonale(env, ENEMY, five_in_row, !is_player_next_move) -
			estimate_diagonale_2(env, ENEMY, five_in_row, !is_player_next_move);
	return estimate;
}

