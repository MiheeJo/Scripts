#!/usr/bin/python
import sys,os,string
try:
  import xmlrpclib, commands
except:
  print "Please use lxplus"
  sys.exit(-1)

### Connect to run registry
server = xmlrpclib.ServerProxy("http://pccmsdqm04.cern.ch/runregistry/xmlrpc")
#selection = "{groupName} = 'Collisions10' and {runNumber} >= 130000 {runNumber} <= 133887 and {duration} >= 3600"
selection = "{runNumber} >= 130000 and {runNumber} <= 133887 and {duration} >= 3600"

#print "Accessing run registry....\n"
runData = server.DataExporter.export('RUN','GLOBAL','xml_all',selection)

#print runData

runInfo = []

for run in runData.split("\n"):
  if "<NUMBER>" in run:
    runInfo.append(run[8:-9])
  elif "<GROUP_NAME>Collisions10</GROUP_NAME>" in run:
    runInfo.append("Collisions10")
  elif "<NAME>RPC</NAME>" in run:
    if runInfo.count("Collisions10") == 1 and runInfo.count("isRPC") == 0:
      runInfo.append("isRPC")
  elif "<VALUE>GOOD</VALUE>" in run:
    if runInfo.count("isRPC") == 1 and runInfo.count("isRPCGood") == 0:
      runInfo.append("isRPCGood")
  elif "</RUN>" in run:
    if runInfo.count("isRPCGood") == 1:
      print runInfo
    del runInfo[:]
