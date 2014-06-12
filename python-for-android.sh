#!/bin/bash

#VERSION=2.7.7
VERSION=2.6.2
CWD=$(pwd)

#if [ ! -f ${CWD}/Python-${VERSION}.tar.xz ]; then
if [ ! -f ${CWD}/Python-${VERSION}.tar.bz2 ]; then
	#URL="http://www.python.org/ftp/python/${VERSION}/Python-${VERSION}.tar.xz"
    #wget -O ${CWD}/Python-${VERSION}.tar.xz $URL
	URL="http://www.python.org/ftp/python/${VERSION}/Python-${VERSION}.tar.bz2"
    wget -O ${CWD}/Python-${VERSION}.tar.bz2 $URL
fi

if [ ! -d host ]; then
    # we need to build the host python and host pgen so we can
    # generate the correct grammar and some other stuff
    mkdir -p ${CWD}/host
    #tar -Jxf ${CWD}/Python-${VERSION}.tar.xz
    tar -xvjf ${CWD}/Python-${VERSION}.tar.bz2
    pushd Python-${VERSION}
    ./configure --prefix=${CWD}/host/
    make
    make install
    cp Parser/pgen ${CWD}/host/
    popd
	rm -rf Python-${VERSION}
fi

PYTHONSRC=${CWD}/python-src

if [ ! -d ${PYTHONSRC} ]; then
	#tar -Jxf ${CWD}/Python-${VERSION}.tar.xz
	tar -xvjf ${CWD}/Python-${VERSION}.tar.bz2
    mv Python-${VERSION} ${PYTHONSRC}
    pushd ${PYTHONSRC}
    patch -p1 < ${CWD}/python-for-android.patch
    popd
fi

export PATH=/home/sonkun/Desktop/building-python/android/android-arm-toolchain/bin:$PATH
export CC=arm-linux-androideabi-gcc
export CXX=arm-linux-androideabi-g++
export AR=arm-linux-androideabi-ar
export RANLIB=arm-linux-androideabi-ranlib
export READELF=arm-linux-androideabi-readelf
${CWD}/host/pgen ${CWD}/python-src/Grammar/Grammar ${CWD}/python-src/Include/graminit.h ${CWD}/python-src/Python/graminit.c

cd ${PYTHONSRC}
./configure --host=arm-linux-androideabi --build=x86_64-linux-gnu --enable-shared --disable-ipv6 ac_cv_file__dev_ptmx=no ac_cv_file__dev_ptc=no ac_cv_have_long_long_format=yes need_version=no
make HOSTPYTHON=${CWD}/host/bin/python HOSTPGEN=${CWD}/host/pgen
make install HOSTPYTHON=${CWD}/host/bin/python HOSTPGEN=${CWD}/host/pgen DESTDIR=${CWD}/tmp-install
