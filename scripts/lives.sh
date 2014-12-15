#!/bin/bash

path="/home/matulik/projekty/praca/gedmin/scripts/temp/"

function servertime
{
    while [ 1 ] ; do
        file="ServerTimeOut"
	    date '+%X' > ${path}${file}
	    sleep 1s
    done
}

function meminfo
{
    while [ 1 ] ; do
        _file="_MemInfoOut"
        file="MemInfoOut"
        cat /proc/meminfo | grep 'MemTotal' > ${path}${file}
        cat /proc/meminfo | grep 'MemFree' >> ${path}${file}
        cat /proc/meminfo | grep 'Buffers' >> ${path}${file}
        cat /proc/meminfo | grep ^'Cached' >> ${path}${file}
        cat /proc/meminfo | grep ^'SwapTotal' >> ${path}${file}
        cat /proc/meminfo | grep ^'SwapFree' >> ${path}${file}
        cat /proc/meminfo | grep ^'SwapCached' >> ${path}${file}
        cp ${path}${file} ${path}${_file}
        sleep 1s
    done
}

if [ $1 = "servertime" ]; then
    servertime
fi

if [ $1 = "meminfo" ] ; then
    meminfo
fi