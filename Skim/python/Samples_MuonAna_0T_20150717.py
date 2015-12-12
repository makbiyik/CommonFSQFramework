anaVersion="MuonAna_0T_20150717"
anaType="MuonAna_0T"

cbSmartCommand="smartCopy"
cbSmartBlackList=""
cbWMS="https://wmscms.cern.ch:7443/glite_wms_wmproxy_server"
skimEfficiencyMethod="getSkimEff"

sam = {}

# CFF Skim using interfill data from run 2015A
# No HLT filter selection was done
sam["data_MinimumBias_Run2015A"]={}
sam["data_MinimumBias_Run2015A"]["crabJobs"]=1609
sam["data_MinimumBias_Run2015A"]["GT"]='GR_R_75_V5A'
sam["data_MinimumBias_Run2015A"]["name"]='data_MinimumBias_Run2015A'
sam["data_MinimumBias_Run2015A"]["isData"]=True
sam["data_MinimumBias_Run2015A"]["numEvents"]=80446390
sam["data_MinimumBias_Run2015A"]["pathSE"]='srm://srm-eoscms.cern.ch:8443/srm/v2/server?SFN=/eos/cms/store/group/phys_heavyions/cwohrman/CFF/CastorMuon/MinimumBias/MuonAna_0T_20150717_data_MinimumBias_Run2015A/150717_095008/0000/'
sam["data_MinimumBias_Run2015A"]["pathTrees"]='/XXXTMFTTree/store/group/phys_heavyions/cwohrman/CFF/CastorMuon/MinimumBias/MuonAna_0T_20150717_data_MinimumBias_Run2015A/150717_095008/0000//'
sam["data_MinimumBias_Run2015A"]["json"]='CommonFSQFramework/Skim/lumi/MinBias_CastorMuonRuns_v2.json'
sam["data_MinimumBias_Run2015A"]["lumiMinBias"]=-1
sam["data_MinimumBias_Run2015A"]["XS"]=-1
sam["data_MinimumBias_Run2015A"]["pathPAT"]='/XXXTMFPAT/store/group/phys_heavyions/cwohrman/CFF/CastorMuon/MinimumBias/MuonAna_0T_20150717_data_MinimumBias_Run2015A/150717_095008/0000//'
sam["data_MinimumBias_Run2015A"]["DS"]='/MinimumBias/Run2015A-PromptReco-v1/RECO'

# CFF Skim using interfill data from run 2015A
# Filtered on CastorMuon HLT path:
#     HLT_L1CastorMuon_v1
#  OR HLT_L1Tech59_CASTORHaloMuon_v1
sam["data_MinimumBias_MuonHLTSkim_Run2015A"]={}
sam["data_MinimumBias_MuonHLTSkim_Run2015A"]["crabJobs"]=1609
sam["data_MinimumBias_MuonHLTSkim_Run2015A"]["GT"]='GR_R_75_V5A'
sam["data_MinimumBias_MuonHLTSkim_Run2015A"]["name"]='data_MinimumBias_MuonHLTSkim_Run2015A'
sam["data_MinimumBias_MuonHLTSkim_Run2015A"]["isData"]=True
sam["data_MinimumBias_MuonHLTSkim_Run2015A"]["numEvents"]=80446390
sam["data_MinimumBias_MuonHLTSkim_Run2015A"]["pathSE"]='srm://srm-eoscms.cern.ch:8443/srm/v2/server?SFN=/eos/cms/store/group/phys_heavyions/cwohrman/CFF/CastorMuon/MinimumBias/MuonAna_0T_20150717_data_MinimumBias_Run2015A/151030_111657/0000/'
sam["data_MinimumBias_MuonHLTSkim_Run2015A"]["pathTrees"]='/XXXTMFTTree/store/group/phys_heavyions/cwohrman/CFF/CastorMuon/MinimumBias/MuonAna_0T_20150717_data_MinimumBias_Run2015A/151030_111657/0000//'
sam["data_MinimumBias_MuonHLTSkim_Run2015A"]["json"]='CommonFSQFramework/Skim/lumi/MinBias_CastorMuonRuns_v2.json'
sam["data_MinimumBias_MuonHLTSkim_Run2015A"]["lumiMinBias"]=-1
sam["data_MinimumBias_MuonHLTSkim_Run2015A"]["XS"]=-1
sam["data_MinimumBias_MuonHLTSkim_Run2015A"]["pathPAT"]='/XXXTMFPAT/store/group/phys_heavyions/cwohrman/CFF/CastorMuon/MinimumBias/MuonAna_0T_20150717_data_MinimumBias_Run2015A/151030_111657/0000//'
sam["data_MinimumBias_MuonHLTSkim_Run2015A"]["DS"]='/MinimumBias/Run2015A-PromptReco-v1/RECO'

