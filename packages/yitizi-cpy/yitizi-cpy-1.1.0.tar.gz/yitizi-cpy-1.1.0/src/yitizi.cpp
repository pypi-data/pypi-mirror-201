#include "yitizi.hpp"

YitiziMap::YitiziMap(string yitizi_data_file) {
  ifstream yitizi_dict(yitizi_data_file);
  string line;
  wstring_convert<codecvt_utf8<char32_t>, char32_t> conv;

  while (getline(yitizi_dict, line)) {
    u32string line_u32 = conv.from_bytes(line);
    char32_t first_char = line_u32[0];
    vector<char32_t> yitizi_list;
    for (size_t i = 2; i < line_u32.size(); i++) {
      if (line_u32[i] > 0x0020)
        yitizi_list.push_back(line_u32[i]);
    }
    _map[first_char] = yitizi_list;
  }
}
vector<char32_t> YitiziMap::get(char32_t c) {
  if (_map.find(c) == _map.end()) {
    return vector<char32_t>();
  } else {
    return _map[c];
  }
}

YitiziMap *new_yitizi_map(char *yitizi_data_file) {
  return new YitiziMap(yitizi_data_file);
}
void delete_yitizi_map(YitiziMap *yitizi_map) { delete yitizi_map; }
PyObject *get_yitizi(YitiziMap *yitizi_map, char32_t c) {
  vector<char32_t> yitizi_list = yitizi_map->get(c);

  PyGILState_STATE gstate = PyGILState_Ensure();
  PyObject *py_yitizi_list = PyList_New(yitizi_list.size());
  for (size_t i = 0; i < yitizi_list.size(); i++) {
    PyList_SetItem(py_yitizi_list, i, PyLong_FromLong(yitizi_list[i]));
  }
  PyGILState_Release(gstate);

  return py_yitizi_list;
}
