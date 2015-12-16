import FWCore.ParameterSet.Config as cms
import CommonFSQFramework.Core.Util
import os

isData = True

if "TMFSampleName" not in os.environ:
    print "TMFSampleName not found, assuming we are running on MC"
else:
    s = os.environ["TMFSampleName"]
    sampleList=CommonFSQFramework.Core.Util.getAnaDefinition("sam")
    isData =  sampleList[s]["isData"]
    if isData: print "Disabling MC-specific features for sample",s

# for test purpose
# isData = True

# when isRawData = True the unpacker is used to create castor Digis and also RecHits
isRawData = False

process = cms.Process("Treemaker")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1000))

process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))

# Source
process.source = cms.Source("PoolSource",
    # fileNames = cms.untracked.vstring('/store/user/hvanhaev/ZeroBias1/Run2015A-v1_RERECO_Run247324_GR_P_V54_withCustomCond-v1/150608_213851/0000/output_data_rereco_1.root')
    #fileNames = cms.untracked.vstring('/store/user/hvanhaev/MinBias_TuneMonash13_13TeV-pythia8/RunIISpring15DR74-NoPU0T_MCRUN2_740TV0_step2-v2/150610_055012/0000/step2_RAW2DIGI_L1Reco_RECO_1.root')
    #fileNames = cms.untracked.vstring('/store/mc/RunIISpring15DR74/ReggeGribovPartonMC_13TeV-EPOS/GEN-SIM-RECO/NoPURawReco_castor_MCRUN2_74_V8B-v1/10000/BC62D29E-7707-E511-A6D9-AC853D9F5344.root')
    #fileNames = cms.untracked.vstring('/store/data/Run2015A/ZeroBias/RECO/PromptReco-v1/000/247/607/00000/52EA626D-9210-E511-843F-02163E01451D.root')
    # fileNames = cms.untracked.vstring('/store/data/Run2015A/MinimumBias/RECO/PromptReco-v1/000/247/403/00000/061A4C94-3B0F-E511-B492-02163E0140E0.root')
    fileNames = cms.untracked.vstring('/store/hidata/HIRun2013/PAMinBiasUPC/RECO/PromptReco-v1/000/210/321/00000/448E474C-3A62-E211-B402-BCAEC532971B.root')
    # fileNames = cms.untracked.vstring('/store/hidata/HIRun2015/Cosmics/RAW/v1/000/262/611/00000/AE2C3478-B793-E511-957C-02163E011B19.root')
    # fileNames = cms.untracked.vstring('file:/tmp/cwohrman/3A28079F-4262-E211-B6D7-5404A640A63D.root')
)

# from PhysicsTools.PatAlgos.patInputFiles_cff import filesRelValProdTTbarGENSIMRECO
# process.source.fileNames = filesRelValProdTTbarGENSIMRECO

# Geometry and Detector Conditions
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
if isData: process.GlobalTag = GlobalTag(process.GlobalTag, 'GR_R_75_V5A', '')
if not isData: process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')
process.load("Configuration.StandardSequences.MagneticField_cff")

# for test purpose
# process.GlobalTag = GlobalTag(process.GlobalTag, 'MCRUN2_75_V5', '')

print process.GlobalTag.globaltag
# process.load("Configuration.StandardSequences.Reconstruction_cff")

# # get custom CASTOR conditions to mark/remove bad channels
# process.load("CondCore.DBCommon.CondDBSetup_cfi")
# process.CastorDbProducer = cms.ESProducer("CastorDbProducer")

# process.es_ascii = cms.ESSource("CastorTextCalibrations",
#    input = cms.VPSet(
#        cms.PSet(
#            object = cms.string('ChannelQuality'),
#            file = cms.FileInPath('data/customcond/castor/quality__2015.txt')
#        ),
#    )
# )

# process.es_prefer_castor = cms.ESPrefer('CastorTextCalibrations','es_ascii')

# # for MC reproduce the CastorTowers and CastorJets to remove the bad channels there
# if not isData:
#     process.load('RecoLocalCalo.Castor.Castor_cff')
#     process.CastorReReco = cms.Path(process.CastorFullReco)

# produce HF PFClusters
# process.PFClustersHF = cms.Path(process.particleFlowRecHitHF*process.particleFlowClusterHF)



