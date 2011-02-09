#!/usr/bin/python
import sys,os,string
try:
  import xmlrpclib, commands
except:
  print "Please use lxplus"
  sys.exit(-1)

### Connect to run registry
server = xmlrpclib.ServerProxy("http://pccmsdqm04.cern.ch/runregistry/xmlrpc")
selection = "{groupName} = 'Collisions10' and  {runNumber} >= 132400 and {runNumber} <= 133887 and {duration} >= 1200 and {cmpRpc} = \'GOOD\'"# and {datasetName} LIKE '%Express%'"

print "Accessing run registry....\n"
runData = server.DataExporter.export('RUN','GLOBAL','xml_all',selection)

#print runData

runInfo = []
for run in runData.split("\n"):
  if "<NUMBER>" in run:
    runInfo.append(run[8:-9])
#    print run[8:-9]
print runInfo
