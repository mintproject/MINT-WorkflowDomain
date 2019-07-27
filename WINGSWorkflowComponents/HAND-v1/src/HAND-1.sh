#!/bin/bash

set -x
set -e

## Get options
dem=""
thresh=""
hand=""
usage() { echo "Usage: $0 -d <dem_file.tif> [-t <threshold>] [-h <hand_file.tif>]" 1>&2; exit 1; }
while getopts "d:t:h:" opt; do
	case "$opt" in
		d)  dem=$OPTARG
		    ;;
		t)  thresh=$OPTARG
		    ;;
		h)  hand=$OPTARG
		    ;;
		*)  usage
		    ;;
	esac
done
shift $((OPTIND-1))

## Extract height above nearest drainage from digital elevation model
if [ -z "${dem}" ]; then
	usage
fi
dem_ext="${dem##*.}"
dem_fn="${dem%.*}"
pitremove $dem
dinfflowdir $dem
areadinf $dem
if [ -z "${thresh}" ]; then
	threshold -ssa "${dem_fn}sca.${dem_ext}" \
		  -src "${dem_fn}src.${dem_ext}" \
		  -thresh 100.0
else
	threshold -ssa "${dem_fn}sca.${dem_ext}" \
		  -src "${dem_fn}src.${dem_ext}" \
		  -thresh $thresh
fi
if [ -z "${hand}" ]; then
	dinfdistdown -ang "${dem_fn}ang.${dem_ext}" \
		     -fel "${dem_fn}fel.${dem_ext}" \
		     -src "${dem_fn}src.${dem_ext}" \
		     -dd "${dem_fn}dd.${dem_ext}"   \
		     -m ave v
else
    HAND_UID=`mktemp -u -p . -t XXXX`.tif
	dinfdistdown -ang "${dem_fn}ang.${dem_ext}" \
		     -fel "${dem_fn}fel.${dem_ext}" \
		     -src "${dem_fn}src.${dem_ext}" \
		     -dd $HAND_UID                  \
		     -m ave v
             mv $HAND_UID $hand
fi
