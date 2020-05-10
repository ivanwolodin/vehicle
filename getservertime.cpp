#define PY_SSIZE_T_CLEAN

#include <Python.h>
#include <iostream>
#include <ctime>  
#include <iomanip>
#include <sstream>



static PyObject* uniqueCombinations(PyObject* self)
{
    return Py_BuildValue("s", "uniqueCombinations() return value (is of type 'string')");
}


static PyObject* getServerTime(PyObject* self)
{
	auto t = std::time(nullptr);
    auto tm = *std::localtime(&t);

    std::stringstream oss;
    oss << std::put_time(&tm, "%d-%m-%Y %H-%M-%S");
    auto strr = oss.str();
	return Py_BuildValue("s", strr.c_str());
}



static char uniqueCombinations_docs[] =
    "usage: uniqueCombinations(lstSortableItems, comboSize)\n";


static char getServerTime_docs[] =
    "usage: getServerTime(lstSortableItems, comboSize)\n";	
	

static PyMethodDef module_methods[] = {
    {"uniqueCombinations", (PyCFunction) uniqueCombinations,
     METH_NOARGS, uniqueCombinations_docs},
	{"getServerTime", (PyCFunction) getServerTime,
     METH_NOARGS, getServerTime_docs}, 
    {NULL}
};


static struct PyModuleDef Combinations =
{
    PyModuleDef_HEAD_INIT,
    "Combinations", /* name of module */
    "usage: Combinations.uniqueCombinations(lstSortableItems, comboSize)\n", /* module documentation, may be NULL */
    -1,   /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    module_methods
};

PyMODINIT_FUNC PyInit_Combinations(void)
{
    return PyModule_Create(&Combinations);
}