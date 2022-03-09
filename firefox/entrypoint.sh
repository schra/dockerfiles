#!/bin/bash

# This file is originally by Jessie Frazelle and is licensed under the MIT
# license.

if [[ -e /dev/snd ]]; then
	exec apulse firefox "$@"
else
	exec firefox "$@"
fi
