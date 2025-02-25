#!/bin/bash

INTERVAL=300 # sec
TARGET=log.txt # target file of watch
CONTINUE=false # flag of run runner.sh or continue.sh
WATCHDOG_LOG=watchdog_log.txt

while getopts cl:b:e: OPT
do
  case $OPT in
    "c" ) CONTINUE=true ;;
    "l" ) label="${OPTARG}" ;;
    "b" ) begin="${OPTARG}" ;;
    "e" ) end="${OPTARG}" ;;
  esac
done

echo "start-up watchdog_runner.sh" >> ${WATCHDOG_LOG}
echo "--ITERVAL=${INTERVAL}" >> ${WATCHDOG_LOG}
echo "--TARGET=${TARGET}" >> ${WATCHDOG_LOG}
if [ ${CONTINUE} ] ; then
  echo "--CONTINUE mode" >> ${WATCHDOG_LOG}
else
  echo "--label=${label}" >> ${WATCHDOG_LOG}
  echo "--begin=${begin}" >> ${WATCHDOG_LOG}
  echo "--end=${end}" >> ${WATCHDOG_LOG}
fi

touch ${TARGET}

last=`ls --full-time ${TARGET} | awk '{print $6"-"$7}'`

echo -n "start process" >> ${WATCHDOG_LOG}
if [ ${CONTINUE} ] ; then
  sh continue.sh &
else
  sh runner.sh -l ${label} -b ${begin} -e ${end} &
fi
PID=$!
echo "done!" >> ${WATCHDOG_LOG}

trap 'kill ${PID} ; exit 1'  1 2 3 15

sleep ${INTERVAL}

while [ `ps -a | grep "${PID}" -o` ] ; do

  current=`ls --full-time ${TARGET} | awk '{print $6"-"$7}'`

  if [ ${last} != ${current} ] ; then
    last=$current
  else
    echo -n "shutdown process..." >> ${WATCHDOG_LOG}
    kill ${PID}
    echo "done!"
    echo -n "rebooting process..." >> ${WATCHDOG_LOG}
    sh continue.sh &
    PID=$!
    echo "done!"
  fi

  sleep ${INTERVAL}
done

echo "all process finished!" >> ${WATCHDOG_LOG}

exit 0