# CFF Skim using interfill data from run 2015E
# during pp-Reference-Run
# This data is stored in the Cosmic dataset therefore it needed to run 
# on RAW data (Cosmics/RECO has no Castor RecHit producer included). 
# Need also to copy dataset from tape to T2_BE_IIHE to access it.
# MagnetField: Undefined 
#              (Most propable 4T but in the end also 0T events could went in)
# Filtered on CastorMuon HLT path:
#     HLT_L1Tech59_CastorMuon_v1
sam["data_Cosmics_MuonHLTSkim_Run2015E"]={}
sam["data_Cosmics_MuonHLTSkim_Run2015E"]["crabJobs"]=232
sam["data_Cosmics_MuonHLTSkim_Run2015E"]["GT"]='75X_dataRun2_Prompt_ppAt5TeV_v0'
sam["data_Cosmics_MuonHLTSkim_Run2015E"]["name"]='data_Cosmics_MuonHLTSkim_Run2015E'
sam["data_Cosmics_MuonHLTSkim_Run2015E"]["isData"]=True
sam["data_Cosmics_MuonHLTSkim_Run2015E"]["numEvents"]=4486825
sam["data_Cosmics_MuonHLTSkim_Run2015E"]["pathSE"]='srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/cwohrman/Cosmics/MuonAna_0T_20150717_data_Cosmics_MuonHLTSkim_Run2015E/151126_133520/0000/'
sam["data_Cosmics_MuonHLTSkim_Run2015E"]["pathTrees"]='/XXXTMFTTree/tier2/store/user/cwohrman/Cosmics/MuonAna_0T_20150717_data_Cosmics_MuonHLTSkim_Run2015E/151126_133520/0000/'
sam["data_Cosmics_MuonHLTSkim_Run2015E"]["json"]='CommonFSQFramework/Skim/lumi/Cosmics_CastorMuonRuns.json'
sam["data_Cosmics_MuonHLTSkim_Run2015E"]["lumiMinBias"]=-1
sam["data_Cosmics_MuonHLTSkim_Run2015E"]["XS"]=-1
sam["data_Cosmics_MuonHLTSkim_Run2015E"]["pathPAT"]='/XXXTMFPAT/tier2/store/user/cwohrman/Cosmics/MuonAna_0T_20150717_data_Cosmics_MuonHLTSkim_Run2015E/151126_133520/0000/store/group/phys_heavyions/cwohrman/CFF/CastorMuon/Cosmics/MuonAna_0T_20150717_data_Cosmics_MuonHLTSkim_Run2015E/151124_172833/0000//'
sam["data_Cosmics_MuonHLTSkim_Run2015E"]["DS"]='/Cosmics/Run2015E-v1/RAW'


