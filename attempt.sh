#!/bin/bash

# Try the stream of passwords against geth account number 0

while read PASS; do
	echo "Trying $PASS"
	echo "$PASS" | geth account update 0 2>&1 | grep Unlocked
	if [ "$?" = "0" ]; then
		echo "Found: $PASS"
		exit 0
	fi
done

exit 1
