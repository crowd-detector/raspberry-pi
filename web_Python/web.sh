#!/bin/bash

while [ 1 ]
	do
		nc -z 8.8.8.8 53 >/dev/null 2>&1
		online=$?
		if [ $online -eq 0 ]; then
			python3 ws.py
			break
		else
			echo "Offline"
		fi
		sleep 5
	done;
