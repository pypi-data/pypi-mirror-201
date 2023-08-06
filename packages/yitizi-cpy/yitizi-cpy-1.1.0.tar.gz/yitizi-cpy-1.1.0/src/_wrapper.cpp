#include "yitizi.hpp"
#include <Python.h>

extern "C" {

static int yitizi_new_yitizi_map(PyObject *module) {
  string yitizi_data_file;
  PyObject *py_file = PyObject_GetAttrString(module, "__file__");
  PyObject *py_pathlib = PyImport_ImportModule("pathlib");
  PyObject *py_pathlib_Path = PyObject_GetAttrString(py_pathlib, "Path");
  PyObject *py_path =
      PyObject_CallFunctionObjArgs(py_pathlib_Path, py_file, NULL);
  PyObject *py_parent = PyObject_GetAttrString(py_path, "parent");
  PyObject *py_yitizi_data_file_path = PyObject_CallMethodObjArgs(
      py_parent, PyUnicode_FromString("joinpath"),
      PyUnicode_FromString("yitizi/yitizi.tsv"), NULL);
  PyObject *py_yitizi_data_file_str = PyObject_CallMethodObjArgs(
      py_yitizi_data_file_path, PyUnicode_FromString("__str__"), NULL);
  yitizi_data_file = PyUnicode_AsUTF8(py_yitizi_data_file_str);
  Py_DECREF(py_file);
  Py_DECREF(py_pathlib);
  Py_DECREF(py_pathlib_Path);
  Py_DECREF(py_path);
  Py_DECREF(py_parent);
  Py_DECREF(py_yitizi_data_file_path);
  Py_DECREF(py_yitizi_data_file_str);

  YitiziMap *yitizi_map = new YitiziMap(yitizi_data_file);
  PyObject *py_yitizi_map =
      PyCapsule_New((void *)yitizi_map, "yitizi_map", NULL);

  PyObject_SetAttrString(module, "_map", py_yitizi_map);
  return 0;
}

static PyObject *yitizi_get(PyObject *self, PyObject *args, PyObject *kwargs) {
  wstring_convert<codecvt_utf8<char32_t>, char32_t> conv;

  char *arg_str;
  static char *kwlist[] = {(char *)"字", NULL};
  if (!PyArg_ParseTupleAndKeywords(args, kwargs, "s", kwlist, &arg_str))
    return NULL;
  char32_t c;
  u32string arg_u32str = conv.from_bytes(arg_str);
  if (arg_u32str.size() != 1) {
    PyErr_Format(PyExc_ValueError, "'%s' is not a single character.", arg_str);
    return NULL;
  }
  c = arg_u32str[0];

  PyObject *py_yitizi_map_capsule = PyObject_GetAttrString(self, "_map");
  YitiziMap *yitizi_map =
      (YitiziMap *)PyCapsule_GetPointer(py_yitizi_map_capsule, "yitizi_map");
  Py_DECREF(py_yitizi_map_capsule);
  if (yitizi_map == NULL) {
    return NULL;
  }

  vector<char32_t> yitizi_list = yitizi_map->get(c);
  PyObject *py_yitizi_set = PySet_New(NULL);
  for (size_t i = 0; i < yitizi_list.size(); i++) {
    string yitizi_str = conv.to_bytes(yitizi_list[i]);
    PyObject *py_yitizi = PyUnicode_FromString(yitizi_str.c_str());
    PySet_Add(py_yitizi_set, py_yitizi);
    Py_DECREF(py_yitizi);
  }
  PyObject *py_yitizi_frozenset = PyFrozenSet_New(py_yitizi_set);
  Py_DECREF(py_yitizi_set);
  return py_yitizi_frozenset;
}

static PyMethodDef yitizi_methods[] = {
    {"get", (PyCFunction)yitizi_get, METH_VARARGS | METH_KEYWORDS,
     "Given one Sinograph, outputs all its variants."},
    {NULL, NULL, 0, NULL},
};

static PyModuleDef_Slot yitizi_slots[] = {
    {Py_mod_exec, (void *)yitizi_new_yitizi_map},
    {0, NULL},
};

static PyModuleDef yitizi_module = [] {
  PyModuleDef def;
  def.m_base = PyModuleDef_HEAD_INIT;
  def.m_name = "__init__";
  def.m_doc = "Given one Sinograph, outputs all its variants. nk2028/yitizi "
              "rewritten in C++";
  def.m_methods = yitizi_methods;
  def.m_slots = yitizi_slots;
  return def;
}();

PyMODINIT_FUNC PyInit_yitizi(void) { return PyModuleDef_Init(&yitizi_module); }
}
