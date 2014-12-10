#!/bin/bash
function servertime
{
    while [ 1 ] ; do
	date '+%X' > /home/matulik/projekty/praca/skrypty/temp/ServerTimeOut
	sleep 1s
    done
}

if [ $1 = "servertime" ]; then
    servertime
fi