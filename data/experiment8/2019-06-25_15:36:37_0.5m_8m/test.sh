#!/bin/bash
# get min and max value of files in current directory

MY_SAVEIFS=$IFS
IFS=$'\n'

# path = $(pwd)


for filename in `ls`
do
	awk -F '"' 'BEGIN{max=-100;min=0; s=0}{ s = s + $8; if ($8>max) max = $8; if ($8<min) min=$8; }END{print FILENAME; print max "," min "," s/NR;}' "${filename}"
	# echo ${filename}
	# echo '===>'
done

IFS=$MY_SAVEIFS
