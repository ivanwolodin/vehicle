from distutils.core import setup, Extension
#setup(name='Combinations', version='1.0',  \
#      ext_modules=[Extension('Combinations', ['hello.c'])])
setup(name='Combinations', version='1.0',  \
      ext_modules=[Extension('Combinations', ['getservertime.cpp'])])