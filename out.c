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

Object *_tan(Object *v0);

Object *_cot(Object *v0);

Object *_operate(Object *v0, Object *v1);

Object *_fib(Object *v0);

Object *_gcd(Object *v0, Object *v1);

Object *make_Point(Object *v0, Object *v1);

void attr_Point(Object *v0, Object *v1, Object *v2);

Object *type_Point_getX(Object *v0);

Object *type_Point_getY(Object *v0);

Object *type_Point_setX(Object *v0, Object *v1);

Object *type_Point_setY(Object *v0, Object *v1);

Object *make_PolarPoint(Object *v0, Object *v1);

void attr_PolarPoint(Object *v0, Object *v1, Object *v2);

Object *type_PolarPoint_rho(Object *v0);

Object *make_Knight(Object *v0, Object *v1);

void attr_Knight(Object *v0, Object *v1, Object *v2);

Object *type_Knight_name(Object *v0);

Object *make_Person(Object *v0, Object *v1);

void attr_Person(Object *v0, Object *v1, Object *v2);

Object *type_Person_name(Object *v0);

Object *type_Person_hash(Object *v0);

Object *make_Superman();

void attr_Superman(Object *v0);

Object *make_Bird();

void attr_Bird(Object *v0);

Object *make_Plane();

void attr_Plane(Object *v0);

Object *make_A();

void attr_A(Object *v0);

Object *type_A_hello(Object *v0);

Object *make_B();

void attr_B(Object *v0);

Object *type_B_hello(Object *v0);

Object *make_C();

void attr_C(Object *v0);

Object *type_C_hello(Object *v0);

