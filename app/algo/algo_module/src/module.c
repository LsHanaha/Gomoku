
#include "algo.h"
#include <Python.h>

static void* create_map(struct game_env* env, PyObject* list) {
	env->size = PyList_Size(list);
	env->desk = (unsigned char**)calloc(env->size + 1, sizeof(unsigned char*));
//	printf("read player: %u\n", env->player);
//	printf("read deep: %u\n", env->deep);
	if (!env->desk) {
		PyErr_SetString(PyExc_TypeError, "Memory issue");
		return NULL;
	}

  	for (Py_ssize_t i = 0; i < env->size; i++) {
		env->desk[i] = (unsigned char*)calloc(env->size, sizeof(unsigned char));
		if (!env->desk[i]) {
			PyErr_SetString(PyExc_TypeError, "Memory issue");
			free_desk(env->desk);
			return NULL;
		}
		PyObject* sublist = PyList_GetItem(list, i);

		if (!PyList_Check(sublist)) {
			PyErr_SetString(PyExc_TypeError, "List must contain lists");
			free_desk(env->desk);
			return NULL;
		}
		if (PyList_Size(sublist) != env->size) {
			PyErr_SetString(PyExc_TypeError, "Desk should be square");
			free_desk(env->desk);
			return NULL;
		}
		for (Py_ssize_t j = 0; j < env->size; j++) {
			unsigned char point = (unsigned char)PyLong_AsLong(PyList_GetItem(sublist, j));
			if (!point) {
				env->desk[i][j] = EMPTY;
			} else if (env->player == point) {
				env->desk[i][j] = PLAYER;
			} else {
				env->desk[i][j] = ENEMY;
			}
			if (PyErr_Occurred()){
				free_desk(env->desk);
				return NULL;
			}
		}
  	}
	return env;
}


static void* parse_args_get_moves(struct game_env* env, PyObject* args) {

	PyObject * list;
	// rules, player_capture, enemy_capture)
	 if (!PyArg_ParseTuple(args, "O!bIiii", &PyList_Type, &list, &env->player, &env->deep,
								&env->rules, &env->player_capture,	&env->enemy_capture))
			return NULL;
	if (!create_map(env, list)) {
		return NULL;
	}
	
	  //memory leaks? unref PyObjects?
	return env;
}


PyObject* create_python_answer(g_env* env) {
	// int const N = 10;

	PyObject* estimates = PyList_New(env->first_frame.moves_quantity);
    for (int i = 0; i < env->first_frame.moves_quantity; ++i)
    {
        // int r = rand() % 10;
		//printf("Get estimate: %f\n", env->first_frame.estimate[i]);
        PyObject* python_est = PyFloat_FromDouble(env->first_frame.estimate[i]);
        PyList_SetItem(estimates, i, python_est);
    }
	PyObject* moves = PyList_New(env->first_frame.moves_quantity);
    for (int i = 0; i < env->first_frame.moves_quantity; ++i)
    {
        // int r = rand() % 10;
        PyObject* x = Py_BuildValue("i", (int)env->first_frame.possibly_moves[i].x);
        PyObject* y = Py_BuildValue("i", (int)env->first_frame.possibly_moves[i].y);
		PyObject* point = PyList_New(2);
        PyList_SetItem(point, 0, x);
        PyList_SetItem(point, 1, y);
        PyList_SetItem(moves, i, point);
    }

	PyObject* ans = PyList_New(2);
	PyList_SetItem(ans, 0, estimates);
	PyList_SetItem(ans, 1, moves);
	return ans;
}

// Точка входа
PyObject* get_moves(PyObject* self, PyObject* args) {
	struct game_env env;
	if (!parse_args_get_moves(&env, args))
		return NULL;
	// print_desk(&env);
	minmax_start(&env);

	return create_python_answer(&env);

	// return PyFloat_FromDouble(0.0);
}

PyObject* implement_move(PyObject* self, PyObject* args) {
	struct game_env env;
	int x;
	int y;
	unsigned char enemy_id;
	PyObject* list;

	if (!PyArg_ParseTuple(args, "O!bbiii", &PyList_Type, &list, &env.player, &enemy_id,
								&env.rules, &x, &y))
		return NULL;
	create_map(&env, list);
	move_info move;
	move.p.x = x;
	move.p.y = y;
	create_step(&env, &move, true);
	for (Py_ssize_t i = 0; i < env.size; i++) {
		PyObject* sublist = PyList_GetItem(list, i);

		if (!PyList_Check(sublist)) {
			PyErr_SetString(PyExc_TypeError, "List must contain lists");
			free_desk(env.desk);
			return NULL;
		}
		if (PyList_Size(sublist) != env.size) {
			PyErr_SetString(PyExc_TypeError, "Desk should be square");
			free_desk(env.desk);
			return NULL;
		}
		for (Py_ssize_t j = 0; j < env.size; j++) {
			int point_value = 0;
			if (env.desk[i][j] == EMPTY) {
				point_value = 0;
			} else if (env.desk[i][j] == PLAYER) {
				point_value = env.player;
			} else {
				point_value = enemy_id;
			}
			PyObject* x = Py_BuildValue("i", point_value);
			PyList_SetItem(sublist, j, x);
		}
  	}
	// print_desk(&env);
	// minmax_start(&env);

	// return create_python_answer(&env);
	return list;
	// return PyFloat_FromDouble(0.0);
}

PyObject* is_step_allowed_py(PyObject* self, PyObject* args) {
	struct game_env env;
	PyObject* list;
	int x;
	int y;
	if (!PyArg_ParseTuple(args, "O!biii", &PyList_Type, &list, &env.player,
								&env.rules, &x, &y))
		return NULL;
	
	create_map(&env, list);
	int is_game_finished = 0;
	if (is_step_allowed(&env, x, y, env.player)) {
		return Py_BuildValue("i", 1);
	} else {
		return Py_BuildValue("i", 0);
	}
}


PyObject* is_victory(PyObject* self, PyObject* args) {
	struct game_env env;
	PyObject* list;

	if (!PyArg_ParseTuple(args, "O!bi", &PyList_Type, &list, &env.player,
								&env.rules))
		return NULL;
	
	create_map(&env, list);
	int is_game_finished = 0;
	double position_score = estimate_position(&env, &is_game_finished, PLAYER);
	if (!is_game_finished) {
		return Py_BuildValue("i", EMPTY);
	} else if (position_score > 0) {
		return Py_BuildValue("i", PLAYER);
	}
	return Py_BuildValue("i", ENEMY);
}


// array containing the module's methods' definitions
// put here the methods to export
// the array must end with a {NULL} struct
PyMethodDef module_methods[] = 
{
		// {"c_fib", c_fib, METH_VARARGS, "Method description"},
		{"get_moves", get_moves, METH_VARARGS, "get possibly good moves"},
		{"implement_move", implement_move, METH_VARARGS, "get map after move"},
		{"is_step_allowed", is_step_allowed_py, METH_VARARGS, "get map after move"},
		{"is_victory", is_victory, METH_VARARGS, "check is victory"},
		{NULL} // this struct signals the end of the array
};

// struct representing the module
struct PyModuleDef c_module =
{
		PyModuleDef_HEAD_INIT, // Always initialize this member to PyModuleDef_HEAD_INIT
		"algo_module", // module name
		"Module description", // module description
		-1, // module size (more on this later)
		module_methods // methods associated with the module
};

// function that initializes the module
PyMODINIT_FUNC PyInit_algo_module()
{
	// srand(time(NULL));  
	return PyModule_Create(&c_module);
}