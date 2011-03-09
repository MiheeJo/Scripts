#!/usr/bin/python
import sys,os,string,subprocess
try:
  import xmlrpclib
except:
  print "Please use lxplus"
  sys.exit(-1)

########## Get arguments
if len(sys.argv) != 4:
  print "Need more arguments!"
  print "Usage: %s [Start run #] [End run #] [Run duration]" %sys.argv[0]
  sys.exit(-1)
elif int(sys.argv[1]) and int(sys.argv[2]) and int(sys.argv[3]):
  startRun = sys.argv[1]
  endRun = sys.argv[2]
  runDuration = sys.argv[3]

########## Connect to run registry
server = xmlrpclib.ServerProxy("http://pccmsdqm04.cern.ch/runregistry/xmlrpc")
selection = "{groupName} = 'Collisions10' and  {runNumber} >= %s and {runNumber} <= %s and {duration} >= %s and {cmpRpc} = \'GOOD\'" %(startRun,endRun,runDuration)
# and {datasetName} LIKE '%Express%'"

print "Accessing run registry.......\n"
runData = server.DataExporter.export('RUN','GLOBAL','xml_all',selection)
#print runData

########## Get run numbers with given conditions
runInfo = []
for run in runData.split("\n"):
  if "<NUMBER>" in run:
    runInfo.append(run[8:-9])
print "Below runs will be submitted."
print runInfo

########## Submit each run to noise tool
for idx in reversed(range(1,len(runInfo))):
  print "Submit run %s" %runInfo[idx]
  subprocess.call("./submitrun.sh %s" %runInfo[idx], shell=True)
  try:
    subprocess.check_call("ls run%s | grep -q database.txt" %runInfo[idx], shell=True)
  except:
    print "Noise results for run %s don't exist..." %runInfo[idx]
    print "Something goes wrong. Program exit!"
    sys.exit(-1)
  
