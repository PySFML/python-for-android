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
from types import StringType, NoneType

from distutils.ccompiler import CCompiler, gen_lib_options

class AndroidCompiler(CCompiler):

    compiler_type = 'android'

    executables = {'preprocessor' : None,
                   'compiler'     : ["g++"],
                   'compiler_so'  : ["g++"],
                   'compiler_cxx' : ["g++"],
                   'linker_so'    : ["g++", "-shared"],
                   'linker_exe'   : ["g++"],
                   'archiver'     : ["ar", "-cr"],
                   'ranlib'       : None,
                  }

    src_extensions = [".c",".C",".cc",".cxx",".cpp"]
    obj_extension = ".o"
    static_lib_extension = ".a"
    shared_lib_extension = ".so"
    static_lib_format = shared_lib_format = dylib_lib_format = "lib%s%s"

    def initialize(self, android_ndk, arch, version, stl, api_level):
		
        # Define the compiler name and codename, the architecture name
        if arch in ['armeabi', 'armeabi-v7a']:
            compiler_name = "arm-linux-androideabi"
            compiler_codename = "arm-linux-androideabi"
            architecture_name = "arm"
        elif arch == "x86":
            compiler_name = "i686-linux-android"
            compiler_codename = "x86"
            architecture_name = "x86"
        elif arch == "mips":
            compiler_name = "mipsel-linux-android"
            compiler_codename = "mipsel-linux-android"
            architecture_name = "mips"

        # Define the STL implementation codename
        if stl == "system":
            stl_codename = "system"
        elif stl == "gabi++":
            stl_codename = "gabi++"
        elif stl == "stlport":
            stl_codename = "stlport"
        elif stl == "gnustl":
            stl_codename = "gnu-libstdc++"
        elif stl == "c++":
            stl_codename = "llvm-libc++"

        # We need to know if the user uses a 32-bit or 64-bit version of 
        # the Android NDK in order to determine the platform code name to
        # to use. The only way is by checking if a file exists.
        if sys.platform == "linux2":
            platform_codename = "linux-x86"
            if not os.path.isdir(android_ndk + "/toolchains/" + compiler_codename + "-" + str(version) + "/prebuilt/" + platform_codename):
                platform_codename = "linux-x86_64"
        elif sys.platform == "darwin":
            platform_codename = "darwin-x86"
            if not os.path.isdir(android_ndk + "/toolchains/" + compiler_codename + "-" + str(version) + "/prebuilt/" + platform_codename):
                platform_codename = "darwin-x86_64"
        elif sys.platform == "win32":
            platform_codename = "windows"
            if not os.path.isdir(android_ndk + "/toolchains/" + compiler_codename + "-" + str(version) + "/prebuilt/" + platform_codename):
                platform_codename = "windows-x86_64"
        else:
            raise Exception("The Android NDK can't be used on other platforms")
            
        self.gcc = android_ndk + "/toolchains/" + compiler_codename + "-" + str(version) + "/prebuilt/" + platform_codename + "/bin/" + compiler_name + "-"
        self.sysroot = android_ndk + "/platforms/android-" + str(api_level) + "/arch-" + architecture_name
        self.stl_path = android_ndk + "/sources/cxx-stl/" + stl_codename
        
    def _compile(self, obj, src, ext, cc_args, extra_postargs, pp_opts):
        compiler_so = self.compiler_so
        compiler_so[0] = self.gcc + compiler_so[0]
        
        try:
            self.spawn(compiler_so + cc_args + [src, '-o', obj] +
                       extra_postargs)
        except DistutilsExecError, msg:
            raise CompileError, msg

    def link(self, target_desc, objects, output_filename, output_dir=None,
             libraries=None, library_dirs=None, runtime_library_dirs=None,
             export_symbols=None, debug=0, extra_preargs=None,
             extra_postargs=None, build_temp=None, target_lang=None):
            
        objects, output_dir = self._fix_object_args(objects, output_dir)
        
        libraries, library_dirs, runtime_library_dirs = \
            self._fix_lib_args(libraries, library_dirs, runtime_library_dirs)
        
        lib_opts = gen_lib_options(self, library_dirs, runtime_library_dirs,
                                   libraries)

        if type(output_dir) not in (StringType, NoneType):
            raise TypeError, "'output_dir' must be a string or None"
        if output_dir is not None:
            output_filename = os.path.join(output_dir, output_filename)

        if self._need_link(objects, output_filename):
            ld_args = (objects + self.objects +
                       lib_opts + ['-o', output_filename])
            if debug:
                ld_args[:0] = ['-g']
            if extra_preargs:
                ld_args[:0] = extra_preargs
            if extra_postargs:
                ld_args.extend(extra_postargs)
            self.mkpath(os.path.dirname(output_filename))
            try:
                linker = self.linker_so[:]
                if target_lang == "c++" and self.compiler_cxx:
                    linker[i] = self.compiler_cxx[i]
                
                linker[0] = self.gcc + linker[0]
                linker.append("--sysroot=" + self.sysroot)
                self.spawn(linker + ld_args)
            except DistutilsExecError, msg:
                raise LinkError, msg
        else:
            log.debug("skipping %s (up-to-date)", output_filename)