Object *make_Animal(Object *v0, Object *v1)
{
	Object *v2 = __create_object();
	__add_member(v2, "f_name", *type_Animal_name);
	__add_member(v2, "f_age", *type_Animal_age);
	__add_member(v2, "type", "Animal");
	int *v3 =  malloc(sizeof(int));
	*v3 =  4;
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
	*v4 =  5;
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
	*v4 =  6;
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

Object *_tan(Object *v0)
{
	Object *v3 = v0;
	Object *v2 = ___builtin_sin(v3);
	Object *v5 = v0;
	Object *v4 = ___builtin_cos(v5);
	Object *v1 = __div_number(v2, v4);
	return v1;
}

Object *_cot(Object *v0)
{
	Object *v2 = __make_number(1);
	Object *v4 = v0;
	Object *v3 = _tan(v4);
	Object *v1 = __div_number(v2, v3);
	return v1;
}

Object *_operate(Object *v0, Object *v1)
{
	Object *v5 = v0;
	Object *v6 = v1;
	Object *v4 = __add_number(v5, v6);
	Object *v3 = ___builtin_print(v4);
	Object *v9 = v0;
	Object *v10 = v1;
	Object *v8 = __sub_number(v9, v10);
	Object *v7 = ___builtin_print(v8);
	Object *v13 = v0;
	Object *v14 = v1;
	Object *v12 = __mul_number(v13, v14);
	Object *v11 = ___builtin_print(v12);
	Object *v16 = v0;
	Object *v17 = v1;
	Object *v15 = __div_number(v16, v17);
	Object *v2 = ___builtin_print(v15);
	return v2;
}

Object *_fib(Object *v0)
{
	Object *v1;
	Object *v4 = v0;
	Object *v5 = __make_number(0);
	Object *v3 = __eq(v4, v5);
	Object *v7 = v0;
	Object *v8 = __make_number(1);
	Object *v6 = __eq(v7, v8);
	Object *v2 = __or_bool(v3, v6);
	if (__to_bool(v2))
	{
		Object *v9 = __make_number(1);
		v1 = v9;
	}
	else
	{
		Object *v13 = v0;
		Object *v14 = __make_number(1);
		Object *v12 = __sub_number(v13, v14);
		Object *v11 = _fib(v12);
		Object *v17 = v0;
		Object *v18 = __make_number(2);
		Object *v16 = __sub_number(v17, v18);
		Object *v15 = _fib(v16);
		Object *v10 = __add_number(v11, v15);
		v1 = v10;
	}
	return v1;
}

Object *_gcd(Object *v0, Object *v1)
{
	Object *v2;
	Object *v5 = v0;
	Object *v6 = __make_number(0);
	Object *v4 = __eq(__comp(v5, v6), __make_number(1));
	Object *v3 = v4;
	while(__to_bool(v3))
	{
		Object *v9 = v0;
		Object *v10 = v1;
		Object *v8 = __mod_number(v9, v10);
		Object *v11 = v8;
		Object *v13 = v0;
		v1 = v13;
		Object *v12 = v13;
		Object *v14 = v11;
		v0 = v14;
		Object *v7 = v14;
		v2 = v7;
		Object *v16 = v0;
		Object *v17 = __make_number(0);
		Object *v15 = __eq(__comp(v16, v17), __make_number(1));
		v3 = v15;
	}
	return v2;
}

Object *make_Point(Object *v0, Object *v1)
{
	Object *v2 = __create_object();
	__add_member(v2, "f_getX", *type_Point_getX);
	__add_member(v2, "f_getY", *type_Point_getY);
	__add_member(v2, "f_setX", *type_Point_setX);
	__add_member(v2, "f_setY", *type_Point_setY);
	__add_member(v2, "type", "Point");
	int *v3 =  malloc(sizeof(int));
	*v3 =  7;
	__add_member(v2, "type_ind", v3);
	attr_Point(v2, v0, v1);
	return v2;
}

void attr_Point(Object *v0, Object *v1, Object *v2)
{
	Object *v3 = v1;
	__add_member(v0, "p_x", v3);
	Object *v4 = v2;
	__add_member(v0, "p_y", v4);
}

Object *type_Point_getX(Object *v0)
{
	Object *v1 = __find_member(v0, "p_x");
	return v1;
}

Object *type_Point_getY(Object *v0)
{
	Object *v1 = __find_member(v0, "p_y");
	return v1;
}

Object *type_Point_setX(Object *v0, Object *v1)
{
	Object *v3 = v1;
	__remove_member(v0, "p_x");
	__add_member(v0, "p_x", v3);
	Object *v2 = v3;
	return v2;
}

Object *type_Point_setY(Object *v0, Object *v1)
{
	Object *v3 = v1;
	__remove_member(v0, "p_y");
	__add_member(v0, "p_y", v3);
	Object *v2 = v3;
	return v2;
}

Object *make_PolarPoint(Object *v0, Object *v1)
{
	Object *v2 = __create_object();
	__add_member(v2, "f_getX", *type_Point_getX);
	__add_member(v2, "f_getY", *type_Point_getY);
	__add_member(v2, "f_setX", *type_Point_setX);
	__add_member(v2, "f_setY", *type_Point_setY);
	__add_member(v2, "f_rho", *type_PolarPoint_rho);
	__add_member(v2, "type", "PolarPoint");
	int *v3 =  malloc(sizeof(int));
	*v3 =  8;
	__add_member(v2, "type_ind", v3);
	attr_PolarPoint(v2, v0, v1);
	return v2;
}

void attr_PolarPoint(Object *v0, Object *v1, Object *v2)
{
	Object *v4 = v2;
	Object *v6 = v1;
	Object *v5 = ___builtin_sin(v6);
	Object *v3 = __mul_number(v4, v5);
	Object *v8 = v2;
	Object *v10 = v1;
	Object *v9 = ___builtin_cos(v10);
	Object *v7 = __mul_number(v8, v9);
	attr_Point(v0, v3, v7);
}

Object *type_PolarPoint_rho(Object *v0)
{
	Object *v5 = v0;
	Object *(*v6)(Object *) = __find_member(v5, "f_getX");
	Object *v4 = v6(v5);
	Object *v7 = __make_number(2);
	Object *v3 = __pow_number(v4, v7);
	Object *v10 = v0;
	Object *(*v11)(Object *) = __find_member(v10, "f_getY");
	Object *v9 = v11(v10);
	Object *v12 = __make_number(2);
	Object *v8 = __pow_number(v9, v12);
	Object *v2 = __add_number(v3, v8);
	Object *v1 = ___builtin_sqrt(v2);
	return v1;
}

Object *make_Knight(Object *v0, Object *v1)
{
	Object *v2 = __create_object();
	__add_member(v2, "f_name", *type_Knight_name);
	__add_member(v2, "f_hash", *type_Person_hash);
	__add_member(v2, "type", "Knight");
	int *v3 =  malloc(sizeof(int));
	*v3 =  9;
	__add_member(v2, "type_ind", v3);
	attr_Knight(v2, v0, v1);
	return v2;
}

void attr_Knight(Object *v0, Object *v1, Object *v2)
{
	Object *v3 = v1;
	Object *v4 = v2;
	attr_Person(v0, v3, v4);
}

Object *type_Knight_name(Object *v0)
{
	Object *v2 = __make_string("Sir");
	Object *v4 = __make_string(" ");
	Object *v5 = type_Person_name(v0);
	Object *v3 = __concat_string(v4, v5);
	Object *v1 = __concat_string(v2, v3);
	return v1;
}

Object *make_Person(Object *v0, Object *v1)
{
	Object *v2 = __create_object();
	__add_member(v2, "f_name", *type_Person_name);
	__add_member(v2, "f_hash", *type_Person_hash);
	__add_member(v2, "type", "Person");
	int *v3 =  malloc(sizeof(int));
	*v3 =  10;
	__add_member(v2, "type_ind", v3);
	attr_Person(v2, v0, v1);
	return v2;
}

void attr_Person(Object *v0, Object *v1, Object *v2)
{
	Object *v3 = v1;
	__add_member(v0, "p_firstname", v3);
	Object *v4 = v2;
	__add_member(v0, "p_lastname", v4);
}

Object *type_Person_name(Object *v0)
{
	Object *v2 = __find_member(v0, "p_firstname");
	Object *v4 = __make_string(" ");
	Object *v5 = __find_member(v0, "p_lastname");
	Object *v3 = __concat_string(v4, v5);
	Object *v1 = __concat_string(v2, v3);
	return v1;
}

Object *type_Person_hash(Object *v0)
{
	Object *v1 = __make_number(5);
	return v1;
}

Object *make_Superman()
{
	Object *v0 = __create_object();
	__add_member(v0, "type", "Superman");
	int *v1 =  malloc(sizeof(int));
	*v1 =  11;
	__add_member(v0, "type_ind", v1);
	attr_Superman(v0);
	return v0;
}

void attr_Superman(Object *v0)
{
}

Object *make_Bird()
{
	Object *v0 = __create_object();
	__add_member(v0, "type", "Bird");
	int *v1 =  malloc(sizeof(int));
	*v1 =  12;
	__add_member(v0, "type_ind", v1);
	attr_Bird(v0);
	return v0;
}

void attr_Bird(Object *v0)
{
}

Object *make_Plane()
{
	Object *v0 = __create_object();
	__add_member(v0, "type", "Plane");
	int *v1 =  malloc(sizeof(int));
	*v1 =  13;
	__add_member(v0, "type_ind", v1);
	attr_Plane(v0);
	return v0;
}

void attr_Plane(Object *v0)
{
}

Object *make_A()
{
	Object *v0 = __create_object();
	__add_member(v0, "f_hello", *type_A_hello);
	__add_member(v0, "type", "A");
	int *v1 =  malloc(sizeof(int));
	*v1 =  14;
	__add_member(v0, "type_ind", v1);
	attr_A(v0);
	return v0;
}

void attr_A(Object *v0)
{
}

Object *type_A_hello(Object *v0)
{
	Object *v2 = __make_string("A");
	Object *v1 = ___builtin_print(v2);
	return v1;
}

Object *make_B()
{
	Object *v0 = __create_object();
	__add_member(v0, "f_hello", *type_B_hello);
	__add_member(v0, "type", "B");
	int *v1 =  malloc(sizeof(int));
	*v1 =  15;
	__add_member(v0, "type_ind", v1);
	attr_B(v0);
	return v0;
}

void attr_B(Object *v0)
{
	attr_A(v0);
}

Object *type_B_hello(Object *v0)
{
	Object *v2 = __make_string("B");
	Object *v1 = ___builtin_print(v2);
	return v1;
}

Object *make_C()
{
	Object *v0 = __create_object();
	__add_member(v0, "f_hello", *type_C_hello);
	__add_member(v0, "type", "C");
	int *v1 =  malloc(sizeof(int));
	*v1 =  16;
	__add_member(v0, "type_ind", v1);
	attr_C(v0);
	return v0;
}

void attr_C(Object *v0)
{
	attr_A(v0);
}

Object *type_C_hello(Object *v0)
{
	Object *v2 = __make_string("C");
	Object *v1 = ___builtin_print(v2);
	return v1;
}

int **hierarchy_graph = NULL;

int main()
{
	srand(time(NULL));
	hierarchy_graph = malloc(sizeof(int*) * 17);
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
	hierarchy_graph[4] = malloc(sizeof(int) * 2);
	hierarchy_graph[4][0] = 1;
	hierarchy_graph[4][1] = 0;
	hierarchy_graph[5] = malloc(sizeof(int) * 2);
	hierarchy_graph[5][0] = 1;
	hierarchy_graph[5][1] = 4;
	hierarchy_graph[6] = malloc(sizeof(int) * 2);
	hierarchy_graph[6][0] = 1;
	hierarchy_graph[6][1] = 4;
	hierarchy_graph[7] = malloc(sizeof(int) * 2);
	hierarchy_graph[7][0] = 1;
	hierarchy_graph[7][1] = 0;
	hierarchy_graph[8] = malloc(sizeof(int) * 2);
	hierarchy_graph[8][0] = 1;
	hierarchy_graph[8][1] = 7;
	hierarchy_graph[9] = malloc(sizeof(int) * 2);
	hierarchy_graph[9][0] = 1;
	hierarchy_graph[9][1] = 10;
	hierarchy_graph[10] = malloc(sizeof(int) * 2);
	hierarchy_graph[10][0] = 1;
	hierarchy_graph[10][1] = 0;
	hierarchy_graph[11] = malloc(sizeof(int) * 2);
	hierarchy_graph[11][0] = 1;
	hierarchy_graph[11][1] = 0;
	hierarchy_graph[12] = malloc(sizeof(int) * 2);
	hierarchy_graph[12][0] = 1;
	hierarchy_graph[12][1] = 0;
	hierarchy_graph[13] = malloc(sizeof(int) * 2);
	hierarchy_graph[13][0] = 1;
	hierarchy_graph[13][1] = 0;
	hierarchy_graph[14] = malloc(sizeof(int) * 2);
	hierarchy_graph[14][0] = 1;
	hierarchy_graph[14][1] = 0;
	hierarchy_graph[15] = malloc(sizeof(int) * 2);
	hierarchy_graph[15][0] = 1;
	hierarchy_graph[15][1] = 14;
	hierarchy_graph[16] = malloc(sizeof(int) * 2);
	hierarchy_graph[16][0] = 1;
	hierarchy_graph[16][1] = 14;
	Object *v1 = __make_number(42);
	Object *v3 = __make_number(42);
	Object *v2 = ___builtin_print(v3);
	Object *v9 = __make_number(1);
	Object *v10 = __make_number(2);
	Object *v8 = __add_number(v9, v10);
	Object *v11 = __make_number(3);
	Object *v7 = __pow_number(v8, v11);
	Object *v12 = __make_number(4);
	Object *v6 = __mul_number(v7, v12);
	Object *v13 = __make_number(5);
	Object *v5 = __div_number(v6, v13);
	Object *v4 = ___builtin_print(v5);
	Object *v15 = __make_string("Hello World");
	Object *v14 = ___builtin_print(v15);
	Object *v18 = __make_string("The meaning of life is ");
	Object *v19 = __make_number(42);
	Object *v17 = __concat_string(v18, v19);
	Object *v16 = ___builtin_print(v17);
	Object *v25 = __make_number(2);
	Object *v26 = __make_number(3.141592653589793);
	Object *v24 = __mul_number(v25, v26);
	Object *v23 = ___builtin_sin(v24);
	Object *v27 = __make_number(2);
	Object *v22 = __pow_number(v23, v27);
	Object *v31 = __make_number(3);
	Object *v32 = __make_number(3.141592653589793);
	Object *v30 = __mul_number(v31, v32);
	Object *v34 = __make_number(4);
	Object *v35 = __make_number(64);
	Object *v33 = ___builtin_log(v34, v35);
	Object *v29 = __div_number(v30, v33);
	Object *v28 = ___builtin_cos(v29);
	Object *v21 = __add_number(v22, v28);
	Object *v20 = ___builtin_print(v21);
	Object *v38 = __make_number(42);
	Object *v37 = ___builtin_print(v38);
	Object *v42 = __make_number(3.141592653589793);
	Object *v43 = __make_number(2);
	Object *v41 = __div_number(v42, v43);
	Object *v40 = ___builtin_sin(v41);
	Object *v39 = ___builtin_print(v40);
	Object *v44 = __make_string("Hello World");
	Object *v36 = ___builtin_print(v44);
	Object *v49 = __make_number(3.141592653589793);
	Object *v48 = _tan(v49);
	Object *v50 = __make_number(2);
	Object *v47 = __pow_number(v48, v50);
	Object *v53 = __make_number(3.141592653589793);
	Object *v52 = _cot(v53);
	Object *v54 = __make_number(2);
	Object *v51 = __pow_number(v52, v54);
	Object *v46 = __add_number(v47, v51);
	Object *v45 = ___builtin_print(v46);
	Object *v56 = __make_string("Hello World");
	Object *v57 = v56;
	Object *v58 = v57;
	Object *v55 = ___builtin_print(v58);
	Object *v60 = __make_number(42);
	Object *v61 = v60;
	Object *v62 = __make_string("The meaning of life is");
	Object *v63 = v62;
	Object *v65 = v63;
	Object *v66 = v61;
	Object *v64 = __concat_string(v65, v66);
	Object *v59 = ___builtin_print(v64);
	Object *v68 = __make_number(42);
	Object *v69 = v68;
	Object *v70 = __make_string("The meaning of life is");
	Object *v71 = v70;
	Object *v73 = v71;
	Object *v74 = v69;
	Object *v72 = __concat_string(v73, v74);
	Object *v67 = ___builtin_print(v72);
	Object *v76 = __make_number(42);
	Object *v77 = v76;
	Object *v78 = __make_string("The meaning of life is");
	Object *v79 = v78;
	Object *v81 = v79;
	Object *v82 = v77;
	Object *v80 = __concat_string(v81, v82);
	Object *v75 = ___builtin_print(v80);
	Object *v84 = __make_number(6);
	Object *v85 = v84;
	Object *v87 = v85;
	Object *v88 = __make_number(7);
	Object *v86 = __mul_number(v87, v88);
	Object *v89 = v86;
	Object *v90 = v89;
	Object *v83 = ___builtin_print(v90);
	Object *v92 = __make_number(6);
	Object *v93 = v92;
	Object *v95 = v93;
	Object *v96 = __make_number(7);
	Object *v94 = __mul_number(v95, v96);
	Object *v97 = v94;
	Object *v98 = v97;
	Object *v91 = ___builtin_print(v98);
	Object *v100 = __make_number(5);
	Object *v101 = v100;
	Object *v102 = __make_number(10);
	Object *v103 = v102;
	Object *v104 = __make_number(20);
	Object *v105 = v104;
	Object *v108 = v101;
	Object *v109 = v103;
	Object *v107 = __add_number(v108, v109);
	Object *v106 = ___builtin_print(v107);
	Object *v112 = v103;
	Object *v113 = v105;
	Object *v111 = __mul_number(v112, v113);
	Object *v110 = ___builtin_print(v111);
	Object *v115 = v105;
	Object *v116 = v101;
	Object *v114 = __div_number(v115, v116);
	Object *v99 = ___builtin_print(v114);
	Object *v119 = __make_number(6);
	Object *v120 = v119;
	Object *v121 = v120;
	Object *v122 = __make_number(7);
	Object *v118 = __mul_number(v121, v122);
	Object *v123 = v118;
	Object *v124 = v123;
	Object *v117 = ___builtin_print(v124);
	Object *v127 = __make_number(6);
	Object *v128 = v127;
	Object *v129 = v128;
	Object *v130 = __make_number(7);
	Object *v126 = __mul_number(v129, v130);
	Object *v125 = ___builtin_print(v126);
	Object *v132 = __make_number(20);
	Object *v133 = v132;
	Object *v135 = __make_number(42);
	Object *v136 = v135;
	Object *v137 = v136;
	Object *v134 = ___builtin_print(v137);
	Object *v138 = v133;
	Object *v131 = ___builtin_print(v138);
	Object *v140 = __make_number(7);
	Object *v141 = v140;
	Object *v143 = __make_number(7);
	Object *v144 = __make_number(6);
	Object *v142 = __mul_number(v143, v144);
	Object *v145 = v142;
	Object *v146 = v145;
	Object *v139 = ___builtin_print(v146);
	Object *v148 = __make_number(7);
	Object *v149 = v148;
	Object *v151 = __make_number(7);
	Object *v152 = __make_number(6);
	Object *v150 = __mul_number(v151, v152);
	Object *v153 = v150;
	Object *v154 = v153;
	Object *v147 = ___builtin_print(v154);
	Object *v156 = __make_number(0);
	Object *v157 = v156;
	Object *v159 = v157;
	Object *v158 = ___builtin_print(v159);
	Object *v161 = __make_number(1);
	v157 = v161;
	Object *v160 = v161;
	Object *v162 = v157;
	Object *v155 = ___builtin_print(v162);
	Object *v164 = __make_number(0);
	Object *v165 = v164;
	Object *v167 = __make_number(1);
	v165 = v167;
	Object *v166 = v167;
	Object *v168 = v166;
	Object *v170 = v165;
	Object *v169 = ___builtin_print(v170);
	Object *v171 = v168;
	Object *v163 = ___builtin_print(v171);
	Object *v173 = __make_number(42);
	Object *v174 = v173;
	Object *v172;
	Object *v177 = v174;
	Object *v178 = __make_number(2);
	Object *v176 = __mod_number(v177, v178);
	Object *v179 = __make_number(0);
	Object *v175 = __eq(v176, v179);
	if (__to_bool(v175))
	{
		Object *v181 = __make_string("Even");
		Object *v180 = ___builtin_print(v181);
		v172 = v180;
	}
	else
	{
		Object *v183 = __make_string("odd");
		Object *v182 = ___builtin_print(v183);
		v172 = v182;
	}
	Object *v185 = __make_number(42);
	Object *v186 = v185;
	Object *v187;
	Object *v190 = v186;
	Object *v191 = __make_number(2);
	Object *v189 = __mod_number(v190, v191);
	Object *v192 = __make_number(0);
	Object *v188 = __eq(v189, v192);
	if (__to_bool(v188))
	{
		Object *v193 = __make_string("even");
		v187 = v193;
	}
	else
	{
		Object *v194 = __make_string("odd");
		v187 = v194;
	}
	Object *v184 = ___builtin_print(v187);
	Object *v196 = __make_number(42);
	Object *v197 = v196;
	Object *v195;
	Object *v200 = v197;
	Object *v201 = __make_number(2);
	Object *v199 = __mod_number(v200, v201);
	Object *v202 = __make_number(0);
	Object *v198 = __eq(v199, v202);
	if (__to_bool(v198))
	{
		Object *v205 = v197;
		Object *v204 = ___builtin_print(v205);
		Object *v206 = __make_string("Even");
		Object *v203 = ___builtin_print(v206);
		v195 = v203;
	}
	else
	{
		Object *v208 = __make_string("Odd");
		Object *v207 = ___builtin_print(v208);
		v195 = v207;
	}
	Object *v210 = __make_number(10);
	Object *v211 = v210;
	Object *v209;
	Object *v214 = v211;
	Object *v215 = __make_number(0);
	Object *v213 = __not_bool(__eq(__comp(v214, v215), __make_number(-1)));
	Object *v212 = v213;
	while(__to_bool(v212))
	{
		Object *v218 = v211;
		Object *v217 = ___builtin_print(v218);
		Object *v220 = v211;
		Object *v221 = __make_number(1);
		Object *v219 = __sub_number(v220, v221);
		v211 = v219;
		Object *v216 = v219;
		v209 = v216;
		Object *v223 = v211;
		Object *v224 = __make_number(0);
		Object *v222 = __not_bool(__eq(__comp(v223, v224), __make_number(-1)));
		v212 = v222;
	}
	Object *v227 = __make_number(3);
	Object *v228 = __make_number(4);
	Object *v226 = make_Point(v227, v228);
	Object *v229 = v226;
	Object *v233 = __make_string("x: ");
	Object *v235 = v229;
	Object *(*v236)(Object *) = __find_member(v235, "f_getX");
	Object *v234 = v236(v235);
	Object *v232 = __concat_string(v233, v234);
	Object *v237 = __make_string("; y: ");
	Object *v231 = __concat_string(v232, v237);
	Object *v239 = v229;
	Object *(*v240)(Object *) = __find_member(v239, "f_getY");
	Object *v238 = v240(v239);
	Object *v230 = __concat_string(v231, v238);
	Object *v225 = ___builtin_print(v230);
	Object *v243 = __make_number(3);
	Object *v244 = __make_number(4);
	Object *v242 = make_PolarPoint(v243, v244);
	Object *v245 = v242;
	Object *v247 = __make_string("rho: ");
	Object *v249 = v245;
	Object *(*v250)(Object *) = __find_member(v249, "f_rho");
	Object *v248 = v250(v249);
	Object *v246 = __concat_string(v247, v248);
	Object *v241 = ___builtin_print(v246);
	Object *v253 = __make_string("Phil");
	Object *v254 = __make_string("Collins");
	Object *v252 = make_Knight(v253, v254);
	Object *v255 = v252;
	Object *v257 = v255;
	Object *(*v258)(Object *) = __find_member(v257, "f_name");
	Object *v256 = v258(v257);
	Object *v251 = ___builtin_print(v256);
	Object *v261 = __make_string("Phil");
	Object *v262 = __make_string("Collins");
	Object *v260 = make_Knight(v261, v262);
	Object *v263 = v260;
	Object *v265 = v263;
	Object *(*v266)(Object *) = __find_member(v265, "f_name");
	Object *v264 = v266(v265);
	Object *v259 = ___builtin_print(v264);
	Object *v268 = __make_number(42);
	Object *v269 = v268;
	Object *v270 = v269;
	Object *v267 = ___builtin_print(v270);
	Object *v272 = make_Superman();
	Object *v273 = v272;
	Object *v274;
	Object *v276 = v273;
	int *v277 = __find_member(v276, "type_ind");
	Object *v275 = __make_bool(__search_type(*v277, 12));
	if (__to_bool(v275))
	{
		Object *v278 = __make_string("It's bird!");
		v274 = v278;
	}
	else
	{
		Object *v280 = v273;
		int *v281 = __find_member(v280, "type_ind");
		Object *v279 = __make_bool(__search_type(*v281, 13));
		if (__to_bool(v279))
		{
			Object *v282 = __make_string("It's a plane!");
			v274 = v282;
		}
		else
		{
			Object *v283 = __make_string("No, it's Superman!");
			v274 = v283;
		}
	}
	Object *v271 = ___builtin_print(v274);
	Object *v285 = __make_number(42);
	Object *v286 = v285;
	Object *v287 = v286;
	Object *v284 = ___builtin_print(v287);
	Object *v292 = __make_string("Total");
	Object *v291 = ___builtin_print(v292);
	Object *v290 = __make_number(5);
	Object *v293 = __make_number(6);
	Object *v289 = __add_number(v290, v293);
	Object *v294 = v289;
	Object *v295 = v294;
	Object *v288 = ___builtin_print(v295);
	Object *v297;
	Object *v299 = ___builtin_rand();
	Object *v300 = __make_number(0.5);
	Object *v298 = __eq(__comp(v299, v300), __make_number(-1));
	if (__to_bool(v298))
	{
		Object *v301 = make_B();
		v297 = v301;
	}
	else
	{
		Object *v302 = make_C();
		v297 = v302;
	}
	Object *v303 = v297;
	Object *v296;
	Object *v305 = v303;
	int *v306 = __find_member(v305, "type_ind");
	Object *v304 = __make_bool(__search_type(*v306, 15));
	if (__to_bool(v304))
	{
		Object *v308 = v303;
		Object *v309 = v308;
		Object *v310 = v309;
		Object *(*v311)(Object *) = __find_member(v310, "f_hello");
		Object *v307 = v311(v310);
		v296 = v307;
	}
	else
	{
		Object *v313 = __make_string("x cannot be downcasted to B");
		Object *v312 = ___builtin_print(v313);
		v296 = v312;
	}
	Object *v315 = __make_string("sato");
	Object *v316 = __make_string("balto");
	Object *v317 = __make_number(7);
	Object *v314 = make_Dog(v315, v316, v317);
	Object *v318 = v314;
	Object *v320 = __make_string("siames");
	Object *v321 = __make_string("Lucas");
	Object *v322 = __make_number(4);
	Object *v319 = make_Cat(v320, v321, v322);
	Object *v323 = v319;
	Object *v326 = v323;
	Object *(*v327)(Object *) = __find_member(v326, "f_maulla");
	Object *v325 = v327(v326);
	Object *v324 = ___builtin_print(v325);
	Object *v329 = v318;
	Object *(*v330)(Object *, Object *, Object *) = __find_member(v329, "f_ladra");
	Object *v331 = __make_string("alex");
	Object *v332 = __make_number(22);
	Object *v328 = v330(v329, v331, v332);
	Object *v0 = ___builtin_print(v328);
}