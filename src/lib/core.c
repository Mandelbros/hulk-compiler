#include "core.h"

Object *__create_object()
{
    Object *dict = malloc(sizeof(Object));
    dict->head = NULL;
    return dict;
}

void __add_member(Object *dict, char *key, void *value)
{
    Member *new_member = malloc(sizeof(Member));
    new_member->key = strdup(key);
    new_member->value = value;
    new_member->next = dict->head;
    dict->head = new_member;
}

void *__find_member(Object *dict, char *key)
{
    Member *current = dict->head;
    while (current != NULL)
    {
        if (strcmp(current->key, key) == 0)
        {
            return current->value;
        }
        current = current->next;
    }
    return NULL;
}

void __remove_member(Object *dict, char *key)
{
    Member *current = dict->head;
    Member *prev = NULL;
    while (current != NULL)
    {
        if (strcmp(current->key, key) == 0)
        {
            if (prev == NULL)
            {
                dict->head = current->next;
            }
            else
            {
                prev->next = current->next;
            }
            free(current->key);
            free(current);
            return;
        }
        prev = current;
        current = current->next;
    }
}

void __free_object(Object *dict)
{
    Member *current = dict->head;
    Member *next;
    while (current != NULL)
    {
        next = current->next;
        free(current->key);
        free(current);
        current = next;
    }
    free(dict);
}

// #######################################################################

Object *type_object_eq(Object *t1, Object *t2)
{
    return __make_bool(t1 == t2);
}

Object *type_object_to_string(Object *t)
{
    char *type = __find_member(t, "type");

    return __make_string(type);
}

// String

Object *__make_string(char *value)
{
    Object *s = __create_object();
    int *len = malloc(sizeof(int)); 
    int *type_ind = malloc(sizeof(int));

    *len = strlen(value); 
    *type_ind = 1;

    __add_member(s, "type", "String");
    __add_member(s, "value", value);
    __add_member(s, "len", len); 
    __add_member(s, "type_ind", type_ind);
    __add_member(s, "f_to_string", *__to_string_string);

    return s;
}

Object *__to_string_string(Object *string)
{
    return string;
}

Object *__concat_string(Object *string1, Object *string2)               //cucu
{
    Object *(*to_string1)(Object *) = __find_member(string1, "f_to_string");
    Object *(*to_string2)(Object *) = __find_member(string2, "f_to_string");

    string1 = to_string1(string1);
    string2 = to_string2(string2);

    int *len1 = __find_member(string1, "len");
    int *len2 = __find_member(string2, "len");

    char *value1 = __find_member(string1, "value");
    char *value2 = __find_member(string2, "value");

    char *aux = malloc(sizeof(char) * (*len1 + *len2 + 1));     // xq +1 wdf
    strcpy(aux, value1);
    strcat(aux, value2);
    return __make_string(aux);
}

// Number

Object *__make_number(double n)
{
    Object *t = __create_object();

    double *value = malloc(sizeof(double));
    *value = n;
    int *type_ind = malloc(sizeof(int));
    *type_ind = 2;

    __add_member(t, "type", "Number");
    __add_member(t, "value", value);
    __add_member(t, "type_ind", type_ind);

    __add_member(t, "f_comp", *__comp_number);
    __add_member(t, "f_eq", *__eq_number);
    __add_member(t, "f_to_string", *__to_string_number);
}

Object *__eq_number(Object *obj1, Object *obj2)
{
    return __make_bool(__to_double(obj1) == __to_double(obj2));         //comparar doubles :skull: eps
}

Object *__comp_number(Object *obj1, Object *obj2)
{
    double val1 = __to_double(obj1);
    double val2 = __to_double(obj2);

    if (val1 > val2)
        return __make_number(1);
    if (val1 == val2)
        return __make_number(0);

    return __make_number(-1);
}

Object *__to_string_number(Object *n)
{
    double *value = __find_member(n, "value");

    char *str = malloc(1024);
    sprintf(str, "%f", *value);     //qejesto
    return __make_string(str);
}

double __to_double(Object *t)
{
    double *value = __find_member(t, "value");
    return *value;
}

Object *__copy_number(Object *t)
{
    return __make_number(__to_double(t));
}

Object *__add_number(Object *obj1, Object *obj2)
{
    double val1 = __to_double(obj1);
    double val2 = __to_double(obj2);

    return __make_number(val1 + val2);
}

Object *__sub_number(Object *obj1, Object *obj2)
{
    double val1 = __to_double(obj1);
    double val2 = __to_double(obj2);

    return __make_number(val1 - val2);
}
Object *__mul_number(Object *obj1, Object *obj2)
{
    double val1 = __to_double(obj1);
    double val2 = __to_double(obj2);

    return __make_number(val1 * val2);
}

Object *__div_number(Object *obj1, Object *obj2)
{
    double val1 = __to_double(obj1);
    double val2 = __to_double(obj2);

    return __make_number(val1 / val2);
}

