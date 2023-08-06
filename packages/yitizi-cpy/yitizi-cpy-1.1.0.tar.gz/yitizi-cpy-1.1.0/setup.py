import os
import sysconfig

from setuptools import Extension, setup

extra_compile_args = (sysconfig.get_config_var("CFLAGS") or "").split()
extra_compile_args += ["-std=c++11", "-O3", "-Wall", "-Wextra"]
os.environ["CFLAGS"] = " ".join(extra_compile_args)

yitizi_module = Extension(
    name="yitizi",
    sources=["src/_wrapper.cpp", "src/yitizi.cpp"],
)

setup(
    ext_modules=[yitizi_module],
)