# CFF Skim using interfill data from run 2015E
# during pp-Reference-Run
# This data is stored in the Cosmic dataset therefore it needed to run 
# on RAW data (Cosmics/RECO has no Castor RecHit producer included). 
# Need also to copy dataset from tape to T2_BE_IIHE to access it.
# MagnetField: 4T
# Filtered on CastorMuon HLT path:
#     HLT_L1Tech59_CastorMuon_v1
sam["data_Cosmics_MuonHLTSkim_2015E_4T"]={}
sam["data_Cosmics_MuonHLTSkim_2015E_4T"]["crabJobs"]=232
sam["data_Cosmics_MuonHLTSkim_2015E_4T"]["GT"]='75X_dataRun2_Prompt_ppAt5TeV_v0'
sam["data_Cosmics_MuonHLTSkim_2015E_4T"]["name"]='data_Cosmics_MuonHLTSkim_2015E_4T'
sam["data_Cosmics_MuonHLTSkim_2015E_4T"]["isData"]=True
sam["data_Cosmics_MuonHLTSkim_2015E_4T"]["numEvents"]=4486825
sam["data_Cosmics_MuonHLTSkim_2015E_4T"]["pathSE"]='srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/cwohrman/CFF/CastorMuon/Cosmics/MuonAna_0T_20150717_data_Cosmics_MuonHLTSkim_2015E_4T/151210_095015/0000/'
sam["data_Cosmics_MuonHLTSkim_2015E_4T"]["pathTrees"]='/XXXTMFTTree/tier2/store/user/cwohrman/CFF/CastorMuon/Cosmics/MuonAna_0T_20150717_data_Cosmics_MuonHLTSkim_2015E_4T/151210_095015/0000//'
sam["data_Cosmics_MuonHLTSkim_2015E_4T"]["json"]='CommonFSQFramework/Skim/lumi/Cosmics_CastorMuonRuns_2015E_4T.json'
sam["data_Cosmics_MuonHLTSkim_2015E_4T"]["lumiMinBias"]=-1
sam["data_Cosmics_MuonHLTSkim_2015E_4T"]["XS"]=-1
sam["data_Cosmics_MuonHLTSkim_2015E_4T"]["pathPAT"]='/XXXTMFPAT/tier2/store/user/cwohrman/CFF/CastorMuon/Cosmics/MuonAna_0T_20150717_data_Cosmics_MuonHLTSkim_2015E_4T/151210_095015/0000//'
sam["data_Cosmics_MuonHLTSkim_2015E_4T"]["DS"]='/Cosmics/Run2015E-v1/RAW'

# CFF Skim using interfill data from run HI 2015E
# the first part of HI data
# This data is stored in the Cosmic dataset therefore it needed to run 
# on RAW data (Cosmics/RECO has no Castor RecHit producer included). 
# Need also to copy dataset from tape to T2_BE_IIHE to access it.
# MagnetField: 0T
# Filtered on CastorMuon HLT path:
#     HLT_L1Tech59_CastorMuon_v1
sam["data_Cosmics_MuonHLTSkim_2015E_0T"]={}
sam["data_Cosmics_MuonHLTSkim_2015E_0T"]["crabJobs"]=232
sam["data_Cosmics_MuonHLTSkim_2015E_0T"]["GT"]='75X_dataRun2_Prompt_ppAt5TeV_v0'
sam["data_Cosmics_MuonHLTSkim_2015E_0T"]["name"]='data_Cosmics_MuonHLTSkim_2015E_0T'
sam["data_Cosmics_MuonHLTSkim_2015E_0T"]["isData"]=True
sam["data_Cosmics_MuonHLTSkim_2015E_0T"]["numEvents"]=4486825
sam["data_Cosmics_MuonHLTSkim_2015E_0T"]["pathSE"]='srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/cwohrman/CFF/CastorMuon/Cosmics/MuonAna_0T_20150717_data_Cosmics_MuonHLTSkim_2015E_0T/151210_195631/0000/'
sam["data_Cosmics_MuonHLTSkim_2015E_0T"]["pathTrees"]='/XXXTMFTTree/tier2/store/user/cwohrman/CFF/CastorMuon/Cosmics/MuonAna_0T_20150717_data_Cosmics_MuonHLTSkim_2015E_0T/151210_195631/0000//'
sam["data_Cosmics_MuonHLTSkim_2015E_0T"]["json"]='CommonFSQFramework/Skim/lumi/Cosmics_CastorMuonRuns_2015E_0T.json'
sam["data_Cosmics_MuonHLTSkim_2015E_0T"]["lumiMinBias"]=-1
sam["data_Cosmics_MuonHLTSkim_2015E_0T"]["XS"]=-1
sam["data_Cosmics_MuonHLTSkim_2015E_0T"]["pathPAT"]='/XXXTMFPAT/tier2/store/user/cwohrman/CFF/CastorMuon/Cosmics/MuonAna_0T_20150717_data_Cosmics_MuonHLTSkim_2015E_0T/151210_195631/0000//'
sam["data_Cosmics_MuonHLTSkim_2015E_0T"]["DS"]='/Cosmics/Run2015E-v1/RAW'


