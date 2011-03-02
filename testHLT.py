import os, commands
#os.system('hltGetConfiguration --offline --full --mc --unprescale --process HLT --globaltag L1HLTST311_V0::All /users/cer/HLT_276TeV_V0/HLT/V7 > hlt.py ')
from HLTrigger.Configuration.hlt import *

########### get a list of files from a specified directory
mydir = "/castor/cern.ch/user/s/silvest/rootfiles/HLT/Pyhia6_Minbias_3111/root"
cmd  = 'nsls %s/ ' % (mydir)
mylist = ["rfio:%s/%s" % (mydir,j) for j in commands.getoutput(cmd).split('\n')]

process.source = cms.Source("PoolSource",
  duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
  fileNames = cms.untracked.vstring()
)

########### add a specified number of files from mydir to the list of fileNames
nfiles = len(mylist)
if nfiles > 255 :
  nfiles = 255
print "Number of files to process is %s" % (nfiles)

for i in range(0,nfiles):
  process.source.fileNames.append('%s' % (mylist[i]))
  print mylist[i]
#print "Number of files to process is %s" % (len(process.source.fileNames))

process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

########### remove the endpaths from the default configuration
import FWCore.ParameterSet.DictTypes
process.__dict__['_Process__endpaths'] = FWCore.ParameterSet.DictTypes.SortedKeysDict()

########## Filter for reference path
process.filter = cms.EDFilter("HLTHighLevel",
    TriggerResultsTag = cms.InputTag("TriggerResults","","HLT"),
    HLTPaths = cms.vstring("HLT_L1SingleMuOpen_v1"),#HLT_HIL1SingleMu3","HLT_HIL1DoubleMuOpen"),  
    eventSetupPathsKey = cms.string(''),
    andOr = cms.bool(True),
    throw = cms.bool(False),
)
'''
for path in process.paths:
getattr(process,path)._seq = process.filter*getattr(process,path)._seq
'''

########## Start / end of processes
process.hltGetRaw = cms.EDAnalyzer( "HLTGetRaw",
    RawDataCollection = cms.InputTag( "rawDataCollector" )
)
process.hltBoolFalse = cms.EDFilter( "HLTBool",
    result = cms.bool( True )
)
process.HLTriggerFirstPath = cms.Path( process.hltGetRaw + process.hltBoolFalse )

process.hltTrigReport = cms.EDAnalyzer("HLTrigReport",
   HLTriggerResults = cms.InputTag("TriggerResults","","HLT"),
   ReferenceRate = cms.untracked.double(14.06),
   ReferencePath = cms.untracked.string('HLT_L1SingleMuOpen_v1'),
)
process.HLTriggerEndPath = cms.EndPath(process.hltTrigReport)

########## MessageLogger
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.categories.append('TriggerSummaryProducerAOD')
process.MessageLogger.categories.append('L1GtTrigReport')
process.MessageLogger.categories.append('HLTrigReport')

########## Running paths
process.schedule = cms.Schedule(
  process.HLTriggerFirstPath,
  process.HLTriggerEndPath
)
