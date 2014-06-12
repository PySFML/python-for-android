"""distutils.androidcompiler

Contains the AndroidCompiler class, a subclass of CCompiler that [..]
according the following arguments:
  * the target architecture
  * the compiler version
  * the STL version to link against
  * the level of the Android API to use
"""

__revision__ = "$Id$"

import os, sys, re
from distutils.ccompiler import CCompiler

class AndroidCompiler(CCompiler):

    compiler_type = 'android'

    executables = {'preprocessor' : None,
                   'compiler'     : ["cc"],
                   'compiler_so'  : ["cc"],
                   'compiler_cxx' : ["cc"],
                   'linker_so'    : ["cc", "-shared"],
                   'linker_exe'   : ["cc"],
                   'archiver'     : ["ar", "-cr"],
                   'ranlib'       : None,
                  }

    src_extensions = [".c",".C",".cc",".cxx",".cpp"]
    obj_extension = ".o"
    static_lib_extension = ".a"
    shared_lib_extension = ".so"
    static_lib_format = shared_lib_format = dylib_lib_format = "lib%s%s"

    def initialize(self, android_ndk, arch, version, stl, api_level):
        self.android_ndk = android_ndk
        self.arch = arch
        self.version = version
        self.stl = stl
        self.api_level = api_level

    def _compile(self, obj, src, ext, cc_args, extra_postargs, pp_opts):
        self.spawn([self.android_ndk + "/toolchains/arm-linux-androideabi-4.8/prebuilt/linux-x86_64/bin/arm-linux-androideabi-gcc"] + cc_args + [src, '-o', obj] + extra_postargs)
        print("AndroidCompiler: compiling! =)")

    def link(self, target_desc, objects, output_filename, output_dir=None,
             libraries=None, library_dirs=None, runtime_library_dirs=None,
             export_symbols=None, debug=0, extra_preargs=None,
             extra_postargs=None, build_temp=None, target_lang=None):
        print("AndroidCompiler: linking!")
