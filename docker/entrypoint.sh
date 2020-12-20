#!/bin/sh

. /opt/conda/etc/profile.d/conda.sh
conda activate base
conda activate soccer

if [ "$@" == "none" ]; then
	bash
else
	$@
fi
