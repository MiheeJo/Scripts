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
  print "Usage: %s [Start run #] [End run #] [Run duration in unit of seconds(>=1200)]" %sys.argv[0]
  sys.exit(-1)
elif int(sys.argv[1]) and int(sys.argv[2]) and int(sys.argv[3]):
  startRun = sys.argv[1]
  endRun = sys.argv[2]
  runDuration = sys.argv[3]
else:
  print "ERROR!!!!!!!!!! Put integer values only!"

########## Connect to run registry
server = xmlrpclib.ServerProxy("http://pccmsdqm04.cern.ch/runregistry/xmlrpc")
selection = "{groupName} = 'Cosmics11' and  {runNumber} >= %s and {runNumber} <= %s and {duration} >= %s and {cmpRpc} = \'GOOD\'" %(startRun,endRun,runDuration)
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

os.environ["PYTHONPATH"]="/nfshome0/mmaggi/PYTHON"
#runInfo = [136097,136096,136088,136087,136083,136082,136080,136068]
runOK = []
########## Submit each run to noise tool
for idx in reversed(range(0,len(runInfo))):
  print "Submit run %s" %runInfo[idx]
#  subprocess.call("./submitrun.sh %s" %runInfo[idx], shell=True)
  try:  #Check database file is there
    subprocess.check_call("ls run%s | grep -q database_new.txt" %runInfo[idx], shell=True)
  except:
    print "Noise results for run %s don't exist..." %runInfo[idx]
    print "Anyway continues........"
    continue
  runOK.append(runInfo[idx])
  try:  #runDataToDB.py to put data into the DB
    subprocess.check_call("python runDataToDB.py -s sqliteDB.db run%s/database_new.txt" %runInfo[idx], shell=True)
  except:
    print "\n\nERROR!!!!!!!!!! run%s: runDataToDB.py doesn't work! Please contact to expert!" %runInfo[idx]
    sys.exit(-1)

########## Finally done!
print "\n\nBelow run's noise informations are put into DB properly :"
for idx in range(0,len(runOK)):
  print runOK[idx]
sys.exit(0)