if isRawData:
    ###############################################################################
    ###############################################################################
    # ## when running on raw data digis has to been unpacked 
    # ## and RecHits need to be reconstruct
    process.load('Configuration.StandardSequences.RawToDigi_cff')
    process.rawtodigi = cms.Path(process.gtDigis)

    process.castorDigis = cms.EDProducer("CastorRawToDigi",
        # Optional filter to remove any digi with "data valid" off, "error" on, 
        # or capids not rotating
        FilterDataQuality = cms.bool(True),
        # Number of the first CASTOR FED.  If this is not specified, the
        # default from FEDNumbering is used.
        CastorFirstFED = cms.int32(690),
        # FED numbers to unpack.  If this is not specified, all FEDs from
        # FEDNumbering will be unpacked.
        FEDs = cms.untracked.vint32( 690, 691, 692 ),
        # Do not complain about missing FEDs
        ExceptionEmptyData = cms.untracked.bool(False),
        # Do not complain about missing FEDs
        ComplainEmptyData = cms.untracked.bool(False),
        # At most ten samples can be put into a digi, if there are more
        # than ten, firstSample and lastSample select which samples
        # will be copied to the digi
        firstSample = cms.int32(0),
        lastSample = cms.int32(9),
        # castor technical trigger processor
        UnpackTTP = cms.bool(True),
        # report errors
        silent = cms.untracked.bool(False),
        #
        InputLabel = cms.InputTag("rawDataCollector"),
        CastorCtdc = cms.bool(False),
        UseNominalOrbitMessageTime = cms.bool(True),
        ExpectedOrbitMessageTime = cms.int32(-1)
    )

    process.load('RecoLocalCalo.CastorReco.CastorSimpleReconstructor_cfi')
    process.castorlocalreco = cms.Path(process.castorDigis*process.castorreco)
    ###############################################################################


###############################################################################
###############################################################################
## switch to uncheduled mode
process.options.allowUnscheduled = cms.untracked.bool(True)
#process.Tracer = cms.Service("Tracer")

process.load("PhysicsTools.PatAlgos.producersLayer1.patCandidates_cff")
process.load("PhysicsTools.PatAlgos.selectionLayer1.selectedPatCandidates_cff")

from PhysicsTools.PatAlgos.tools.metTools import addMETCollection
#addMETCollection(process, labelName='patMETCalo', metSource='met')
addMETCollection(process, labelName='patMETPF', metSource='pfMetT1')
#addMETCollection(process, labelName='patMETTC', metSource='tcMet') # FIXME: removed from RECO/AOD; needs functionality to add to processing

## uncomment the following line to add different jet collections
## to the event content
from PhysicsTools.PatAlgos.tools.jetTools import addJetCollection
from PhysicsTools.PatAlgos.tools.jetTools import switchJetCollection

