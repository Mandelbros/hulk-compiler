#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>

#define bool int

typedef struct Member
{
    char *key;
    void *value;
    struct Member *next;
} Member;

typedef struct Object
{
    Member *head;
} Object;

Object *__create_object();
void __add_member(Object *dict, char *key, void *value);
void *__find_member(Object *dict, char *key);
void __remove_member(Object *dict, char *key);
void __free_object(Object *dict);

Object *type_object_eq(Object *obj1, Object *obj2);
Object *type_object_to_string(Object *obj);

Object *__make_string(char *value);
Object *__length_string(Object *string);
Object *__get_string(Object *str, Object *index);
Object *__eq_string(Object *str1, Object *str2);
Object *__comp_string(Object *str1, Object *str2);
Object *__concat_string(Object *str1, Object *str2);  
Object *__to_string_string(Object *str);

Object *__make_number(double obj);
Object *__eq_number(Object *obj1, Object *obj2);
Object *__comp_number(Object *obj1, Object *obj2);
Object *__add_number(Object *obj1, Object *obj2);
Object *__sub_number(Object *obj1, Object *obj2);
Object *__mul_number(Object *obj1, Object *obj2);
Object *__div_number(Object *obj1, Object *obj2);
Object *__pow_number(Object *obj1, Object *obj2);
Object *__mod_number(Object *obj1, Object *obj2);
Object *__to_string_number(Object *obj);

Object *__make_bool(bool obj);
Object *__eq_bool(Object *obj1, Object *obj2);
Object *__to_string_bool(Object *obj);
Object *__and_bool(Object *obj1, Object *obj2);
Object *__or_bool(Object *obj1, Object *obj2);
Object *__not_bool(Object *obj);

double __to_double(Object *obj);
bool __to_bool(Object *obj);
Object *__copy_number(Object *obj);
Object *__copy_bool(Object *obj);
Object *__eq(Object *obj1, Object *obj2);
Object *__comp(Object *obj1, Object *obj2);

Object *___builtin_print(Object *obj);
Object *___builtin_sin(Object *obj);
Object *___builtin_cos(Object *obj);
Object *___builtin_sqrt(Object *obj);
Object *___builtin_log(Object *obj1, Object *obj2);
Object *___builtin_rand();

extern int **hierarchy_graph;
int __search_type(int curr, int target);