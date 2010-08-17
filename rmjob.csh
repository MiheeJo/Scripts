#!/bin/sh
# kill the remaining batch jobs
#echo $(awk '{print $1}' < $(bqueues | grep Open:Active))
(bjobs | grep miheejo) > blist
bkill $(awk '{print $1}' < blist)
rm -f blist
