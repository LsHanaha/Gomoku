#include "algo.h"

// static double estimate_diagonale(g_env* env, unsigned char for_player, int *have_five) {

// }

typedef struct estimate_counter {
	int free_spaces;
	int free_spaces_in_row;
	int free_accum;
	int counter;
	int five_in_row;
	int row;
	double estimate;
} e_counter;

static void clean(e_counter* c) {
	c->free_spaces = 0;
	c->free_spaces_in_row = 0;
	c->free_accum = 0;
	c->row = 0;
	c->counter = 0;
	c->estimate = 0.0;
	c->five_in_row = 0;
}

// Вариант оценивания 2:
// оцениваем сегменты - непрерывные последовательности из шашек.
// Алгоритм однопроходный
// для каждой сегмента нужно знать:
// 1. количество шашек до секции
// 2. количество свободного места до
// 3. длину секции
// 4. количество свободного пространства после секции
// 5. количество своих шашек после секции
//          |- это центр сегмента
// [***....***....*****]
// [prev_section_len, prev_section_free, section_len, post_section_free, post_section_len]

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
							[0, 4, 4, 0, 0]
//	Далее считаем свои камни, находим следующий конец сегмента:    [0, 4, 4, 3, 1]  // ШАГ АЛГОРИТМА
// 									Для любой функции: оцениваем сегмент.
//									Для end_line: сдвигаем сегмент (до [4, 3, 1, 0, 0])
//																	И оцениваем его еще раз




// Check():
// В функции check меняем только последние 2 переменные - post_section_free, post_section_len
// Если видим свою шашку, а переменная post_section_free > 0:    (если post_section_free==0  - что-то пошло не так, такого не должно быть никогда)
// 		++post_section_len;
// Если видим свободное место, а post_section_len==0:
//		 ++post_section_free
// Если видим свободное место, а post_section_len > 0:
// 		Сегмент закончился, вызываем end_segment(), post_section_free=1
// Если видим чужую шашку (или из функции выше вызывается end_line):
//		end_line()



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



//////// Старый алгоритм:
// Если внутри линии пропусков не больше камней - считаем это рядом
//[..... *.*.*....]
//[..... ***.*....]
//[..... **..*....]
//[..... ***......]
//[..... *....*....]
// свободных клеток + камней должно быть минимум 5
// 

// [.**..*..] меньше, чем [.**.*...]
// [.**.*...] меньше, чем [.***....]

// Оцениваем ряд:
// (количество камней) ^ 2 - (количество пустых клеток в ряде) ^ 2
static double estimate(int counter, int free_spaces_in_row, int free_spaces) {
	if (counter && counter > free_spaces_in_row &&
							counter + free_spaces_in_row + free_spaces >= WIN_LENGTH) {
		return ((counter + 1) * (counter + 1) * 100) - (free_spaces_in_row * free_spaces_in_row * 10) + free_spaces * 30;
	
	} else {
		return 0.0;
	}
}
// commit read line
static void new_line(e_counter* c) {
	c->estimate += estimate(c->counter, c->free_spaces_in_row - c->free_accum, c->free_spaces);
	c->free_spaces = 0;
	c->row = 0;
	c->free_spaces_in_row = 0;
	c->free_accum = 0;
	c->counter = 0;
}

// функция вызывается для каждой клетки
static void check(e_counter* c, int is_free, int is_player) {
	if (is_player) {
		if (!c->counter) {  // нашли новую линию. ограничиваем соседние пустые клетки
			c->free_spaces = MIN(3, c->free_spaces);
			c->free_spaces_in_row = 0;
		}
		// ++c->in_row;
		++c->counter;
		c->free_accum = 0;
		++c->row;
		if (c->row >= WIN_LENGTH) {
			// Если уже есть линия - останавливаемся и оцениваем.
			// TODO: записывать линию в отдельный массив и оценивать массив целиком, а не через 3 переменные
			// c->estimate += estimate(c->counter, c->free_spaces_in_row, c->free_spaces);
			c->estimate += WIN_ESTIMATE;
			c->counter = 0;
			c->five_in_row = true;
		}
	} else if (is_free) {
		if (c->counter) {
			++c->free_spaces_in_row;
		}
		c->row = 0;
		++c->free_spaces;
		++c->free_accum;
	} else {
		new_line(c);
		// c->estimate += estimate(c->counter, c->free_spaces_in_row - c->free_accum, c->free_spaces);
		// c->free_accum = 0;
		// c->free_spaces = 0;
		// c->free_spaces_in_row = 0;
		// c->counter = 0;
		// enemy
	}
}

