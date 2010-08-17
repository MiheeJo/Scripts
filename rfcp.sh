#!/bin/sh -f

indir="/castor/cern.ch/user/m/miheejo/cms370/HardEnriched_vtxcor_ZS_skim0"

for file in `nsls $indir`
do
  rfcp $indir/$file .
#  echo $indir/$file
done
