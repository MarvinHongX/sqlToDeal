#!/bin/bash

#00. bashrc
cat /home/fildata/.bashrc | grep export > /root/sh/sqlToDeal/bash.sh
cat /home/fildata/.bashrc | grep cargo >> /root/sh/sqlToDeal/bash.sh
cat /root/sh/sqlToDeal/bash.sh
. /root/sh/sqlToDeal/bash.sh


process_count2=$(ps aux | grep "sql_to_deal.py" | grep -v "grep" | wc -l)

if [ $process_count2 -gt 0 ]; then
    echo "sql_to_deal.py is already running."
    exit
fi


process_count=$(ps aux | grep "deal.py" | grep -v "grep" | wc -l)

if [ $process_count -gt 0 ]; then
    echo "deal.py is already running."
    exit
fi


python3 /root/sh/sqlToDeal/sql_to_deal.py  >> /root/log/sql_to_deal.log 2>&1 &
