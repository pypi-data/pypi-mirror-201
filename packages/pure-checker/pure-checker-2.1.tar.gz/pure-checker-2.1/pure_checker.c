#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "include/pure.h"

static PyObject *pure_checker_pure_zip(PyObject *self, PyObject *args)
{
    uint8_t* *buffer;
    Py_ssize_t *size;
    uint64_t *flags;
    if (!PyArg_ParseTuple(args, "s#|K", &buffer, &size, &flags))
    {
        return NULL;
    }
    return Py_BuildValue("i", pure_zip(buffer, size, flags));
}

static PyObject *pure_checker_pure_zip_bomb(PyObject *self, PyObject *args)
{
    int *error = NULL;
    if (!PyArg_ParseTuple(args, "i", &error))
    {
        return NULL;
    }

    return PyBool_FromLong(pure_zip_bomb(error));
}

static PyObject *pure_checker_pure_error_code(PyObject *self, PyObject *args){
    int *error = NULL;
    if (!PyArg_ParseTuple(args, "i", &error))
    {
        return NULL;
    }

    return Py_BuildValue("s", pure_error_code(error));
}

static PyObject *pure_checker_pure_error_string(PyObject *self, PyObject *args){
    int *error = NULL;
    if (!PyArg_ParseTuple(args, "i", &error))
    {
        return NULL;
    }

    return Py_BuildValue("s", pure_error_string(error));
}

static PyMethodDef pure_checker_methods[] = {
    {"pure_zip", pure_checker_pure_zip, METH_VARARGS, "Returns a non-zero error return code, or a zero return code if the zip file is clean and has no file format anomalies. A buffer instead of a path is passed to pure_zip() for portability, for reduced surface area for bugs, and to avoid forcing unnecessary IO if file contents are already in memory."},
    {"pure_zip_bomb", pure_checker_pure_zip_bomb, METH_VARARGS, "Returns 1 if the error return code indicates a zip bomb, otherwise 0."},
    {"pure_error_code", pure_checker_pure_error_code, METH_VARARGS, "Returns the constant name of the error return code."},
    {"pure_error_string", pure_checker_pure_error_string, METH_VARARGS, "Returns the error message string corresponding the error return code."},
    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef pure_checker_module = {
    PyModuleDef_HEAD_INIT,
    "pure-checker",
    "A static analysis file format checker.",
    -1,
    pure_checker_methods
};

PyMODINIT_FUNC PyInit_pure_checker(void) {
    return PyModule_Create(&pure_checker_module);
}