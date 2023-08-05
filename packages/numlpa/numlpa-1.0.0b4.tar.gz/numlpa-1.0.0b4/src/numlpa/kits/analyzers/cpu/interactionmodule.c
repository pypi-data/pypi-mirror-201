#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdio.h>
#include <math.h>

/**
 * Compute the sum of the interaction terms between dislocation i and the rest of the dislocations.
 *
 * @param i Index of the dislocation.
 * @param d_x Dislocation x-coordinates.
 * @param d_y Dislocation y-coordinates.
 * @param senses Dislocation Burgers vector senses.
 * @param number Number of dislocations.
 * @param step Step size.
 * @param count_equal Number of dislocations of equal sign per radius slice.
 * @param count_opposed Number of dislocations of opposite sign per radius slice.
 * @param e_i Interaction energy term.
 */
void sum_term(
    unsigned long long i,
    double* d_x,
    double* d_y,
    signed char* senses,
    unsigned long long number,
    double* step,
    unsigned long long* count_equal,
    unsigned long long* count_opposed,
    double* e_i
)
{
    double x_i = d_x[i];
    double y_i = d_y[i];
    double s_i = senses[i];
    double r_x;
    double r_y;
    double r;
    size_t k;
    signed char dot;
    *e_i = 0;
    for(size_t j=0; j<number; j++)
    {
        if (i!=j)
        {
            dot = senses[j] * s_i;
            r_x = d_x[j] - x_i;
            r_y = d_y[j] - y_i;
            r = sqrt(r_x*r_x + r_y*r_y);
            *e_i -= dot * log(r);
            k = (size_t)(r / *step);
            if (dot > 0)
            {
                count_equal[k]++;
            }
            else
            {
                count_opposed[k]++;
            }
        }
    }
}

/**
 * Python sum_term wrapper function.
 *
 * @param PyObject
 * @param args
 * @return the sum term: sum_ij sign(b_i*b_j) * ln(1/d_ij).
 */
static PyObject *py_sum_term(
    PyObject *self,
    PyObject *args
)
{
    unsigned long long i;
    PyObject *obj_d_x;
    Py_buffer buf_d_x;
    PyObject *obj_d_y;
    Py_buffer buf_d_y;
    PyObject *obj_senses;
    Py_buffer buf_senses;
    double step;
    PyObject *obj_count_equal;
    Py_buffer buf_count_equal;
    PyObject *obj_count_opposed;
    Py_buffer buf_count_opposed;
    double e_i;
    if (!PyArg_ParseTuple(args, "KOOOdOO", &i, &obj_d_x, &obj_d_y, &obj_senses, &step, &obj_count_equal, &obj_count_opposed))
    {
        return NULL;
    }
    if (PyObject_GetBuffer(obj_d_x, &buf_d_x, PyBUF_ANY_CONTIGUOUS | PyBUF_FORMAT) == -1)
    {
        return NULL;
    }
    if (PyObject_GetBuffer(obj_d_y, &buf_d_y, PyBUF_ANY_CONTIGUOUS | PyBUF_FORMAT) == -1)
    {
        return NULL;
    }
    if (PyObject_GetBuffer(obj_senses, &buf_senses, PyBUF_ANY_CONTIGUOUS | PyBUF_FORMAT) == -1)
    {
        return NULL;
    }
    if (PyObject_GetBuffer(obj_count_equal, &buf_count_equal, PyBUF_ANY_CONTIGUOUS | PyBUF_FORMAT) == -1)
    {
        return NULL;
    }
    if (PyObject_GetBuffer(obj_count_opposed, &buf_count_opposed, PyBUF_ANY_CONTIGUOUS | PyBUF_FORMAT) == -1)
    {
        return NULL;
    }
    sum_term(i, buf_d_x.buf, buf_d_y.buf, buf_senses.buf, buf_senses.shape[0], &step, buf_count_equal.buf, buf_count_opposed.buf, &e_i);
    return Py_BuildValue("d", e_i);
}

static PyMethodDef InteractionModule[] = {
    {
        "sum_term",
        py_sum_term,
        METH_VARARGS,
        "Compute the sum of interaction terms for one dislocation."
    },
    {
        NULL,
        NULL,
        0,
        NULL
    }
};

static struct PyModuleDef interactionmodule = {
    PyModuleDef_HEAD_INIT,
    "interaction", // module name
    NULL,  // module documentation
    -1,
    InteractionModule
};

PyMODINIT_FUNC PyInit_interaction(void)
{
    return PyModule_Create(&interactionmodule);
}
