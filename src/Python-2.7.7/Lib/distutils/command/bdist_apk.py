"""distutils.command.bdist_apk

Implements the Distutils 'bdist_apk' command that creates an Android
project, configure it to use the Python boostrap which will call the
user entry point of his application, and create the final .apk
package."""

__revision__ = "$Id$"

import os

from distutils.core import Command
from distutils.debug import DEBUG
from distutils.errors import DistutilsPlatformError

from subprocess import call

class bdist_apk (Command):

    description = "create an Android package"

    user_options = [
        ('android-ndk=', None,
         "location of the android ndk"),
        ('dist-dir=', 'd',
         "directory to put final RPM files in)")]

    def initialize_options(self):
        self.android_ndk = os.environ.get('ANDROID_NDK')
        self.dist_dir = None

    def finalize_options(self):
        if self.android_ndk is None:
            raise DistutilsPlatformError(
                "Building an APK requires access to the android NDK. Please "
                "specify its location using either the ANDROID_NDK "
                "variable or by passing it to the --android-ndk option.")

        self.dist_dir = self.dist_dir or "dist"

    def run(self):
        name = self.distribution.get_name()

        if DEBUG:
            print("preparing an Android project")

        self.mkpath(self.dist_dir)
        call([
            "android", "create", "project",
            "--target", "android-10",
            "--name", name,
            "--path", os.path.join(self.dist_dir, name),
            "--activity", "MainActivity",
            "--package", "org.python.{}".format(name)]) 

        print("Note: No bootstrap available, so this build WILL fail!")
        if DEBUG:
            call(["ant", "debug"])
        else:
            call(["ant", "release"])
