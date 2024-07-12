#include "src/lib/core.h"

Object *make_Animal(Object *v0, Object *v1);

void attr_Animal(Object *v0, Object *v1, Object *v2);

Object *type_Animal_name(Object *v0);

Object *type_Animal_age(Object *v0);

Object *make_Dog(Object *v0, Object *v1, Object *v2);

void attr_Dog(Object *v0, Object *v1, Object *v2, Object *v3);

Object *type_Dog_ladra(Object *v0, Object *v1, Object *v2);

Object *make_Cat(Object *v0, Object *v1, Object *v2);

void attr_Cat(Object *v0, Object *v1, Object *v2, Object *v3);

Object *type_Cat_maulla(Object *v0);

Object *make_Animal(Object *v0, Object *v1)
{
	Object *v2 = __create_object();
	__add_member(v2, "f_name", *type_Animal_name);
	__add_member(v2, "f_age", *type_Animal_age);
	__add_member(v2, "type", "Animal");
	int *v3 =  malloc(sizeof(int));
	*v3 =  5;
	__add_member(v2, "type_ind", v3);
	attr_Animal(v2, v0, v1);
	return v2;
}

void attr_Animal(Object *v0, Object *v1, Object *v2)
{
	Object *v3 = v1;
	__add_member(v0, "p_name", v3);
	Object *v4 = v2;
	__add_member(v0, "p_age", v4);
}

Object *type_Animal_name(Object *v0)
{
	Object *v1 = __find_member(v0, "p_name");
	return v1;
}

Object *type_Animal_age(Object *v0)
{
	Object *v1 = __find_member(v0, "p_age");
	return v1;
}

Object *make_Dog(Object *v0, Object *v1, Object *v2)
{
	Object *v3 = __create_object();
	__add_member(v3, "f_name", *type_Animal_name);
	__add_member(v3, "f_age", *type_Animal_age);
	__add_member(v3, "f_ladra", *type_Dog_ladra);
	__add_member(v3, "type", "Dog");
	int *v4 =  malloc(sizeof(int));
	*v4 =  6;
	__add_member(v3, "type_ind", v4);
	attr_Dog(v3, v0, v1, v2);
	return v3;
}

void attr_Dog(Object *v0, Object *v1, Object *v2, Object *v3)
{
	Object *v4 = v1;
	__add_member(v0, "p_race", v4);
	Object *v5 = v2;
	Object *v6 = v3;
	attr_Animal(v0, v5, v6);
}

Object *type_Dog_ladra(Object *v0, Object *v1, Object *v2)
{
	Object *v4 = __make_string("esta ladrando");
	Object *v5 = v4;
	Object *v7 = v1;
	Object *v9 = __make_string(" ");
	Object *v10 = v2;
	Object *v8 = __concat_string(v9, v10);
	Object *v6 = __concat_string(v7, v8);
	Object *v12 = __make_string(" ");
	Object *v13 = v5;
	Object *v11 = __concat_string(v12, v13);
	Object *v3 = __concat_string(v6, v11);
	return v3;
}

Object *make_Cat(Object *v0, Object *v1, Object *v2)
{
	Object *v3 = __create_object();
	__add_member(v3, "f_name", *type_Animal_name);
	__add_member(v3, "f_age", *type_Animal_age);
	__add_member(v3, "f_maulla", *type_Cat_maulla);
	__add_member(v3, "type", "Cat");
	int *v4 =  malloc(sizeof(int));
	*v4 =  7;
	__add_member(v3, "type_ind", v4);
	attr_Cat(v3, v0, v1, v2);
	return v3;
}

void attr_Cat(Object *v0, Object *v1, Object *v2, Object *v3)
{
	Object *v4 = v1;
	__add_member(v0, "p_race", v4);
	Object *v5 = v2;
	Object *v6 = v3;
	attr_Animal(v0, v5, v6);
}

Object *type_Cat_maulla(Object *v0)
{
	Object *v2 = __make_string("esta maullando como un");
	Object *v3 = v2;
	Object *v7 = v0;
	Object *(*v8)(Object *) = __find_member(v7, "f_name");
	Object *v6 = v8(v7);
	Object *v10 = __make_string(" ");
	Object *v12 = v0;
	Object *(*v13)(Object *) = __find_member(v12, "f_age");
	Object *v11 = v13(v12);
	Object *v9 = __concat_string(v10, v11);
	Object *v5 = __concat_string(v6, v9);
	Object *v15 = __make_string(" ");
	Object *v16 = v3;
	Object *v14 = __concat_string(v15, v16);
	Object *v4 = __concat_string(v5, v14);
	Object *v18 = __make_string(" ");
	Object *v19 = __find_member(v0, "p_race");
	Object *v17 = __concat_string(v18, v19);
	Object *v1 = __concat_string(v4, v17);
	return v1;
}

int **hierarchy_graph = NULL;

int main()
{
	srand(time(NULL));
	hierarchy_graph = malloc(sizeof(int*) * 9);
	hierarchy_graph[0] = malloc(sizeof(int) * 1);
	hierarchy_graph[0][0] = 0;
	hierarchy_graph[1] = malloc(sizeof(int) * 2);
	hierarchy_graph[1][0] = 1;
	hierarchy_graph[1][1] = 0;
	hierarchy_graph[2] = malloc(sizeof(int) * 2);
	hierarchy_graph[2][0] = 1;
	hierarchy_graph[2][1] = 0;
	hierarchy_graph[3] = malloc(sizeof(int) * 2);
	hierarchy_graph[3][0] = 1;
	hierarchy_graph[3][1] = 0;
	hierarchy_graph[4] = malloc(sizeof(int) * 3);
	hierarchy_graph[4][0] = 2;
	hierarchy_graph[4][1] = 0;
	hierarchy_graph[4][2] = 8;
	hierarchy_graph[5] = malloc(sizeof(int) * 2);
	hierarchy_graph[5][0] = 1;
	hierarchy_graph[5][1] = 0;
	hierarchy_graph[6] = malloc(sizeof(int) * 2);
	hierarchy_graph[6][0] = 1;
	hierarchy_graph[6][1] = 5;
	hierarchy_graph[7] = malloc(sizeof(int) * 2);
	hierarchy_graph[7][0] = 1;
	hierarchy_graph[7][1] = 5;
	hierarchy_graph[8] = malloc(sizeof(int) * 1);
	hierarchy_graph[8][0] = 0;
	Object *v2 = __make_string("sato");
	Object *v3 = __make_string("balto");
	Object *v4 = __make_number(7);
	Object *v1 = make_Dog(v2, v3, v4);
	Object *v5 = v1;
	Object *v7 = __make_string("siames");
	Object *v8 = __make_string("Lucas");
	Object *v9 = __make_number(4);
	Object *v6 = make_Cat(v7, v8, v9);
	Object *v10 = v6;
	Object *v13 = v10;
	Object *(*v14)(Object *) = __find_member(v13, "f_maulla");
	Object *v12 = v14(v13);
	Object *v11 = ___builtin_print(v12);
	Object *v16 = v5;
	Object *(*v17)(Object *, Object *, Object *) = __find_member(v16, "f_ladra");
	Object *v18 = __make_string("alex");
	Object *v19 = __make_number(22);
	Object *v15 = v17(v16, v18, v19);
	Object *v0 = ___builtin_print(v15);
}