# uncomment the following lines to switch to ak4CaloJets in your PAT output
labelAK4Calo = 'AK4Calo'
addJetCollection(
   process,
   labelName = labelAK4Calo,
   jetSource = cms.InputTag('ak4CaloJets'),
   jetCorrections = ('AK7Calo', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute']), 'Type-1'), # FIXME: Use proper JECs, as soon as available
   btagDiscriminators = [
       'pfJetBProbabilityBJetTags'
     , 'pfJetProbabilityBJetTags'
     , 'pfTrackCountingHighPurBJetTags'
     , 'pfTrackCountingHighEffBJetTags'
     , 'pfSimpleSecondaryVertexHighEffBJetTags'
     , 'pfSimpleSecondaryVertexHighPurBJetTags'
     , 'pfCombinedInclusiveSecondaryVertexV2BJetTags'
     ]
   )
#process.out.outputCommands.append( 'drop *_selectedPatJets%s_pfCandidates_*'%( labelAK4Calo ) )
## JetID works only with RECO input for the CaloTowers (s. below for 'process.source.fileNames')
#process.patJets.addJetID=True
#process.load("RecoJets.JetProducers.ak4JetID_cfi")
#process.patJets.jetIDMap="ak4JetID"
process.patJetsAK4Calo.useLegacyJetMCFlavour=True # Need to use legacy flavour since the new flavour requires jet constituents which are dropped for CaloJets from AOD
###############################################################################
###############################################################################

###############################################################################
# HLT path filter
process.hltcastormuon = cms.EDFilter("HLTHighLevel",
     TriggerResultsTag = cms.InputTag("TriggerResults","","HLT"),
     # HLTPaths = cms.vstring('HLT_L1CastorMuon_v1','HLT_L1Tech59_CASTORHaloMuon_v1'), # provide list of HLT paths (or patterns) you want
     # HLTPaths = cms.vstring('HLT_L1Tech59_CastorMuon_v1'), # provide list of HLT paths (or patterns) you want
     HLTPaths = cms.vstring('HLT_PAL1Tech63_CASTORHaloMuon_v1'), # provide list of HLT paths (or patterns) you want
     eventSetupPathsKey = cms.string(''), # not empty => use read paths from AlCaRecoTriggerBitsRcd via this key #HLT_MinBiasBSC # HLT_L1Tech_BSC_minBias
     andOr = cms.bool(True),             # how to deal with multiple triggers: True (OR) accept if ANY is true, False (AND) accept if ALL are true
     throw = cms.bool(False)    # throw exception on unknown path names
) 
###############################################################################
###############################################################################

# Here starts the CFF specific part
import CommonFSQFramework.Core.customizePAT
process = CommonFSQFramework.Core.customizePAT.customize(process)

# GT customization
process = CommonFSQFramework.Core.customizePAT.customizeGT(process)

# define treeproducer
process.MuonCastorVTwo = cms.EDAnalyzer("CFFTreeProducer")

# use this when HLT filter should be used to create tree
# comment: filter has to be include with a star before the EDAnalyzer in a path
#          so CMSSW knows that can not paralize event processing
process.FiltererdTree = cms.Path(process.hltcastormuon*process.MuonCastorVTwo)

import CommonFSQFramework.Core.VerticesViewsConfigs
import CommonFSQFramework.Core.CaloRecHitViewsConfigs
import CommonFSQFramework.Core.CaloTowerViewsConfigs
import CommonFSQFramework.Core.CastorViewsConfigs
import CommonFSQFramework.Core.PFObjectsViewsConfigs
import CommonFSQFramework.Core.TriggerResultsViewsConfigs
import CommonFSQFramework.Core.JetViewsConfigs

if not isData:
    import CommonFSQFramework.Core.GenLevelViewsConfigs
    

# process.MuonCastorVTwo._Parameterizable__setParameters(CommonFSQFramework.Core.VerticesViewsConfigs.get(["VerticesView"]))
# process.MuonCastorVTwo._Parameterizable__setParameters(CommonFSQFramework.Core.CaloRecHitViewsConfigs.get(["HBHERecHitView","HFRecHitView"]))
# process.MuonCastorVTwo._Parameterizable__setParameters(CommonFSQFramework.Core.CaloTowerViewsConfigs.get(["CaloTowerView"]))
# process.MuonCastorVTwo._Parameterizable__setParameters(CommonFSQFramework.Core.CastorViewsConfigs.get(["ak5CastorJetView"]))
process.MuonCastorVTwo._Parameterizable__setParameters(CommonFSQFramework.Core.CastorViewsConfigs.get(["CastorRecHitViewFull"]))
# process.MuonCastorVTwo._Parameterizable__setParameters(CommonFSQFramework.Core.PFObjectsViewsConfigs.get(["PFCandidateView","ecalPFClusterView","hcalPFClusterView","hfPFClusterView"]))
# process.MuonCastorVTwo._Parameterizable__setParameters(CommonFSQFramework.Core.TriggerResultsViewsConfigs.get(["CastorSpecialMuonTriggerResultsView","L1GTriggerResultsView"]))
process.MuonCastorVTwo._Parameterizable__setParameters(CommonFSQFramework.Core.TriggerResultsViewsConfigs.get(["CastorSpecialMuonTriggerResultsView_2013PA","L1GTriggerResultsView"]))
#process.MuonCastorVTwo._Parameterizable__setParameters(CommonFSQFramework.Core.JetViewsConfigs.get(["JetViewAK4Calo"]))

if not isData:
    process.MuonCastorVTwo._Parameterizable__setParameters(CommonFSQFramework.Core.GenLevelViewsConfigs.get(["GenPartView"]))
    process.MuonCastorVTwo._Parameterizable__setParameters(CommonFSQFramework.Core.GenLevelViewsConfigs.get(["ak4GenJetView"]))

# steps which are needed for RecHit creation when run on RAW data
if isRawData:
    process = CommonFSQFramework.Core.customizePAT.addPath(process, process.rawtodigi)
    process = CommonFSQFramework.Core.customizePAT.addPath(process, process.castorlocalreco)


# # add paths
# if not isData:
#     process = CommonFSQFramework.Core.customizePAT.addPath(process, process.CastorReReco)

# process = CommonFSQFramework.Core.customizePAT.addPath(process, process.PFClustersHF)

###############################################################################
# produce just CFF tree without any filters
# process = CommonFSQFramework.Core.customizePAT.addTreeProducer(process, process.MuonCastorVTwo)

###############################################################################
# produce CFF tree whith filter
process = CommonFSQFramework.Core.customizePAT.addPath(process, process.FiltererdTree)