// проходим по линиям
static double estimate_check_line(g_env* env, unsigned char for_player, int *have_five) {
	e_counter counter;

	clean(&counter);
	for (int x = 0; x < env->size; ++x) {
		for (int y = 0; y < env->size; ++y) {
			check(&counter, env->desk[x][y] == EMPTY, env->desk[x][y] == for_player);
		}
		new_line(&counter);
	}
	*have_five = MAX(*have_five, counter.five_in_row);
	return counter.estimate;
}
// проходим по столбцам
static double estimate_check_column(g_env* env, unsigned char for_player, int *have_five) {
	e_counter counter;

	clean(&counter);
	for (int x = 0; x < env->size; ++x) {
		for (int y = 0; y < env->size; ++y) {
			check(&counter, env->desk[y][x] == EMPTY, env->desk[y][x] == for_player);
		}
		new_line(&counter);
	}
	*have_five = MAX(*have_five, counter.five_in_row);
	return counter.estimate;
}

// диагональ вправо вниз
static double estimate_diagonale(g_env* env, unsigned char for_player, int *have_five) {
	e_counter counter;

	clean(&counter);
	for (int i = env->size - 1; i > -env->size; --i) {
		int first_y = ABS(MIN(0, i));
		int first_x = MAX(0, i);
		for (int j = 0; j < env->size; ++j) {
			if (first_y + j >= env->size || first_x + j >= env->size){
				break;
			}
			check(&counter, env->desk[first_y + j][first_x + j] == EMPTY, env->desk[first_y + j][first_x + j] == for_player);
		}
		new_line(&counter);
	}
	*have_five = MAX(*have_five, counter.five_in_row);
	return counter.estimate;
}

// диагональ влево вниз
static double estimate_diagonale_2(g_env* env, unsigned char for_player, int *have_five) {
	e_counter counter;
	clean(&counter);

	for (int i = 0; i < env->size * 2 - 1 ; ++i) {
		int first_y = MIN(i, env->size - 1);
		int first_x = MAX(0, i - (env->size - 1));
		for (int j = 0; j < env->size; ++j) {
			if (first_y - j < 0 || first_x + j >= env->size){
				break;
			}
			check(&counter, env->desk[first_y - j][first_x + j] == EMPTY, env->desk[first_y - j][first_x + j] == for_player);
		}
		new_line(&counter);
	}
	*have_five = MAX(*have_five, counter.five_in_row);
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
	// int five_in_row;
	// double mult = 1.0; //(player == PLAYER) ? 1.01 : 0.99
	// if (player == ENEMY) {
	// 	mult = 1.01; // Только что закончил ход игрок. Боту нужно в первую очередь помешать игроку
	// } else {
	// 	mult = 0.99; // Только что закончил ход бот. 
	// }
	return estimate_check_line(env, PLAYER, five_in_row) + 
			estimate_check_column(env, PLAYER, five_in_row) + 
			estimate_diagonale(env, PLAYER, five_in_row) + 
			estimate_diagonale_2(env, PLAYER, five_in_row) - 
			estimate_check_line(env, ENEMY, five_in_row) -
			estimate_check_column(env, ENEMY, five_in_row) -
			estimate_diagonale(env, ENEMY, five_in_row) -
			estimate_diagonale_2(env, ENEMY, five_in_row);
}

