import FWCore.ParameterSet.Config as cms
import CommonFSQFramework.Core.Util
import os

isData = False
if "TMFSampleName" not in os.environ:
    print "TMFSampleName not found, assuming we are running on MC"
else:
    s = os.environ["TMFSampleName"]
    sampleList=CommonFSQFramework.Core.Util.getAnaDefinition("sam")
    isData =  sampleList[s]["isData"]
    if isData: print "Disabling MC-specific features for sample",s
        
  

process = cms.Process("Treemaker")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))

process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))

# Source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
       '/store/user/sbaur/MinBias_CUETP8M1_13TeV-pythia8/MinBias_CUETP8M1_13TeV-pythia8_MagnetOff_CASTORmeasured_RECO/160207_214204/0000/MinBias_CUETP8M1_13TeV-pythia8_CASTORmeasured_RECO_511.root') 


       )
    
       
        
        
       
)

# Geometry and Detector Conditions
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
if isData: process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data', '')
# if not isData: process.GlobalTag = GlobalTag(process.GlobalTag,'76X_mcRun2_asymptotic_v14', '')
if not isData: process.GlobalTag = GlobalTag(process.GlobalTag,'auto:run2_mc', '')
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")
print process.GlobalTag.globaltag

# get custom CASTOR conditions to mark/remove bad channels
process.load("CondCore.DBCommon.CondDBSetup_cfi")
process.CastorDbProducer = cms.ESProducer("CastorDbProducer")

process.es_ascii = cms.ESSource("CastorTextCalibrations",
   input = cms.VPSet(
       cms.PSet(
           object = cms.string('ChannelQuality'),
           file = cms.FileInPath('data/quality__2015.txt')
       ),
   )
)

process.es_prefer_castor = cms.ESPrefer('CastorTextCalibrations','es_ascii')

# for MC reproduce the CastorTowers and CastorJets to remove the bad channels there
if not isData:
    process.load('RecoLocalCalo.Castor.Castor_cff')
    process.CastorReReco = cms.Path(process.CastorFullReco)

# produce HF PFClusters
process.PFClustersHF = cms.Path(process.particleFlowRecHitHF*process.particleFlowClusterHF)

#in data produce Tracker Rechits
# if isData:
process.PixelRecHits = cms.Path(process.siPixelRecHits)
process.StripMatchedRecHits = cms.Path(process.siStripMatchedRecHits)


# Here starts the CFF specific part
import CommonFSQFramework.Core.customizePAT
process = CommonFSQFramework.Core.customizePAT.customize(process)

# GT customization
process = CommonFSQFramework.Core.customizePAT.customizeGT(process)

# define treeproducer
process.EflowTree = cms.EDAnalyzer("CFFTreeProducer")

import CommonFSQFramework.Core.VerticesViewsConfigs
import CommonFSQFramework.Core.CaloRecHitViewsConfigs
import CommonFSQFramework.Core.CaloTowerViewsConfigs
import CommonFSQFramework.Core.CastorViewsConfigs
import CommonFSQFramework.Core.PFObjectsViewsConfigs
import CommonFSQFramework.Core.TriggerResultsViewsConfigs

if not isData:
    import CommonFSQFramework.Core.GenLevelViewsConfigs
    


if not isData:
    process.EflowTree._Parameterizable__setParameters(CommonFSQFramework.Core.VerticesViewsConfigs.get(["VerticesView","ZeroTeslaVertexView_Pixel_PreSplitting","ZeroTeslaVertexView_Pixel_noPreSplitting","ZeroTeslaVertexView_Strips"]))
if isData:
    process.EflowTree._Parameterizable__setParameters(CommonFSQFramework.Core.VerticesViewsConfigs.get(["VerticesView","ZeroTeslaVertexView_Pixel_noPreSplitting","ZeroTeslaVertexView_Strips"]))
# process.EflowTree._Parameterizable__setParameters(CommonFSQFramework.Core.VerticesViewsConfigs.get(["VerticesView"]))
process.EflowTree._Parameterizable__setParameters(CommonFSQFramework.Core.CaloRecHitViewsConfigs.get(["EcalRecHitView","HBHERecHitView","HFRecHitView"]))
process.EflowTree._Parameterizable__setParameters(CommonFSQFramework.Core.CaloTowerViewsConfigs.get(["CaloTowerView"]))
process.EflowTree._Parameterizable__setParameters(CommonFSQFramework.Core.CastorViewsConfigs.get(["CastorRecHitViewFull","CastorTowerView"]))
process.EflowTree._Parameterizable__setParameters(CommonFSQFramework.Core.PFObjectsViewsConfigs.get(["PFCandidateView","ecalPFClusterView","hcalPFClusterView","hfPFClusterView"]))
if isData: process.EflowTree._Parameterizable__setParameters(CommonFSQFramework.Core.TriggerResultsViewsConfigs.get(["ZeroBiasTriggerResultsViewWithPS","L1GTriggerResultsView"]))

if not isData:
    process.EflowTree._Parameterizable__setParameters(CommonFSQFramework.Core.GenLevelViewsConfigs.get(["GenPartView"]))

# add paths
if not isData:
    process = CommonFSQFramework.Core.customizePAT.addPath(process, process.CastorReReco)
# if isData:
process = CommonFSQFramework.Core.customizePAT.addPath(process, process.PixelRecHits)
    
process = CommonFSQFramework.Core.customizePAT.addPath(process, process.StripMatchedRecHits)
process = CommonFSQFramework.Core.customizePAT.addPath(process, process.PFClustersHF)
process = CommonFSQFramework.Core.customizePAT.addTreeProducer(process, process.EflowTree)
