#!/bin/bash

while read line
do
    if [[ X$line!='X' ]];
    then
      tar_name=`echo $line| awk '{ print $1 }'`
      image=`echo $line| awk '{ print $2 }'`
      echo "load $tar_name"

      docker load < $tar_name
      docker push $image
    fi
done < $1