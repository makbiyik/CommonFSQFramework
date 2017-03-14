#!/bin/bash
#
export SmallXAnaDefFile="/afs/cern.ch/work/m/makbiyik/public/CMSSW/CMSSW_7_6_3_patch2/src/CommonFSQFramework/Core/test/DiffractiveCrossSection/MyAnalysis.py"
export SmallXAnaVersion="CommonFSQFramework.Skim.Samples_Run2015A_B0T_lowPU_14102015"
#0tesla
# export SmallXAnaVersion="CommonFSQFramework.Skim.Samples_RunIILowPU_0T_20062015"

#38tesla runRun247324
#export SmallXAnaVersion="CommonFSQFramework.Skim.Samples_RunIILowPU_38T_18082015"
source /cvmfs/cms.cern.ch/crab3/crab.sh
grid-proxy-init
voms-proxy-init --voms cms:/cms/dcms