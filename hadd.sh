#!/bin/bash

list=$(nsls /castor/cern.ch/cms/store/user/tdahms/HeavyIons/Onia/Data2010/v10/Skims/ReReco/ | grep onia2MuMuPAT)
for file in $list
do
  tmp=$tmp" rfio:/castor/cern.ch/cms/store/user/tdahms/HeavyIons/Onia/Data2010/v10/Skims/ReReco/"$file
done
echo $tmp

hadd /tmp/miheejo/onia2MuMuPATmerge.root $tmp >& merge.log &
