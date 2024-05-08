#!/bin/bash
process_count=$(ps aux | grep "deal.py" | grep -v "grep" | wc -l)

if [ $process_count -gt 0 ]; then
    echo "deal.py is already running."
    exit
fi


python3 /root/sh/sqlToDeal/deal.py  >> /root/log/deal.log 2>&1 &
