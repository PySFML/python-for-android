from distutils.core import setup, Extension

setup(name='foo',
      version='1.0',
      py_modules=['foobar'],
      ext_modules=[Extension('barfoo', ['barfoo.c'])],
      )