# CFF Skim using interfill data from run HI 2015E
# This data is stored in the Cosmic dataset therefore it needed to run 
# on RAW data (Cosmics/RECO has no Castor RecHit producer included). 
# Dataset need to be transfered on T2 Storage site
# MagnetField: 4T
# Filtered on CastorMuon HLT path:
#     HLT_L1Tech59_CastorMuon_v1
sam["data_Cosmics_MuonHLTSkim_HI2015E_4T"]={}
sam["data_Cosmics_MuonHLTSkim_HI2015E_4T"]["crabJobs"]=232
sam["data_Cosmics_MuonHLTSkim_HI2015E_4T"]["GT"]='75X_dataRun2_Prompt_ppAt5TeV_v0'
sam["data_Cosmics_MuonHLTSkim_HI2015E_4T"]["name"]='data_Cosmics_MuonHLTSkim_HI2015E_4T'
sam["data_Cosmics_MuonHLTSkim_HI2015E_4T"]["isData"]=True
sam["data_Cosmics_MuonHLTSkim_HI2015E_4T"]["numEvents"]=4486825
sam["data_Cosmics_MuonHLTSkim_HI2015E_4T"]["pathSE"]='srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/cwohrman/CFF/CastorMuon/Cosmics/MuonAna_0T_20150717_data_Cosmics_MuonHLTSkim_2015E_4T/151209_200510/0000/'
sam["data_Cosmics_MuonHLTSkim_HI2015E_4T"]["pathTrees"]='/XXXTMFTTree/tier2/store/user/cwohrman/CFF/CastorMuon/Cosmics/MuonAna_0T_20150717_data_Cosmics_MuonHLTSkim_2015E_4T/151209_200510/0000//'
sam["data_Cosmics_MuonHLTSkim_HI2015E_4T"]["json"]='CommonFSQFramework/Skim/lumi/Cosmics_CastorMuonRuns_2015E_4T.json'
sam["data_Cosmics_MuonHLTSkim_HI2015E_4T"]["lumiMinBias"]=-1
sam["data_Cosmics_MuonHLTSkim_HI2015E_4T"]["XS"]=-1
sam["data_Cosmics_MuonHLTSkim_HI2015E_4T"]["pathPAT"]='/XXXTMFPAT/tier2/store/user/cwohrman/CFF/CastorMuon/Cosmics/MuonAna_0T_20150717_data_Cosmics_MuonHLTSkim_2015E_4T/151209_200510/0000//'
sam["data_Cosmics_MuonHLTSkim_HI2015E_4T"]["DS"]='/Cosmics/HIRun2015-v1/RAW'


