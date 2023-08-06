import os
import sysconfig
from distutils.command.build_ext import build_ext as _build_ext

from setuptools import Extension, setup

extra_compile_args = (sysconfig.get_config_var("CFLAGS") or "").split()
extra_compile_args += ["-std=c++11", "-O3", "-Wall", "-Wextra"]
os.environ["CFLAGS"] = " ".join(extra_compile_args)


class build_ext(_build_ext):
    def build_extension(self, ext):
        self._ctypes = isinstance(ext, Extension)
        return super().build_extension(ext)

    def get_export_symbols(self, ext):
        if self._ctypes:
            return ext.export_symbols
        return super().get_export_symbols(ext)

    def get_ext_filename(self, ext_name):
        if self._ctypes:
            return f"{ext_name}.so"
        return super().get_ext_filename(ext_name)


yitizi_module = Extension(
    name="yitizi",
    sources=["src/yitizi/yitizi.cpp"],
)

setup(
    ext_modules=[
        Extension(
            name="yitizi._lib",
            sources=["src/yitizi/yitizi.cpp"],
        ),
    ],
    cmdclass={"build_ext": build_ext},
)
