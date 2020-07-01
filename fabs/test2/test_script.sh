#!/bin/bash
rings=$(nodetool ring |  sed -ne '/^[0-9]/p' | awk '{print $3, $4}' | sort -u | grep -c -v 'Up')
echo "$HOSTNAME RINGS : $rings"
