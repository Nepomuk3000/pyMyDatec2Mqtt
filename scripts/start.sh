#!/bin/sh
ROOT_DIR=`dirname $(readlink -m $0)`
echo $ROOT_DIR

$ROOT_DIR/kill.sh
rm -f nohup.out
nohup python $ROOT_DIR/../myDatecMqttGateway.py &
