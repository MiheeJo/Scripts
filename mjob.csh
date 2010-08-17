#!/bin/csh
# Submit batch jobs
# This must be used with MkRunBat.sh

cd _pwd_
eval `scramv1 runtime -csh`
cd -
cmsRun _pwd_/_input_py_
rfcp _output_file_ _storage_
