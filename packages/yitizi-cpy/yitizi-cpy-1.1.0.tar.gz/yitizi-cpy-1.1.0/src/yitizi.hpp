#include "Python.h"
#include <codecvt>
#include <fstream>
#include <iostream>
#include <locale>
#include <string>
#include <unordered_map>
#include <vector>

using namespace std;

#if defined(_MSC_VER)
#define YITIZI_API __declspec(dllexport)
#elif defined(__GNUC__)
#define YITIZI_API __attribute__((visibility("default")))
#else
#define YITIZI_API
#pragma warning Unknown dynamic link import / export semantics.
#endif

class YitiziMap {
public:
  unordered_map<char32_t, vector<char32_t>> _map;
  YitiziMap(string yitizi_data_file);
  vector<char32_t> get(char32_t c);
};

extern "C" {
YITIZI_API YitiziMap *new_yitizi_map(char *yitizi_data_file);
YITIZI_API void delete_yitizi_map(YitiziMap *yitizi_map);
YITIZI_API PyObject *get_yitizi(YitiziMap *yitizi_map, char32_t c);
}
