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
        
# JUST FOR CROSSCHeck
# isData = True


process = cms.Process("Treemaker")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))

process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))

# Source
process.source = cms.Source("PoolSource",
    # fileNames = cms.untracked.vstring('/store/user/sbaur/MinBias_CUETP8M1_13TeV-pythia8/MinBias_CUETP8M1_13TeV-pythia8_MagnetOff_CASTORmeasured_RECO/160207_214204/0000/MinBias_CUETP8M1_13TeV-pythia8_CASTORmeasured_RECO_1.root',,)
    fileNames = cms.untracked.vstring(
      # # 251721
      #  '/store/data/Run2015B/ZeroBias1/RECO/16Dec2015-v1/70000/EC4D4897-BAB2-E511-AFCB-00266CFEFCE8.root'

      # 247934 0 Tesla
      
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/04C45CEB-F116-E511-9DE7-02163E011A7B.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/06A76DBE-F116-E511-92F7-02163E0138FD.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/06CF140F-F016-E511-9D43-02163E013629.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/0867684A-6613-E511-AAA1-02163E0135E2.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/0891CF7B-E116-E511-9D86-02163E011BFC.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/0A020ACD-F116-E511-BD2F-02163E0137CC.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/0AB559C0-F116-E511-8CB2-02163E01261E.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/0CF23081-6413-E511-8B5A-02163E011DB6.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/1610FFBD-F116-E511-B20A-02163E0135E8.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/16DC4E80-E116-E511-AC5E-02163E01386E.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/1812EEE4-F516-E511-A5CF-02163E011B38.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/18245C92-6213-E511-A3EB-02163E013471.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/1A034483-E116-E511-98BE-02163E011BF3.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/2055348B-6213-E511-B367-02163E011DBC.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/208BEBE4-F416-E511-8919-02163E013401.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/246EAF4C-6313-E511-8894-02163E0146D2.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/261508C3-F116-E511-9BC2-02163E014745.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/26E4B1E8-EE16-E511-864A-02163E011B81.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/2CAFD024-6713-E511-B892-02163E012808.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/34676B9F-F716-E511-B56F-02163E0139C0.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/34A75888-E116-E511-9094-02163E011833.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/368EE503-F016-E511-B36A-02163E0135A3.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/36C3DD6A-6413-E511-80AC-02163E0136A7.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/3A0AF501-FE16-E511-992F-02163E011A35.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/3C708265-F016-E511-9889-02163E013907.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/40B999BE-F116-E511-ADE1-02163E012213.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/42E4146F-EE16-E511-ADD1-02163E012213.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/484A04C0-F116-E511-9FC4-02163E014284.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/50852AE0-E016-E511-BE6D-02163E011C8A.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/52FA7D0B-F016-E511-B622-02163E0141A0.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/5601738D-6213-E511-9317-02163E011DBC.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/62C3C066-6313-E511-BBBB-02163E011F63.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/62DBBC7B-E116-E511-A539-02163E013926.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/64410305-F016-E511-9F32-02163E0138CE.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/661C3514-F016-E511-AA9F-02163E011AF0.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/680E2C41-6313-E511-BAAE-02163E014155.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/6E1EF7BE-F116-E511-85A3-02163E011A5D.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/6E256EBE-F116-E511-B641-02163E0134E8.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/70A1ACBB-F116-E511-93B3-02163E01440D.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/70D03E01-F016-E511-9327-02163E01413B.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/72BA91BB-F116-E511-82D6-02163E01366E.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/76FE4804-6213-E511-93B9-02163E011BE1.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/7885E5C3-6313-E511-BBC1-02163E01189C.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/7AEA7104-F016-E511-805A-02163E0133A0.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/807F2817-6213-E511-96FD-02163E012AED.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/82EB3B2D-F916-E511-8D24-02163E01239B.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/82F7DA0E-E016-E511-802F-02163E0124F3.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/841EAD03-F016-E511-95B3-02163E0119CE.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/866A1A6D-EE16-E511-998F-02163E013571.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/8C4083C0-F116-E511-9BD8-02163E0134D1.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/8E01C68E-6213-E511-BB72-02163E011B58.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/8ED21E01-F016-E511-8190-02163E01444B.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/8ED5707E-E116-E511-B09B-02163E011E0A.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/988EFB8F-6213-E511-BF64-02163E013692.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/9E225506-F016-E511-96BD-02163E012213.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/A27485C9-F116-E511-9DCD-02163E01207C.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/A6876D03-F016-E511-8FA7-02163E011EDB.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/A8D41C0B-E016-E511-9FF5-02163E014495.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/AAEE46BD-F116-E511-A9F1-02163E014592.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/ACA49744-EE16-E511-8BF5-02163E0138C3.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/AEA400BD-F116-E511-AB36-02163E01382A.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/B2508106-6213-E511-A41C-02163E011942.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/B26BA909-F016-E511-9D74-02163E013864.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/B46C311A-F016-E511-9566-02163E012351.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/B644804B-6213-E511-9CCD-02163E01453C.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/B6C90B50-F416-E511-9737-02163E0133BE.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/B88F4A07-F016-E511-A110-02163E01339A.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/BCC77148-6313-E511-B13C-02163E011942.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/BE4C470C-E016-E511-8E9B-02163E011B3F.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/C0F76E09-F016-E511-9B45-02163E011FD4.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/C29F2AC0-F116-E511-9665-02163E0135FD.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/C2F868C9-F116-E511-9F20-02163E0123FE.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/C6344862-DF16-E511-B26F-02163E012AF9.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/C88368ED-F116-E511-9422-02163E011D12.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/C8FFF799-EE16-E511-B018-02163E0133BE.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/CA8F0B3C-6913-E511-AC02-02163E0138D3.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/CCCD5966-EE16-E511-B5B4-02163E011B15.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/CE4E274E-F216-E511-B7E0-02163E011BBE.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/CEB2BEBC-F116-E511-920E-02163E014289.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/D028594E-EE16-E511-A1EF-02163E011E07.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/D0500D8E-6213-E511-8423-02163E0141D2.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/D27C4CC0-F116-E511-934A-02163E011A59.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/D28BB003-F016-E511-985D-02163E01194B.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/D4840D0C-E016-E511-BD45-02163E013692.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/D673B4D0-F116-E511-9669-02163E011C33.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/D860FD08-6213-E511-A341-02163E01199C.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/DC463C7D-EE16-E511-AFE0-02163E011BD8.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/E06DEE5B-6813-E511-A479-02163E0119D3.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/E26486BB-F116-E511-9FAB-02163E013418.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/E6BBAAC3-F116-E511-9F9C-02163E0133C2.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/E89F3AD0-F116-E511-B3A6-02163E011CE4.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/F069D519-F016-E511-A1BE-02163E013673.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/F281EC62-DF16-E511-B45E-02163E011E79.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/F8069A61-DF16-E511-82E2-02163E0135A1.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/FA1727C3-F116-E511-A0E1-02163E01365F.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/FAA91A08-F016-E511-AFE5-02163E012180.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/FABD91CB-F116-E511-87C5-02163E011BA7.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/FEBF893E-3314-E511-9604-02163E014172.root",
      # "/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/247/934/00000/FEE1197C-E116-E511-9C1E-02163E0141CF.root"
        
      # 247324 0 Tesla
      # '/store/user/hvanhaev/ZeroBias1/Run2015A-v1_RERECO_Run247324_GR_P_V54_withCustomCond-v1/150608_213851/0000/output_data_rereco_88.root',
      # '/store/user/hvanhaev/ZeroBias1/Run2015A-v1_RERECO_Run247324_GR_P_V54_withCustomCond-v1/150608_213851/0000/output_data_rereco_105.root',
      # '/store/user/hvanhaev/ZeroBias1/Run2015A-v1_RERECO_Run247324_GR_P_V54_withCustomCond-v1/150608_213851/0000/output_data_rereco_26.root',
      # '/store/user/hvanhaev/ZeroBias1/Run2015A-v1_RERECO_Run247324_GR_P_V54_withCustomCond-v1/150608_213851/0000/output_data_rereco_82.root',
     


      )
     
     
)

# Geometry and Detector Conditions
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
# if isData: process.GlobalTag = GlobalTag(process.GlobalTag, '76X_dataRun2_v16', '')
if isData: process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data', '')
if not isData: process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')
# print "process.GlobalTag" ,process.GlobalTag.globaltag

process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")


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
if isData:
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
if isData:
    process = CommonFSQFramework.Core.customizePAT.addPath(process, process.PixelRecHits)
    
process = CommonFSQFramework.Core.customizePAT.addPath(process, process.StripMatchedRecHits)
process = CommonFSQFramework.Core.customizePAT.addPath(process, process.PFClustersHF)
process = CommonFSQFramework.Core.customizePAT.addTreeProducer(process, process.EflowTree)
