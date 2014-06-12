"""distutils.command.bdist_apk

Implements the Distutils 'bdist_apk' command that creates an Android
project, configure it to use the Python boostrap which will call the
user entry point of his application, and create the final .apk
package."""

__revision__ = "$Id$"

import os

from distutils.core import Command
from distutils.errors import DistutilsPlatformError

class bdist_apk (Command):

    description = "create an Android package"

    user_options = [('android-ndk=', None,
                     "location of the android ndk")]

    def initialize_options(self):
        self.android_ndk = os.environ.get('ANDROID_NDK')

    def finalize_options(self):
        if self.android_ndk is None:
            raise DistutilsPlatformError, \
                  ("don't know where the Android NDK directory is " +
                   "we expect an environement variable ANDROID_NDK pointing to it " +
                   "or use the --android-ndk argument")

    def run(self):
        print(self.android_ndk)
        print("Create the apk...")