Object *__pow_number(Object *obj1, Object *obj2)
{
    double val1 = __to_double(obj1);
    double val2 = __to_double(obj2);

    return __make_number(pow(val1, val2));
}

Object *__mod_number(Object *obj1, Object *obj2)
{
    double val1 = __to_double(obj1);
    double val2 = __to_double(obj2);

    return __make_number(fmod(val1, val2));
}

// bool

Object *__make_bool(bool n)
{
    Object *t = __create_object();
    bool *value = malloc(sizeof(int));
    *value = n;
    int *type_ind = malloc(sizeof(int));
    *type_ind = 3;

    __add_member(t, "type", "Boolean");
    __add_member(t, "value", value);
    __add_member(t, "type_ind", type_ind);

    __add_member(t, "f_eq", *__eq_bool);
    __add_member(t, "f_to_string", *__to_string_bool);
}

Object *__eq_bool(Object *obj1, Object *obj2)
{
    return __make_bool(__to_bool(obj1) == __to_bool(obj2));
}

Object *__to_string_bool(Object *obj)
{
    bool bool_rpr = __to_bool(obj);

    if (bool_rpr == 1)
        return __make_string("True");
    else
        return __make_string("False");
}

bool __to_bool(Object *obj)
{
    bool *value = __find_member(obj, "value");
    return *value;
}

Object *__copy_bool(Object *obj)
{
    return __make_bool(__to_bool(obj));
}

Object *__and_bool(Object *obj1, Object *obj2)
{
    return __make_bool(__to_bool(obj1) && __to_bool(obj2));
}

Object *__or_bool(Object *obj1, Object *obj2)
{
    return __make_bool(__to_bool(obj1) || __to_bool(obj2));
}

Object *__not_bool(Object *obj)
{
    return __make_bool(!__to_bool(obj));
}

/////////////////////////////////////////////////////////////////////////////////////////

Object *__eq(Object *obj1, Object *obj2)
{
    Object *(*eq)(Object *, Object *) = __find_member(obj1, "f_eq");

    return eq(obj1, obj2);
}

Object *__comp(Object *obj1, Object *obj2)
{
    Object *(*comp)(Object *, Object *) = __find_member(obj1, "f_comp");

    return comp(obj1, obj2);
}

///////////////////////////////////////////////////////////////////////////////////////////

Object *___builtin_print(Object *t)             //annadir el exp!!!!!!
{
    Object *(*to_string)(Object *) = __find_member(t, "f_to_string");
    Object *s = to_string(t);

    char *value = __find_member(s, "value");
    printf("%s\n", value);
    fflush(stdout);

    return t;
}
 
Object *___builtin_sin(Object *obj)
{
    double *val1 = __find_member(obj, "value");

    return __make_number(sin(*val1));
}

Object *___builtin_cos(Object *obj)
{
    double *val1 = __find_member(obj, "value");

    return __make_number(cos(*val1));
}

Object *___builtin_sqrt(Object *obj)
{
    double *val1 = __find_member(obj, "value");

    return __make_number(sqrt(*val1));
}


Object *___builtin_log(Object *obj1, Object *obj2)
{
    double *val1 = __find_member(obj1, "value");
    double *val2 = __find_member(obj2, "value");

    return __make_number(log10(*val1) / log10(*val2));
}

Object *___builtin_rand()
{
    double random_value = (double)rand() / (double)RAND_MAX;
    return __make_number(random_value); 
}

Object *___builtin_exp(Object *obj)
{
    double *val1 = __find_member(obj, "value");

    return __make_number(exp(*val1));
}

/////////////////////////////////////////////////////////////////////////

int __search_type(int curr, int target)
{
    if (curr == target)
        return 1;
 
    int mk = 0;

    for (int i = 1 ; i <= hierarchy_graph[curr][0] ; i++)
    {
        if(__search_type(hierarchy_graph[curr][i], target)) mk = 1;
    }

    return mk;
}

/////////////////////////////////////////////////////////////////////////

Object *__next_range(Object *r)
{
    double *curr = (double *)__find_member(r, "curr_ind");

    double *end = __find_member(r, "end");

    if (*curr + 1 == *end)
        return __make_bool(0);

    *curr = *curr + 1;

    return __make_bool(1);
}

Object *__current_range(Object *r)
{
    double *curr = __find_member(r, "curr_ind");

    return __make_number(*curr);
}
 

Object *___builtin_range(Object *obj1, Object *obj2)
{
    double *val1 = __find_member(obj1, "value");
    double *val2 = __find_member(obj2, "value");
    double *curr = malloc(sizeof(double));
    *curr = *val1 - 1;

    Object *range = __create_object();
    __add_member(range, "start", val1);
    __add_member(range, "end", val2); 
    __add_member(range, "f_current", *__current_range);
    __add_member(range, "f_next", *__next_range);
    __add_member(range, "curr_ind", curr);
}
