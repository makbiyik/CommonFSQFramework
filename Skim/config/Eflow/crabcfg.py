from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.workArea = 'crab_projects'
config.User.voGroup = 'dcms'
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'treemaker_Eflow_74X.py'

config.section_("Data")
config.Data.inputDataset = '/A/B/C'
config.Data.inputDBS = 'global'

# config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased' # alt: LumiBased                                                                                
config.Data.unitsPerJob = 200000
# config.Data.totalUnits = 10000 # havent worked last time, use lumi mask?                                                          
#config.Data.lumiMask = "CommonFSQFramework/Skim/lumi/Run2015A_lowPU_B0T.json"
#config.Data.dbsUrl = "global"                                                                                                      
config.Data.allowNonValidInputDataset = True

config.Data.publication = False
# config.Data.publishDataName = 'MA_Diffractive'                                                                                    

config.section_("Site")
config.Site.whitelist = ['T2_CH_*','T2_DE_*']
# config.Site.storageSite = 'T2_CH_CERN'
# config.Data.outLFNDirBase = '/store/group/phys_heavyions/cwohrman/CFF/CastorMuon'
config.Site.storageSite = 'T2_DE_RWTH'