# CFF Skim using interfill data from run HI 2015E
# with changed interfill HV set to pp-HV
# This data is stored in the Cosmic dataset therefore it needed to run 
# on RAW data (Cosmics/RECO has no Castor RecHit producer included). 
# Dataset need to be transfered on T2 Storage site
# MagnetField: 4T
# Filtered on CastorMuon HLT path:
#     HLT_L1Tech59_CastorMuon_v1
sam["data_Cosmics_MuonHLTSkim_HI2015E_ppHVInterfill"]={}
sam["data_Cosmics_MuonHLTSkim_HI2015E_ppHVInterfill"]["crabJobs"]=232
sam["data_Cosmics_MuonHLTSkim_HI2015E_ppHVInterfill"]["GT"]='75X_dataRun2_Prompt_ppAt5TeV_v0'
sam["data_Cosmics_MuonHLTSkim_HI2015E_ppHVInterfill"]["name"]='data_Cosmics_MuonHLTSkim_HI2015E_ppHVInterfill'
sam["data_Cosmics_MuonHLTSkim_HI2015E_ppHVInterfill"]["isData"]=True
sam["data_Cosmics_MuonHLTSkim_HI2015E_ppHVInterfill"]["numEvents"]=4486825
# sam["data_Cosmics_MuonHLTSkim_HI2015E_ppHVInterfill"]["pathSE"]='srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/cwohrman/CFF/CastorMuon/Cosmics/MuonAna_0T_20150717_data_Cosmics_MuonHLTSkim_2015E_4T/151209_200510/0000/'
# sam["data_Cosmics_MuonHLTSkim_HI2015E_ppHVInterfill"]["pathTrees"]='/XXXTMFTTree/tier2/store/user/cwohrman/CFF/CastorMuon/Cosmics/MuonAna_0T_20150717_data_Cosmics_MuonHLTSkim_2015E_4T/151209_200510/0000//'
sam["data_Cosmics_MuonHLTSkim_HI2015E_ppHVInterfill"]["json"]='CommonFSQFramework/Skim/lumi/Cosmics_CastorMuonRuns_HIRun2015E_ppHVInterfill.json'
sam["data_Cosmics_MuonHLTSkim_HI2015E_ppHVInterfill"]["lumiMinBias"]=-1
sam["data_Cosmics_MuonHLTSkim_HI2015E_ppHVInterfill"]["XS"]=-1
# sam["data_Cosmics_MuonHLTSkim_HI2015E_ppHVInterfill"]["pathPAT"]='/XXXTMFPAT/tier2/store/user/cwohrman/CFF/CastorMuon/Cosmics/MuonAna_0T_20150717_data_Cosmics_MuonHLTSkim_2015E_4T/151209_200510/0000//'
sam["data_Cosmics_MuonHLTSkim_HI2015E_ppHVInterfill"]["DS"]='/Cosmics/HIRun2015-v1/RAW'


def fixLocalPaths(sam):
        import os,imp
        if "SmallXAnaDefFile" not in os.environ:
            print "Please set SmallXAnaDefFile environment variable:"
            print "export SmallXAnaDefFile=FullPathToFile"
            raise Exception("Whooops! SmallXAnaDefFile env var not defined")

        anaDefFile = os.environ["SmallXAnaDefFile"]
        mod_dir, filename = os.path.split(anaDefFile)
        mod, ext = os.path.splitext(filename)
        f, filename, desc = imp.find_module(mod, [mod_dir])
        mod = imp.load_module(mod, f, filename, desc)

        localBasePathPAT = mod.PATbasePATH
        localBasePathTrees = mod.TTreeBasePATH

        for s in sam:
            if "pathPAT" in sam[s]:
                sam[s]["pathPAT"] = sam[s]["pathPAT"].replace("XXXTMFPAT", localBasePathPAT)
            if "pathTrees" in sam[s]:
                sam[s]["pathTrees"] = sam[s]["pathTrees"].replace("XXXTMFTTree", localBasePathTrees)
            #print sam[s]["pathPAT"]
            #print sam[s]["pathTrees"]
        return sam
sam = fixLocalPaths(sam)
