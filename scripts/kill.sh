#!/bin/sh
stop=0
cpt=0
while [ $stop -eq 0 ]
do
    netstat -lnp 2> /dev/null | grep -q 10004
    if [ $? -eq 0 ]
    then
        if [ $cpt -le 5 ]
        then
            echo "On essaye de tuer $PID proprement"
            PID=`netstat -lnp 2> /dev/null | grep 10004 | sed "s@  *@/@g" | cut -d"/" -f7 `
            kill $PID
        else
            echo "On tue $PID salement"
            kill -9 $PID 2> /dev/null
        fi
    else
        stop=1
    fi
    cpt=$(($cpt + 1))
done