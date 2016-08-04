#!/usr/bin/env python


import CommonFSQFramework.Core.ExampleProofReader
#from rootpy.math.physics.vector import LorentzVector
import sys, os, time
sys.path.append(os.path.dirname(__file__))

import ROOT
ROOT.gROOT.SetBatch(True)
import ParticleDataTool as pd

from collections import Counter

from ROOT import edm

from array import *
import math
import numpy as np
from math import cosh
from math import sinh
from math import sin
from math import cos
from math import tan
from math import pi
from math import sqrt
from math import log10

from BadChannels2015 import badChannelsSecMod


def compareTracketa(first,second):
    if first[0] > second[0]: return 1
    if first[0] == second[0]: return 0
    if first[0] < second[0]: return -1


def compareGeneta(first,second):
    if first[0].eta() > second[0].eta(): return 1
    if first[0].eta() == second[0].eta(): return 0
    if first[0].eta() < second[0].eta(): return -1
class DiffractiveAndTrack(CommonFSQFramework.Core.ExampleProofReader.ExampleProofReader):
    def init(self,maxEvents = None):
        
        self.maxEvents = maxEvents
        self.hist = {}
        self.hist["hNentries"] = ROOT.TH1F("hNentries","hNentries",10, 0, 20)
        self.hist["BunchCrossing"] = ROOT.TH1F("BunchCrossing", "BunchCrossing",  3600, 0-0.5, 3600-0.5)
        self.hist["Runs"] =  ROOT.TH1F("Runs", "Runs",  2000, 246000-0.5, 278000-0.5)
        self.hist["HFEnergy"] = ROOT.TH1F("HFEnergy","HFEnergy",100, 0, 200)
        self.hist["Hist_sum_CAS_E"] = ROOT.TH1F("Hist_sum_CAS_E", "Hist_sum_CAS_E" ,100,0,600)
        self.hist["hParticleCounts"] = ROOT.TH1F("hParticleCounts","hParticleCounts",10, 0, 20) 
        self.hist["Hist_Angle"] = ROOT.TH1F("Hist_Angle", "Hist_Angle", 200, 0, 5)    
        self.hist["Hist_2Drecogen_EnergyX"] = ROOT.TH2D("Hist_2Drecogen_EnergyX", "Hist_2Drecogen_EnergyX", 100, 0, 8000,100, 0, 8000)    
        self.hist["Hist_2Drecogen_EnergyY"] = ROOT.TH2D("Hist_2Drecogen_EnergyY", "Hist_2Drecogen_EnergyY", 100, 0, 8000,100, 0, 8000)


        nEtaBins = 8
        EtaBins = array('d',[-6.6, -5.2, -3.2, -2.8, -1.4, 1.4, 2.8, 3.2, 5.2])
    

        NbrVtxzBins = 50
        BinVtxzMin = -20
        BinVtxzMax = 20


        self.hist["Hist_NrVtx"] = ROOT.TH1F("Hist_NrVtx_","Hist_NrVtx",NbrVtxzBins,BinVtxzMin, BinVtxzMax)  

        NbrEtaBins = 50
        BinEtaMin = -5.5
        BinEtaMax = 4.5
        NbrDetaBins = 50
        BinDetaMin = 0
        BinDetaMax = 8
       

        self.hist["Hist_GPCut_Eta_Min"] =  ROOT.TH1F("Hist_GPCut_Eta_Min", "Hist_GPCut_Eta_Min", NbrEtaBins, BinEtaMin, BinEtaMax)
        self.hist["Hist_GPCut_Eta_Max"] =  ROOT.TH1F("Hist_GPCut_Eta_Max", "Hist_GPCut_Eta_Max", NbrEtaBins, BinEtaMin, BinEtaMax)
        self.hist["Hist_GPCut_DeltaMax"] =  ROOT.TH1F("Hist_GPCut_DeltaMax", "Hist_GPCut_DeltaMax", NbrDetaBins, BinDetaMin, BinDetaMax)
        self.hist["Hist_GPCut_DeltaZero"] = ROOT.TH1F("Hist_GPCut_DeltaZero", "Hist_GPCut_DeltaZero", NbrDetaBins, BinDetaMin, BinDetaMax)
       
        self.hist["Hist_Eta_Min"] =  ROOT.TH1F("Hist_Eta_Min", "Hist_Eta_Min", NbrEtaBins, BinEtaMin, BinEtaMax)
        self.hist["Hist_Eta_Max"] =  ROOT.TH1F("Hist_Eta_Max", "Hist_Eta_Max", NbrEtaBins, BinEtaMin, BinEtaMax)
        self.hist["Hist_Eta_Delta"] =  ROOT.TH1F("Hist_Eta_Delta", "Hist_Eta_Delta", NbrDetaBins, BinDetaMin, BinDetaMax)
        self.hist["Hist_Eta_DeltaZero"] = ROOT.TH1F("Hist_Eta_DeltaZero", "Hist_Eta_DeltaZero", NbrDetaBins, BinDetaMin, BinDetaMax)
       
         

        
        self.hist["Hist_Eta_DeltaMax"] =  ROOT.TH1F("Hist_Eta_DeltaMax", "Hist_Eta_DeltaMax", NbrDetaBins, BinDetaMin, BinDetaMax)
        self.hist["Hist_2D_genreco_Deltapos"] = ROOT.TH2D("Hist_2D_genreco_Deltapos", "Hist_2D_genreco_Deltapos", NbrEtaBins, BinEtaMin, BinEtaMax,NbrEtaBins, BinEtaMin, BinEtaMax)
        # Gen PArticle 
        self.hist["Hist_2D_recogen_Mean"] = ROOT.TH2D("Hist_2D_recogen_Mean","Hist_2D_recogen_Mean",NbrEtaBins, BinEtaMin, BinEtaMax,NbrEtaBins, BinEtaMin, BinEtaMax)
        self.hist["Hist_GP_Eta_Min"] =  ROOT.TH1F("Hist_GP_Eta_Min", "Hist_GP_Eta_Min", NbrEtaBins, BinEtaMin, BinEtaMax)
        self.hist["Hist_GP_Eta_Max"] =  ROOT.TH1F("Hist_GP_Eta_Max", "Hist_GP_Eta_Max", NbrEtaBins, BinEtaMin, BinEtaMax)
        self.hist["Hist_GP_Eta_Delta"] =  ROOT.TH1F("Hist_GP_Eta_Delta","Hist_GP_Eta_Delta", NbrDetaBins, BinDetaMin, BinDetaMax)
        self.hist["Hist_GP_Eta_DeltaZero"] =  ROOT.TH1F("Hist_GP_Eta_DeltaZero", "Hist_GP_Eta_DeltaZero", NbrDetaBins, BinDetaMin, BinDetaMax)
        self.hist["Hist_GP_Eta_DeltaMax"] =  ROOT.TH1F("Hist_GP_Eta_DeltaMax", "Hist_GP_Eta_DeltaMax", NbrDetaBins, BinDetaMin, BinDetaMax)
        self.hist["Hist_Deltazero_deltagenreco"] =  ROOT.TH1F("Hist_Deltazero_deltagenreco", "Hist_Deltazero_deltagenreco", NbrDetaBins, -10, BinDetaMax)
        self.hist["Hist_2D_recogen_DeltaZero"] = ROOT.TH2D("Hist_2D_recogen_DeltaZero","Hist_2D_recogen_DeltaZero", NbrDetaBins,BinDetaMin, BinDetaMax,NbrDetaBins,BinDetaMin, BinDetaMax);
        self.hist["Hist_2D_recogen_DeltaMax"] = ROOT.TH2D("Hist_2D_recogen_DeltaMax","Hist_2D_recogen_DeltaMax", NbrDetaBins,BinDetaMin, BinDetaMax,NbrDetaBins,BinDetaMin, BinDetaMax);
        self.hist["Hist_2D_recogen_EtaMiniumum"] = ROOT.TH2D("Hist_2D_recogen_EtaMiniumum","Hist_2D_recogen_EtaMiniumum",NbrEtaBins, BinEtaMin, BinEtaMax,NbrEtaBins, BinEtaMin, BinEtaMax)
        self.hist["Hist_2D_recogen_EtaMax"]= ROOT.TH2D("Hist_2D_recogen_EtaMax","Hist_2D_recogen_EtaMax",NbrEtaBins, BinEtaMin, BinEtaMax,NbrEtaBins, BinEtaMin, BinEtaMax)

        NbrSizeBins = 50
        BinSizeEMin = 0
        BinSizeEMax = 50
        
        self.hist["Hist_TrackCandClass"] = ROOT.TH1F("Hist_TrackCandClass","Hist_TrackCandClass",NbrSizeBins, BinSizeEMin,100)

        NbrPhiBins = 50
        BinPhiMin = -5
        BinPhiMax = 5

        self.hist["Hist_trkPhi"] = ROOT.TH1F("Hist_trkPhi","Hist_trkPhi",NbrPhiBins,  BinPhiMin, BinPhiMax)  
        self.hist["Hist_Eta"] = ROOT.TH1F("Hist_Eta","Hist_Eta",NbrEtaBins, BinEtaMin, BinEtaMax) 
        self.hist["Hist_reducedEta"] = ROOT.TH1F("Hist_reducedEta","Hist_reducedEta",NbrEtaBins, BinEtaMin, BinEtaMax)  
        self.hist["Hist_trkEta"] = ROOT.TH1F("Hist_trkEta","Hist_trkEta",NbrEtaBins, BinEtaMin, BinEtaMax)  
        self.hist["Hist_trkplusEta"] = ROOT.TH1F("Hist_trkplusEta","Hist_trkplusEta",NbrEtaBins, BinEtaMin, BinEtaMax) 
        NbrNtrackBins = 50
        BinNtrackMin = 0
        BinNtrackMax = 150
       
        NbrLogMBins = 70
        BinLogMMin = -3
        BinLogMMax = 5
        
        NbrPFEBins = 50
        BinPFEMin = 0
        BinPFEMax = 50

       
        self.hist["Hist_log10Mx"] =  ROOT.TH1F("Hist_log10Mx", "Hist_log10Mx", NbrLogMBins, BinLogMMin, BinLogMMax)
        self.hist["Hist_log10My"] =  ROOT.TH1F("Hist_log10My", "Hist_log10My", NbrLogMBins, BinLogMMin, BinLogMMax)  
        self.hist["Hist_2Dlog10MxMy"] =  ROOT.TH2D("Hist_2Dlog10MxMy", "Hist_2Dlog10MxMy", NbrLogMBins, BinLogMMin, BinLogMMax, NbrLogMBins, BinLogMMin, BinLogMMax)
        

        Process_ID = ["_NONE","_ND","_SD1","_SD2","_DD", "_CD"]
        
        self.hist["Hist_NTracks"] = ROOT.TH1F("Hist_NTracks","Hist_NTracks",NbrNtrackBins, BinNtrackMin, BinNtrackMax)
        self.hist["Hist_GP_Mx"] =  ROOT.TH1F("Hist_GP_Mx", "Hist_GP_Mx", NbrLogMBins, BinLogMMin, BinLogMMax)
        self.hist["Hist_GP_My"] =  ROOT.TH1F("Hist_GP_My", "Hist_GP_My", NbrLogMBins, BinLogMMin, BinLogMMax)  
        self.hist["Hist_GP_log10Mx"] =  ROOT.TH1F("Hist_GP_log10Mx", "Hist_GP_log10Mx", NbrLogMBins, BinLogMMin, BinLogMMax)
        self.hist["Hist_GP_log10My"] =  ROOT.TH1F("Hist_GP_log10My", "Hist_GP_log10My", NbrLogMBins, BinLogMMin, BinLogMMax)  
        self.hist["Hist_GP_2Dlog10MxMy"] =  ROOT.TH2D("Hist_GP_2Dlog10MxMy", "Hist_GP_2Dlog10MxMy", NbrLogMBins, BinLogMMin, BinLogMMax, NbrLogMBins, BinLogMMin, BinLogMMax)
       
        self.hist["Hist_Energy"] =  ROOT.TH1F("Hist_Energy", "Hist_Energy" , NbrPFEBins, BinPFEMin, BinPFEMax)
        self.hist["Hist_Energy_barrel"] =  ROOT.TH1F("Hist_Energy_barrel", "Hist_Energy_barrel" , NbrPFEBins, BinPFEMin, BinPFEMax)
        self.hist["Hist_Energy_endcap"] =  ROOT.TH1F("Hist_Energy_endcap", "Hist_Energy_endcap" , NbrPFEBins, BinPFEMin, BinPFEMax)
        self.hist["Hist_Energy_endcap_forwardtransition"] =  ROOT.TH1F("Hist_Energy_endcap_forwardtransition", "Hist_Energy_endcap_forwardtransition" , NbrPFEBins, BinPFEMin, BinPFEMax)
        self.hist["Hist_Energy_forward"] =  ROOT.TH1F("Hist_Energy_forward", "Hist_Energy_forward" , NbrPFEBins, BinPFEMin, BinPFEMax)
        self.hist["Hist_Energy_forwardplus"] =  ROOT.TH1F("Hist_Energy_forwardplus", "Hist_Energy_forwardplus" , NbrPFEBins, BinPFEMin, BinPFEMax)
        self.hist["Hist_Energy_forwardminus"] =  ROOT.TH1F("Hist_Energy_forwardminus", "Hist_Energy_forwardminus" , NbrPFEBins, BinPFEMin, BinPFEMax)
        self.hist["Hist_Energy_Castor"] =  ROOT.TH1F("Hist_Energy_Castor", "Hist_Energy_Castor" , NbrPFEBins, BinPFEMin, BinPFEMax)
 
        self.hist["Hist_reducedEnergy"] =  ROOT.TH1F("Hist_reducedEnergy", "Hist_reducedEnergy" , NbrPFEBins, BinPFEMin, BinPFEMax)
        self.hist["Hist_reducedEnergy_barrel"] =  ROOT.TH1F("Hist_reducedEnergy_barrel", "Hist_reducedEnergy_barrel" , NbrPFEBins, BinPFEMin, BinPFEMax)
        self.hist["Hist_reducedEnergy_endcap"] =  ROOT.TH1F("Hist_reducedEnergy_endcap", "Hist_reducedEnergy_endcap" , NbrPFEBins, BinPFEMin, BinPFEMax)
        self.hist["Hist_reducedEnergy_endcap_forwardtransition"] =  ROOT.TH1F("Hist_reducedEnergy_endcap_forwardtransition", "Hist_reducedEnergy_endcap_forwardtransition" , NbrPFEBins, BinPFEMin, BinPFEMax)
        self.hist["Hist_reducedEnergy_forward"] =  ROOT.TH1F("Hist_reducedEnergy_forward", "Hist_reducedEnergy_forward" , NbrPFEBins, BinPFEMin, BinPFEMax)
        self.hist["Hist_reducedEnergy_forwardplus"] =  ROOT.TH1F("Hist_reducedEnergy_forwardplus", "Hist_reducedEnergy_forwardplus" , NbrPFEBins, BinPFEMin, BinPFEMax)
        self.hist["Hist_reducedEnergy_forwardminus"] =  ROOT.TH1F("Hist_reducedEnergy_forwardminus", "Hist_reducedEnergy_forwardminus" , NbrPFEBins, BinPFEMin, BinPFEMax)
        self.hist["Hist_reducedEnergy_Castor"] =  ROOT.TH1F("Hist_reducedEnergy_Castor", "Hist_reducedEnergy_Castor" , NbrPFEBins, BinPFEMin, BinPFEMax)
  

        NbrLogXiBins = 50
        BinLogXiMin = -11
        BinLogXiMax = -2

        NbrXiBins = 50
        BinXiMin = 0
        BinXiMax = 5

       
        self.hist["Hist_XiX"] =  ROOT.TH1F("Hist_XiX", "Hist_XiX", NbrXiBins, BinXiMin, BinXiMax)
        self.hist["Hist_XiY"] =  ROOT.TH1F("Hist_XiY", "Hist_XiY", NbrXiBins, BinXiMin, BinXiMax)
        NbrLogXiBins = 50
        BinLogXiMin = -11
        BinLogXiMax = 1
   
        self.hist["Hist_GP_log10Xi_DD"] =  ROOT.TH1F("Hist_GP_log10Xi_DD", "Hist_GP_log10Xi_DD", NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        self.hist["Hist_Reco_log10Xi_DD"] =  ROOT.TH1F("Hist_Reco_log10Xi_DD", "Hist_Reco_log10Xi_DD", NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        self.hist["Hist_2DRecoLogXi_DDGenLogXi_DD"] = ROOT.TH2D("Hist_2DRecoLogXi_DDGenLogXi_DD", "Hist_2DRecoLogXi_DDGenLogXi_DD", NbrLogXiBins, BinLogXiMin, BinLogXiMax, NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        self.hist["Hist_log10XiX"] =  ROOT.TH1F("Hist_log10XiX", "Hist_log10XiX", NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        self.hist["Hist_log10XiY"] =  ROOT.TH1F("Hist_log10XiY", "Hist_log10XiY", NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        self.hist["Hist_GP_log10XiX"] =  ROOT.TH1F("Hist_GP_log10XiX", "Hist_GP_log10XiX", NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        self.hist["Hist_GP_log10XiY"] =  ROOT.TH1F("Hist_GP_log10XiY", "Hist_GP_log10XiY", NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        self.hist["Hist_2Dlog10XiXXiY"] = ROOT.TH2D("Hist_2Dlog10XiXXiY", "Hist_2Dlog10XiXXiY", NbrLogXiBins, BinLogXiMin, BinLogXiMax, NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        self.hist["Hist_2DRecoLogXiXGenLogXiX"] = ROOT.TH2D("Hist_2DRecoLogXiXGenLogXiX", "Hist_2DRecoLogXiXGenLogXiX", NbrLogXiBins, BinLogXiMin, BinLogXiMax, NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        self.hist["Hist_2DRecoLogXiYGenLogXiY"] = ROOT.TH2D("Hist_2DRecoLogXiYGenLogXiY", "Hist_2DRecoLogXiYGenLogXiY", NbrLogXiBins, BinLogXiMin, BinLogXiMax, NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        self.hist["Hist_2DGPLogXiXLogXiY"] = ROOT.TH2D("Hist_2DGPLogXiXLogXiY", "Hist_2DGPLogXiXLogXiY", NbrLogXiBins, BinLogXiMin, BinLogXiMax, NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        self.hist["Hist_2D_FG2_RecoLogXiXGenLogXiX"] = ROOT.TH2D("Hist_2D_FG2_RecoLogXiXGenLogXiX", "Hist_2D_FG2_RecoLogXiXGenLogXiX", NbrLogXiBins, BinLogXiMin, BinLogXiMax, NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        self.hist["Hist_2D_FG2_RecoLogXiYGenLogXiY"] = ROOT.TH2D("Hist_2D_FG2_RecoLogXiYGenLogXiY", "Hist_2D_FG2_RecoLogXiYGenLogXiY", NbrLogXiBins, BinLogXiMin, BinLogXiMax, NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        self.hist["Hist_2D_FG1_RecoLogXiXGenLogXiX"] = ROOT.TH2D("Hist_2D_FG1_RecoLogXiXGenLogXiX", "Hist_2D_FG1_RecoLogXiXGenLogXiX", NbrLogXiBins, BinLogXiMin, BinLogXiMax, NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        self.hist["Hist_2D_FG1_RecoLogXiYGenLogXiY"] = ROOT.TH2D("Hist_2D_FG1_RecoLogXiYGenLogXiY", "Hist_2D_FG1_RecoLogXiYGenLogXiY", NbrLogXiBins, BinLogXiMin, BinLogXiMax, NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        self.hist["Hist_2D_CG_RecoLogXiXGenLogXiX"] = ROOT.TH2D("Hist_2D_CG_RecoLogXiXGenLogXiX", "Hist_2D_CG_RecoLogXiXGenLogXiX", NbrLogXiBins, BinLogXiMin, BinLogXiMax, NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        self.hist["Hist_2D_CG_RecoLogXiYGenLogXiY"] = ROOT.TH2D("Hist_2D_CG_RecoLogXiYGenLogXiY", "Hist_2D_CG_RecoLogXiYGenLogXiY", NbrLogXiBins, BinLogXiMin, BinLogXiMax, NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        self.hist["Hist_2D_FG2_2DGPLogXiXLogXiY"] = ROOT.TH2D("Hist_2D_FG2_2DGPLogXiXLogXiY", "Hist_2D_FG2_2DGPLogXiXLogXiY", NbrLogXiBins, BinLogXiMin, BinLogXiMax, NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        self.hist["Hist_2D_FG1_2DGPLogXiXLogXiY"] = ROOT.TH2D("Hist_2D_FG1_2DGPLogXiXLogXiY", "Hist_2D_FG1_2DGPLogXiXLogXiY", NbrLogXiBins, BinLogXiMin, BinLogXiMax, NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        self.hist["Hist_2D_CG_2DGPLogXiXLogXiY"] = ROOT.TH2D("Hist_2D_CG_2DGPLogXiXLogXiY", "Hist_2D_CG_2DGPLogXiXLogXiY", NbrLogXiBins, BinLogXiMin, BinLogXiMax, NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        
       



        for ip in Process_ID:
            self.hist["Hist_Eta_Min"+str(ip)] = ROOT.TH1D("Hist_Eta_Min"+str(ip),"Hist_Eta_Min ", NbrEtaBins, BinEtaMin, BinEtaMax)
            self.hist["Hist_Eta_Max"+str(ip)] = ROOT.TH1D("Hist_Eta_Max"+str(ip),"Hist_Eta_Max ", NbrEtaBins, BinEtaMin, BinEtaMax) 
            self.hist["Hist_Eta_Delta"+str(ip)] = ROOT.TH1D("Hist_Eta_Delta"+str(ip),"Hist_Eta_Delta ", NbrDetaBins, BinDetaMin, BinDetaMax)
            self.hist["Hist_Eta_DeltaZero"+str(ip)] = ROOT.TH1D("Hist_Eta_DeltaZero"+str(ip),"Hist_Eta_DeltaZero ", NbrDetaBins, BinDetaMin, BinDetaMax)
            self.hist["Hist_Eta"+str(ip)] =  ROOT.TH1F("Hist_Eta"+str(ip), "Hist_Eta"+str(ip), nEtaBins, EtaBins)
            self.hist["Hist_reducedEta"+str(ip)] =  ROOT.TH1F("Hist_reducedEta"+str(ip), "Hist_reducedEta"+str(ip), nEtaBins, EtaBins)
            self.hist["Hist_Eta_DeltaMax"+str(ip)] =  ROOT.TH1F("Hist_Eta_DeltaMax"+str(ip), "Hist_Eta_DeltaMax"+str(ip), NbrDetaBins, BinDetaMin, BinDetaMax)               
            
            self.hist["Hist_GPCut_Eta_Min"+str(ip)] = ROOT.TH1D("Hist_GPCut_Eta_Min"+str(ip),"Hist_GPCut_Eta_Min ", NbrEtaBins, BinEtaMin, BinEtaMax)
            self.hist["Hist_GPCut_Eta_Max"+str(ip)] = ROOT.TH1D("Hist_GPCut_Eta_Max"+str(ip),"Hist_GPCut_Eta_Max ", NbrEtaBins, BinEtaMin, BinEtaMax) 

            self.hist["Hist_GPCut_DeltaMax"+str(ip)] =  ROOT.TH1F("Hist_GPCut_DeltaMax"+str(ip), "Hist_GPCut_DeltaMax"+str(ip), NbrDetaBins, BinDetaMin, BinDetaMax)
            self.hist["Hist_GPCut_DeltaZero"+str(ip)] =  ROOT.TH1F("Hist_GPCut_DeltaZero"+str(ip), "Hist_GPCut_DeltaZero"+str(ip), NbrDetaBins, BinDetaMin, BinDetaMax)
            


            self.hist["Hist_Energy"+str(ip)] =  ROOT.TH1F("Hist_Energy"+str(ip), "Hist_Energy"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_Energy_barrel"+str(ip)] =  ROOT.TH1F("Hist_Energy_barrel"+str(ip), "Hist_Energy_barrel"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_Energy_endcap"+str(ip)] =  ROOT.TH1F("Hist_Energy_endcap"+str(ip), "Hist_Energy_endcap"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_Energy_endcap_forwardtransition"+str(ip)] =  ROOT.TH1F("Hist_Energy_endcap_forwardtransition"+str(ip), "Hist_Energy_endcap_forwardtransition"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_Energy_forward"+str(ip)] =  ROOT.TH1F("Hist_Energy_forward"+str(ip), "Hist_Energy_forward"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_Energy_forwardplus"+str(ip)] =  ROOT.TH1F("Hist_Energy_forwardplus"+str(ip), "Hist_Energy_forwardplus"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_Energy_forwardminus"+str(ip)] =  ROOT.TH1F("Hist_Energy_forwardminus"+str(ip), "Hist_Energy_forwardminus"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_Energy_Castor"+str(ip)] =  ROOT.TH1F("Hist_Energy_Castor"+str(ip), "Hist_Energy_Castor"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            
            self.hist["Hist_reducedEnergy"+str(ip)] =  ROOT.TH1F("Hist_reducedEnergy"+str(ip), "Hist_reducedEnergy"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_reducedEnergy_barrel"+str(ip)] =  ROOT.TH1F("Hist_reducedEnergy_barrel"+str(ip), "Hist_reducedEnergy_barrel"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_reducedEnergy_endcap"+str(ip)] =  ROOT.TH1F("Hist_reducedEnergy_endcap"+str(ip), "Hist_reducedEnergy_endcap"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_reducedEnergy_endcap_forwardtransition"+str(ip)] =  ROOT.TH1F("Hist_reducedEnergy_endcap_forwardtransition"+str(ip), "Hist_reducedEnergy_endcap_forwardtransition"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_reducedEnergy_forward"+str(ip)] =  ROOT.TH1F("Hist_reducedEnergy_forward"+str(ip), "Hist_reducedEnergy_forward"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_reducedEnergy_forwardplus"+str(ip)] =  ROOT.TH1F("Hist_reducedEnergy_forwardplus"+str(ip), "Hist_reducedEnergy_forwardplus"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_reducedEnergy_forwardminus"+str(ip)] =  ROOT.TH1F("Hist_reducedEnergy_forwardminus"+str(ip), "Hist_reducedEnergy_forwardminus"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_reducedEnergy_Castor"+str(ip)] =  ROOT.TH1F("Hist_reducedEnergy_Castor"+str(ip), "Hist_reducedEnergy_Castor"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            



            self.hist["Hist_2Dlog10MxMy"+str(ip)] =  ROOT.TH2D("Hist_2Dlog10MxMy"+str(ip), "Hist_2Dlog10MxMy"+str(ip), NbrLogMBins, BinLogMMin, BinLogMMax, NbrLogMBins, BinLogMMin, BinLogMMax)
            self.hist["Hist_log10Mx"+str(ip)] =  ROOT.TH1D("Hist_log10Mx"+str(ip), "Hist_log10Mx"+str(ip), NbrLogMBins, BinLogMMin, BinLogMMax)
            self.hist["Hist_log10My"+str(ip)] =  ROOT.TH1D("Hist_log10My"+str(ip), "Hist_log10My"+str(ip), NbrLogMBins, BinLogMMin, BinLogMMax)
            self.hist["Hist_GP_log10Mx"+str(ip)] =  ROOT.TH1D("Hist_GP_log10Mx"+str(ip), "Hist_GP_log10Mx"+str(ip), NbrLogMBins, BinLogMMin, BinLogMMax)
            self.hist["Hist_GP_log10My"+str(ip)] =  ROOT.TH1D("Hist_GP_log10My"+str(ip), "Hist_GP_log10My"+str(ip), NbrLogMBins, BinLogMMin, BinLogMMax)
            self.hist["Hist_GP_2Dlog10MxMy"+str(ip)] =  ROOT.TH2D("Hist_GP_2Dlog10MxMy"+str(ip), "Hist_GP_2Dlog10MxMy"+str(ip), NbrLogMBins, BinLogMMin, BinLogMMax, NbrLogMBins, BinLogMMin, BinLogMMax)
            self.hist["Hist_GP_log10XiX"+str(ip)] =  ROOT.TH1F("Hist_GP_log10XiX"+str(ip), "Hist_GP_log10XiX"+str(ip), NbrLogXiBins, BinLogXiMin, BinLogXiMax)
            self.hist["Hist_GP_log10XiY"+str(ip)] =  ROOT.TH1F("Hist_GP_log10XiY"+str(ip), "Hist_GP_log10XiY"+str(ip), NbrLogXiBins, BinLogXiMin, BinLogXiMax)
           


            self.hist["Hist_Xi"+str(ip)] =  ROOT.TH1F("Hist_Xi"+str(ip), "Hist_Xi"+str(ip), NbrXiBins, BinXiMin, BinXiMax)
            self.hist["Hist_Xi"+str(ip)] =  ROOT.TH1F("Hist_Xi"+str(ip), "Hist_Xi"+str(ip), NbrXiBins, BinXiMin, BinXiMax)
            self.hist["Hist_XiX"+str(ip)] =  ROOT.TH1F("Hist_XiX"+str(ip), "Hist_XiX"+str(ip), NbrXiBins, BinXiMin, BinXiMax)
            self.hist["Hist_XiY"+str(ip)] =  ROOT.TH1F("Hist_XiY"+str(ip), "Hist_XiY"+str(ip), NbrXiBins, BinXiMin, BinXiMax)

            self.hist["Hist_log10Xi"+str(ip)] =  ROOT.TH1F("Hist_log10Xi"+str(ip), "Hist_log10Xi"+str(ip), NbrLogXiBins, BinLogXiMin, BinLogXiMax)
            self.hist["Hist_log10Xi"+str(ip)] =  ROOT.TH1F("Hist_log10Xi"+str(ip), "Hist_log10Xi"+str(ip), NbrLogXiBins, BinLogXiMin, BinLogXiMax)
            self.hist["Hist_log10XiX"+str(ip)] =  ROOT.TH1F("Hist_log10XiX"+str(ip), "Hist_log10XiX"+str(ip), NbrLogXiBins, BinLogXiMin, BinLogXiMax)
            self.hist["Hist_log10XiY"+str(ip)] =  ROOT.TH1F("Hist_log10XiY"+str(ip), "Hist_log10XiY"+str(ip), NbrLogXiBins, BinLogXiMin, BinLogXiMax)

            self.hist["Hist_2Dlog10XiXXiY"+str(ip)] = ROOT.TH2D("Hist_2Dlog10XiXXiY"+str(ip), "Hist_2Dlog10XiXXiY"+str(ip), NbrLogXiBins, BinLogXiMin, BinLogXiMax, NbrLogXiBins, BinLogXiMin, BinLogXiMax)
            self.hist["Hist_2DRecoLogXiXGenLogXiX"+str(ip)] = ROOT.TH2D("Hist_2DRecoLogXiXGenLogXiX"+str(ip), "Hist_2DRecoLogXiXGenLogXiX"+str(ip), NbrLogXiBins, BinLogXiMin, BinLogXiMax, NbrLogXiBins, BinLogXiMin, BinLogXiMax)
            self.hist["Hist_2DRecoLogXiYGenLogXiY"+str(ip)] = ROOT.TH2D("Hist_2DRecoLogXiYGenLogXiY"+str(ip), "Hist_2DRecoLogXiYGenLogXiY"+str(ip), NbrLogXiBins, BinLogXiMin, BinLogXiMax, NbrLogXiBins, BinLogXiMin, BinLogXiMax)
            self.hist["Hist_2DGPLogXiXLogXiY"+str(ip)] = ROOT.TH2D("Hist_2DGPLogXiXLogXiY"+str(ip), "Hist_2DGPLogXiXLogXiY"+str(ip), NbrLogXiBins,BinLogXiMin, BinLogXiMax, NbrLogXiBins, BinLogXiMin, BinLogXiMax)
            
   
      
        for h in self.hist:
            self.hist[h].Sumw2()
            self.GetOutputList().Add(self.hist[h])

        self.pdg_helper = pd.PYTHIAParticleData()
        self.castor_tower_p4 = []
        self.CMenergy = 13000 # GeV
        self.protonmass = 0.938 # GeV

        for isec in xrange(0,16):
            self.castor_tower_p4.append( ROOT.ROOT.Math.LorentzVector('ROOT::Math::PxPyPzE4D<double>')(0,0,0,0) )

        outTree = ROOT.TTree("TreeS", "selected DD events")
        self.OUTlog10XixGen = array( 'f', 1 * [0] )
        self.OUTLog10XiyGen = array( 'f', 1 * [0] )
        self.OUTlog10XixReco = array( 'f', 1 * [0] )
        self.OUTlog10XiyReco = array( 'f', 1 * [0] )
        self.OUTlog10MxGen = array( 'f', 1 * [0] )
        self.OUTlog10MyGen = array( 'f', 1 * [0] )
        self.OUTlog10MxReco = array( 'f', 1 * [0] )
        self.OUTlog10MyReco = array( 'f', 1 * [0] )
        self.OUTdeltazero = array( 'f', 1 * [0] )
        self.OUTdelta = array( 'f', 1 * [0] )
        self.OUTetamin = array( 'f', 1 * [0] )
        self.OUTrapditygapmean = array( 'f', 1 * [0] )
        self.OUTetamax = array( 'f', 1 * [0] )
        # self.OUTCastorRecHitEnergy = array( 'd', 224 * [0.0])
        outTree.Branch('log10XixGen', self.OUTlog10XixGen,'log10XixGen/F')
        outTree.Branch('Log10XiyGen', self.OUTLog10XiyGen,'Log10XiyGen/F')
        outTree.Branch('log10XixReco', self.OUTlog10XixReco,'log10XixReco/F')
        outTree.Branch('log10XiyReco', self.OUTlog10XiyReco,'log10XiyReco/F')
        outTree.Branch('log10MxGen', self.OUTlog10MxGen,'log10MxGen/F')
        outTree.Branch('log10MyGen', self.OUTlog10MyGen,'log10MyGen/F')
        outTree.Branch('log10MxReco', self.OUTlog10MxReco,'log10MxReco/F')
        outTree.Branch('log10MyReco', self.OUTlog10MyReco,'log10MyReco/F')
        outTree.Branch('deltazero', self.OUTdeltazero,'deltazero/F')
        outTree.Branch('delta', self.OUTdelta,'delta/F')
        outTree.Branch('etamin', self.OUTetamin, 'etamin/F')
        outTree.Branch('RGmean', self.OUTrapditygapmean,'RGmean/F')
        outTree.Branch('etamax', self.OUTetamax, 'etamax/F')
        


       

        setattr(self, "outTree", outTree)
        self.addToOutput(self.outTree)
        
        outTreeB = ROOT.TTree("TreeB", "all events except DD events")
        self.OUTlog10XixGen_B = array( 'f', 1 * [0] )
        self.OUTLog10XiyGen_B = array( 'f', 1 * [0] )
        self.OUTlog10XixReco_B = array( 'f', 1 * [0] )
        self.OUTlog10XiyReco_B = array( 'f', 1 * [0] )
        self.OUTlog10MxGen_B = array( 'f', 1 * [0] )
        self.OUTlog10MyGen_B = array( 'f', 1 * [0] )
        self.OUTlog10MxReco_B = array( 'f', 1 * [0] )
        self.OUTlog10MyReco_B = array( 'f', 1 * [0] )
        self.OUTdeltazero_B = array( 'f', 1 * [0] )
        self.OUTdelta_B = array( 'f', 1 * [0] )
        self.OUTetamin_B = array( 'f', 1 * [0] )
        self.OUTetamax_B = array( 'f', 1 * [0] )
        self.OUTrapditygapmean_B = array( 'f', 1 * [0] )
        # self.OUTCastorRecHitEnergy = array( 'd', 224 * [0.0])
        outTreeB.Branch('log10XixGen', self.OUTlog10XixGen_B, 'log10XixGen/F')
        outTreeB.Branch('Log10XiyGen', self.OUTLog10XiyGen_B, 'Log10XiyGen/F')
        outTreeB.Branch('log10XixReco', self.OUTlog10XixReco_B, 'log10XixReco/F')
        outTreeB.Branch('log10XiyReco', self.OUTlog10XiyReco_B, 'log10XiyReco/F')
        outTreeB.Branch('log10MxGen', self.OUTlog10MxGen_B, 'log10MxGen/F')
        outTreeB.Branch('log10MyGen', self.OUTlog10MyGen_B, 'log10MyGen/F')
        outTreeB.Branch('log10MxReco', self.OUTlog10MxReco_B, 'log10MxReco/F')
        outTreeB.Branch('log10MyReco', self.OUTlog10MyReco_B, 'log10MyReco/F')
       
        outTreeB.Branch('delta', self.OUTdelta_B, 'delta/F')
        outTreeB.Branch('deltazero', self.OUTdeltazero_B, 'deltazero/F')
        outTreeB.Branch('etamin', self.OUTetamin_B, 'etamin/F')
        outTreeB.Branch('etamax', self.OUTetamax_B, 'etamax/F')
        outTreeB.Branch('RGmean', self.OUTrapditygapmean_B,'RGmean/F')
        setattr(self, "outTreeB", outTreeB)
        self.addToOutput(self.outTreeB)
        

        

    def analyze(self):
        # return 1
        

        if self.isData:
            if self.fChain.ZeroTeslaPixelnoPreSplittingVtx_vrtxX.size() > 0: 
                self.hist["Hist_NrVtx"].Fill(self.fChain.ZeroTeslaStripVtx_vrtxX.size())

            if self.fChain.ZeroTeslaPixelnoPreSplittingVtx_vrtxX.size() > 1:  return 0


        

        weight = 1
        num = 0
        # genTracks
        #num = self.fChain.genTracks.size()
        Eta = 0
        theta= 0
        Ntrack = 0
        phi = 0
        #print self.maxEta # see slaveParams below
        #self.hist["numGenTracks"].Fill(1)
       

     #############################################################
        # also write a ttree          #
        #               #
        # create the branches and assign the fill-variables to them #
        #############################################################
        



        Process_ID_Ext = '_NONE'
        if not self.isData:
            if self.fChain.processID == 101:
                Proces_ND= self.fChain.processID == 101
                Process_ID_Ext = '_ND'
            if self.fChain.processID == 103:    
                Proces_SD1= self.fChain.processID == 103   
                Process_ID_Ext = '_SD1'
            if self.fChain.processID == 104: 
                Proces_SD2= self.fChain.processID==104
                Process_ID_Ext = '_SD2'
            if self.fChain.processID == 105:
                process_DD= self.fChain.processID == 105 
                Process_ID_Ext = '_DD'
            if self.fChain.processID == 106:
                process_CD= self.fChain.processID == 106 
                Process_ID_Ext = '_CD'
      
   


        self.hist["hNentries"].Fill("all",1)
        self.hist["BunchCrossing"].Fill(self.fChain.bx)
        self.hist["Runs"].Fill(self.fChain.run)
   
    #######################HFCUT##################################    
        HFCut = False
        CaloTower = self.fChain.CaloTowersp4.size()
        for icalo in xrange(0,CaloTower):
            calop4 = self.fChain.CaloTowersp4[icalo]
            caloem = self.fChain.CaloTowersemEnergy[icalo]
            calohad = self.fChain.CaloTowershadEnergy[icalo]
           
            if abs(calop4.eta()) > 3.2 and abs(calop4.eta()) < 5.2 :
                if (calop4.e()) > 5:
                    HFCut = True
                    

        
        if HFCut == False : return 0
        
        Eta = 0
        GenParticleClass = []
        ChargedGenParticleClass = []
        theta = 0
       
        # self.hist["hNentries"].Fill("hf cut",1)         

        if  not self.isData:
            # GenParticleClass = []
            ngenParticle = self.fChain.genParticlesp4.size()

            # self.CMenergy= self.fChain.cmenergy
           
            # final state particles from the genParticles collection
            for igenP in xrange(ngenParticle):
                genp4 = self.fChain.genParticlesp4[igenP]
                genid = self.fChain.genParticlespdg[igenP]
                genst = self.fChain.genParticlesstatus[igenP]
                
              
                if genst != 1: continue
                
                GenParticleClass.append([genp4,genid])

                # if self.pdg_helper.charge(genid) == 0 : continue ######### only use charged particles
               
                ChargedGenParticleClass.append([genp4,genid])
      
    ##################Track##############################################################3
        TrackCandClass = []
       
        nTrackCand = self.fChain.ZeroTeslaPixelnoPreSplittingVtx_trktheta.size()
        for itrk in xrange(nTrackCand):
            
            theta= self.fChain.ZeroTeslaPixelnoPreSplittingVtx_trktheta[itrk]
            trkphi = self.fChain.ZeroTeslaPixelnoPreSplittingVtx_trkphi[itrk]
       
            Eta = -np.log(math.tan(theta/2))
            TrackCandClass.append([Eta,trkphi])
            

       

        mineta = -10000
        maxeta = -10000
        Deltaeta = -10000
        
        if len(TrackCandClass) == 0:
                return 0


        self.hist["Hist_TrackCandClass"].Fill(len(TrackCandClass))  

        TrackCandClass.sort(cmp=compareTracketa)
        mineta =  TrackCandClass[0][0]
        maxeta =  TrackCandClass[len(TrackCandClass)-1][0] #eta()pseduorapidty

        
        self.hist["Hist_Eta_Min"].Fill(mineta)
        self.hist["Hist_Eta_Max"].Fill(maxeta)
           
        Deltaeta = maxeta - mineta

        self.hist["Hist_Eta_Delta"].Fill(Deltaeta)  
        self.hist["Hist_Eta_Min" + Process_ID_Ext].Fill(mineta)
        self.hist["Hist_Eta_Max" + Process_ID_Ext].Fill(maxeta)  
        self.hist["Hist_Eta_Delta" + Process_ID_Ext].Fill(Deltaeta) 
       

        deltaeta = 1
        delta_zero = -1
        delta_Reco_zero_pos = -1
        deltaetamax = -1
        deltaetamax_Reco_pos = -1
        minangle = float("inf")
        r = -10000
        
        for jtrk in xrange(0,len(TrackCandClass)): #change   GenParticleClass to  TrackCandClass for testing
            tracketa  =  TrackCandClass[jtrk][0]
            trackphi = TrackCandClass[jtrk][1]
            # trackid  =  TrackCandClass[itrack][1]

            self.hist["Hist_trkEta"].Fill(TrackCandClass[jtrk][0])

            if jtrk < len(TrackCandClass)-1:
                # deltaeta =  TrackCandClass[itrack+1][0].eta() -  TrackCandClass[itrack][0].eta()
                deltaeta =  TrackCandClass[jtrk+1][0] - TrackCandClass[jtrk][0] #eta()pseduorapidty
                

                self.hist["Hist_trkplusEta"].Fill(TrackCandClass[jtrk+1][0])
                if  (deltaeta > deltaetamax):
                    deltaetamax = deltaeta
                    deltaetamax_Reco_pos = jtrk

                if  TrackCandClass[jtrk+1][0] > 0 and TrackCandClass[jtrk][0]< 0:
                    delta_zero = deltaeta
                    delta_Reco_zero_pos = jtrk

            self.hist["Hist_Eta_DeltaZero"].Fill(delta_zero)
            self.hist["Hist_Eta_DeltaMax"].Fill(deltaetamax)
            self.hist["Hist_Eta_DeltaMax"+ Process_ID_Ext].Fill(deltaetamax)
            self.hist["Hist_Eta_DeltaZero"+ Process_ID_Ext].Fill(delta_zero)
          

            
     
            # if  not self.isData:
                
            
            #     for iGP in xrange(len(ChargedGenParticleClass)):
            #         genp4  = ChargedGenParticleClass[iGP][0]
            #         dEta = tracketa - genp4.eta()
            #         dPhi = trackphi - genp4.phi()
                  
            #         r = sqrt((dEta**2) + (dPhi**2))
                    
            #         if (r < minangle):
            #             minangle = r

            # self.hist["Hist_Angle"].Fill(minangle) 




        mingeneta =-10000
        maxgeneta = -10000
         
        if not self.isData: #Rapidity -> chanded to eta again :)

            if len(ChargedGenParticleClass) == 0:
                return 0

            ChargedGenParticleClass.sort(cmp=compareGeneta)
            mingeneta = ChargedGenParticleClass[0][0].eta()
            maxgeneta = ChargedGenParticleClass[len(ChargedGenParticleClass)-1][0].eta()
            self.hist["Hist_GP_Eta_Min"].Fill(mingeneta)
            self.hist["Hist_GP_Eta_Max"].Fill(maxgeneta)
           
            Deltaeta = maxgeneta - mingeneta
            self.hist["Hist_GP_Eta_Delta"].Fill(Deltaeta)

            deltaeta=-1
            delta_zero_gen = -1
            delta_max_gen = -1
            delta_Gen_zero_pos = -1
            deltaetamax_Gen_pos = -1
            deltagenreco = -1
            
            for igp in xrange(len(ChargedGenParticleClass)-1):
                genp4  = ChargedGenParticleClass[igp][0]
                genid  = ChargedGenParticleClass[igp][1]
    
                
                deltaeta = ChargedGenParticleClass[igp+1][0].eta() - ChargedGenParticleClass[igp][0].eta() 
               
                

                if  (deltaeta > delta_max_gen):
                    delta_max_gen = deltaeta
                    deltaetamax_Gen_pos = igp

                if ChargedGenParticleClass[igp+1][0].eta() > 0 and ChargedGenParticleClass[igp][0].eta() < 0:
                    delta_zero_gen = deltaeta
                    delta_Gen_zero_pos = igp

                

            deltagenreco = (delta_zero_gen - delta_zero)
            self.hist["Hist_GP_Eta_DeltaMax"].Fill(delta_max_gen)
            self.hist["Hist_GP_Eta_DeltaZero"].Fill(delta_zero_gen)
            self.hist["Hist_Deltazero_deltagenreco"].Fill(deltagenreco)
            self.hist["Hist_2D_recogen_DeltaZero"].Fill(delta_zero, delta_zero_gen)
            self.hist["Hist_2D_recogen_DeltaMax"].Fill(deltaetamax, delta_max_gen) 
            self.hist["Hist_2D_recogen_EtaMiniumum"].Fill(mineta,mingeneta)
            self.hist["Hist_2D_recogen_EtaMax"].Fill(maxeta,maxgeneta)
            
           
       

            
            
            if len(GenParticleClass) == 0:
                return 0

            # calculate Mx2 and My2 for all genetrated particles
            XGenEtot = 0
            XPxtot = 0
            XPytot = 0
            XPztot = 0
            YGenEtot = 0
            YPxtot = 0
            YPytot = 0
            YPztot = 0
            Mx2 = 0
            My2 = 0
            MxGen = 0 
            MyGen = 0 
            MeanGen = -10000
            Px = 0
            Py= 0
            Px2 = 0
            Py2= 0
            GenXi_DD = -10000 

            for igp in xrange(0,len(GenParticleClass)): 
                if GenParticleClass[igp][0].eta() < ChargedGenParticleClass[deltaetamax_Gen_pos][0].eta():
                    XGenEtot += GenParticleClass[igp][0].E()
                    XPxtot += GenParticleClass[igp][0].Px()
                    XPytot += GenParticleClass[igp][0].Py()
                    XPztot += GenParticleClass[igp][0].Pz()

                if GenParticleClass[igp][0].eta() > ChargedGenParticleClass[deltaetamax_Gen_pos+1][0].eta():
                    YGenEtot += GenParticleClass[igp][0].E()
                    YPxtot += GenParticleClass[igp][0].Px()
                    YPytot += GenParticleClass[igp][0].Py()
                    YPztot += GenParticleClass[igp][0].Pz()
                
                MeanGen = (ChargedGenParticleClass[deltaetamax_Gen_pos+1][0].eta() + ChargedGenParticleClass[deltaetamax_Gen_pos][0].eta())/2 


            # Mx2 = XGenEtot*XGenEtot - XPxtot*XPxtot - XPytot*XPytot - XPztot*XPztot
            # My2 = YGenEtot*YGenEtot - YPxtot*YPxtot - YPytot*YPytot - YPztot*YPztot


            Px2 =  XPxtot**2 + XPytot**2 +XPztot**2
            Py2 =  YPxtot**2 + YPytot**2 +YPztot**2
            Px = sqrt(Px2)
            Py = sqrt(Py2)

            Mx2 = (XGenEtot+Px)*(XGenEtot-Px)
            My2 = (YGenEtot+Py)*(YGenEtot-Py)  
          

            if Mx2<=0: Mx2=1.01e-6
            if My2<=0: My2=1.01e-6

                      
            MxGen = sqrt(Mx2)
            self.hist["Hist_GP_Mx"].Fill(MxGen)
            self.hist["Hist_GP_log10Mx"].Fill(log10(MxGen))

            MyGen = sqrt(My2)
            self.hist["Hist_GP_My"].Fill(MyGen)
            self.hist["Hist_GP_log10My"].Fill(log10(MyGen))

            self.hist["Hist_GP_2Dlog10MxMy"].Fill(log10(MxGen),log10(MyGen))

            GenXiX = Mx2/self.CMenergy/self.CMenergy
            GenXiY = My2/self.CMenergy/self.CMenergy
            
            GenXi_DD = Mx2*My2/(self.protonmass**2 * self.CMenergy**2)
      
         
           
            self.hist["Hist_GP_log10Mx"+ Process_ID_Ext].Fill(log10(MxGen))
            self.hist["Hist_GP_log10My"+ Process_ID_Ext].Fill(log10(MyGen))
            self.hist["Hist_GP_2Dlog10MxMy"+ Process_ID_Ext].Fill(log10(MxGen),log10(MyGen))
          



         ####################################Calotower######################################


        CaloCandClass = []
        CaloReducedenergyClass = []
        CaloTower = self.fChain.CaloTowersp4.size()
       
        #noise cut i am using the vrtx cut ==0 and vrtx cut ==1
          
       
      
        counter = 0
        for icalo in xrange(0,CaloTower):
            calop4 = self.fChain.CaloTowersp4[icalo]
            caloem = self.fChain.CaloTowersemEnergy[icalo]
            calohad = self.fChain.CaloTowershadEnergy[icalo]

            CaloCandClass.append([calop4,caloem,calohad])
            
            if abs(calop4.eta()) < 1.6:
               
                if (calop4.e()) < 2.40: continue
                   
            if abs( calop4.eta()) > 1.4 and abs( calop4.eta()) < 2.8:
                if (calop4.e()) < 1.80: continue
              
            if abs( calop4.eta()) > 2.8 and abs( calop4.eta()) < 3.2: 
                if (calop4.e()) < 3.0: continue
                   
            if abs(calop4.eta()) > 3.2 and abs(calop4.eta()) < 5.2 :
                if (calop4.e()) < 2.2: continue

            CaloReducedenergyClass.append([calop4,caloem,calohad])
         
 


            #  if abs(calop4.eta()) < 1.4:
               
            #     if (calop4.e()) > 1.40: counter += 1
                   
            # if abs( calop4.eta()) > 1.4 and abs( calop4.eta()) < 2.6:
            #     if (calop4.e()) > 1.80: counter += 1 
              
            # if abs( calop4.eta()) > 2.6 and abs( calop4.eta()) < 3.2: 
            #     if (calop4.e()) > 2.40: counter += 1 
                   
            # if abs(calop4.eta()) > 3.2 and abs(calop4.eta()) < 5.2 :
            #     if (calop4.e()) > 1.8: counter += 1

              

        ####################################Castortower######################################
       
        self.sum_CAS_E_em = [0.0] * 16
        self.sum_CAS_E_had = [0.0] * 16
        self.sum_CAS_E = [0.0] * 16
        self.castor_id = [0] * 16
        self.castor_tower_E = [0.0] * 16



        if self.fChain.CastorRecHitEnergy.size() != 224:
            return 0


        for i in xrange(0, 224):
            isec = i//14
            imod = i%14
            if imod< 2:
               self.sum_CAS_E_em[isec] += self.fChain.CastorRecHitEnergy[i]
               # print "sum_CAS_E_em[isec][imod]", self.sum_CAS_E_em[isec]
            elif imod< 5:
                self.sum_CAS_E_had[isec] += self.fChain.CastorRecHitEnergy[i]
                # print "sum_CAS_E_had[isec][imod]", self.sum_CAS_E_had[isec]

            self.castor_tower_E[isec] += self.fChain.CastorRecHitEnergy[i]


      
        for isec in xrange(0,16): 
            self.sum_CAS_E[isec] = self.sum_CAS_E_em[isec] + self.sum_CAS_E_had[isec]
            self.hist["Hist_sum_CAS_E"].Fill(self.sum_CAS_E[isec])

            if  self.sum_CAS_E_em[isec] > self.sum_CAS_E_had[isec]:
                self.castor_id[isec] = 9 #3 is_gamma id
            else : self.castor_id[isec] = 8 # charged  hadron

            energy = self.sum_CAS_E[isec]
            caseta = -6.0
            px = energy/cosh(caseta) * cos(isec*pi/16. + pi/32.)
            py = energy/cosh(caseta) * sin(isec*pi/16. + pi/32.)
            pz = energy/cosh(caseta) * sinh(caseta)
            self.castor_tower_p4[isec].SetPxPyPzE(px,py,pz,energy)




            if (energy) < 0.8:continue   #Threshold for castor: 5.600000 ############# Castor noise cut

            CaloReducedenergyClass.append([self.castor_tower_p4[isec], 
                                # self.castor_id[isec],
                                self.sum_CAS_E_em[isec],
                                self.sum_CAS_E_had[isec]])
            
         ####### Vrtx cut######  
        if self.isData:
            if self.fChain.ZeroTeslaPixelnoPreSplittingVtx_vrtxX.size() == 0 and len(CaloReducedenergyClass) == 0: return 0
            if not self.fChain.ZeroTeslaPixelnoPreSplittingVtx_vrtxX.size() == 1 and len(CaloReducedenergyClass) < 1: return 0
             

       


        if len(CaloReducedenergyClass) == 0:
            return 0
       
        for icalo in xrange(0,len(CaloReducedenergyClass)):
            calop4  = CaloReducedenergyClass[icalo][0]
            caloem  = CaloReducedenergyClass[icalo][1]
            calohad  = CaloReducedenergyClass[icalo][2]
           
            
            self.hist["Hist_reducedEta"].Fill(calop4.eta()) 
            self.hist["Hist_reducedEnergy"].Fill(calop4.e())     

            self.hist["Hist_reducedEta" + Process_ID_Ext].Fill(calop4.eta())     
            self.hist["Hist_reducedEnergy" + Process_ID_Ext].Fill(calop4.e())     
           
            self.hist["hParticleCounts"].Fill("all",1)
           
            

            if abs( calop4.eta() ) < 1.4:
                self.hist["Hist_reducedEnergy_barrel"].Fill(calop4.e()) 
                self.hist["Hist_reducedEnergy_barrel" + Process_ID_Ext].Fill(calop4.e()) 
               


            if  abs( calop4.eta() ) > 1.8 and abs( calop4.eta() ) < 3.1:
                self.hist["Hist_reducedEnergy_endcap"].Fill(calop4.e()) 
                self.hist["Hist_reducedEnergy_endcap" + Process_ID_Ext].Fill(calop4.e()) 
               
                                       
           
            if  abs( calop4.eta() ) > 2.8 and abs( calop4.eta() ) < 3.2:
                self.hist["Hist_reducedEnergy_endcap_forwardtransition"].Fill(calop4.e()) 
                self.hist["Hist_reducedEnergy_endcap_forwardtransition" + Process_ID_Ext].Fill(calop4.e()) 
               
                            

            if  abs (calop4.eta()) > 3.2 and abs(calop4.eta()) < 5.2:
                self.hist["Hist_reducedEnergy_forward"].Fill(calop4.e())
                self.hist["Hist_reducedEnergy_forward" + Process_ID_Ext].Fill(calop4.e()) 
               
                    
            if calop4.eta() > 3.2 and calop4.eta() < 5.2:
                self.hist["Hist_reducedEnergy_forwardplus"].Fill(calop4.e())
                self.hist["Hist_reducedEnergy_forwardplus" + Process_ID_Ext].Fill(calop4.e()) 
               
            if calop4.eta() > -5.2 and calop4.eta() < -3.2:
                self.hist["Hist_reducedEnergy_forwardminus"].Fill(calop4.e())
                self.hist["Hist_reducedEnergy_forwardminus" + Process_ID_Ext].Fill(calop4.e()) 
            

            if  (calop4.eta()) > -6.6 and (calop4.eta()) < -5.2 :
                self.hist["Hist_reducedEnergy_Castor"].Fill(calop4.e())
                self.hist["Hist_reducedEnergy_Castor" + Process_ID_Ext].Fill(calop4.e()) 
                
          


        XEtot =  0
        XPxtot = 0
        XPytot = 0
        XPztot = 0
        YEtot =  0
        YPxtot = 0
        YPytot = 0
        YPztot = 0
        xix = 0 
        xiy = 0 
        Mx2 = 0
        My2 = 0
        Xi_DD = 0
        Px= 0
        Py= 0
        meanRec0 = -1000


        if len(CaloCandClass) == 0:
            return 0
       
        for icalo in xrange(0,len(CaloCandClass)):
            calop4  = CaloCandClass[icalo][0]
            caloem  = CaloCandClass[icalo][1]
            calohad  = CaloCandClass[icalo][2]
           
            
            self.hist["Hist_Eta"].Fill(calop4.eta()) 
            self.hist["Hist_Energy"].Fill(calop4.e())     

            self.hist["Hist_Eta" + Process_ID_Ext].Fill(calop4.eta())     
            self.hist["Hist_Energy" + Process_ID_Ext].Fill(calop4.e())     
           
            self.hist["hParticleCounts"].Fill("all",1)
           
            

            if abs( calop4.eta() ) < 1.4:
                self.hist["Hist_Energy_barrel"].Fill(calop4.e()) 
                self.hist["Hist_Energy_barrel" + Process_ID_Ext].Fill(calop4.e()) 
               


            if  abs( calop4.eta() ) > 1.8 and abs( calop4.eta() ) < 3.1:
                self.hist["Hist_Energy_endcap"].Fill(calop4.e()) 
                self.hist["Hist_Energy_endcap" + Process_ID_Ext].Fill(calop4.e()) 
               
                                       
           
            if  abs( calop4.eta() ) > 2.8 and abs( calop4.eta() ) < 3.2:
                self.hist["Hist_Energy_endcap_forwardtransition"].Fill(calop4.e()) 
                self.hist["Hist_Energy_endcap_forwardtransition" + Process_ID_Ext].Fill(calop4.e()) 
               
                            

            if  abs (calop4.eta()) > 3.2 and abs(calop4.eta()) < 5.2:
                self.hist["Hist_Energy_forward"].Fill(calop4.e())
                self.hist["Hist_Energy_forward" + Process_ID_Ext].Fill(calop4.e()) 
               
                    
            if calop4.eta() > 3.2 and calop4.eta() < 5.2:
                self.hist["Hist_Energy_forwardplus"].Fill(calop4.e())
                self.hist["Hist_Energy_forwardplus" + Process_ID_Ext].Fill(calop4.e()) 
               
            if calop4.eta() > -5.2 and calop4.eta() < -3.2:
                self.hist["Hist_Energy_forwardminus"].Fill(calop4.e())
                self.hist["Hist_Energy_forwardminus" + Process_ID_Ext].Fill(calop4.e()) 
            

            if  (calop4.eta()) > -6.6 and (calop4.eta()) < -5.2 :
                self.hist["Hist_Energy_Castor"].Fill(calop4.e())
                self.hist["Hist_Energy_Castor" + Process_ID_Ext].Fill(calop4.e()) 
                


      

            
            if calop4.eta() < TrackCandClass[deltaetamax_Reco_pos][0]:
               
                XEtot += calop4.E()
                XPxtot += calop4.Px()
                XPytot += calop4.Py()
                XPztot += calop4.Pz()
                

       
            if calop4.eta() > TrackCandClass[deltaetamax_Reco_pos+1][0]:
                  
                YEtot += calop4.E()
                YPxtot += calop4.Px()
                YPytot += calop4.Py()
                YPztot += calop4.Pz()

            MeanReco = (TrackCandClass[deltaetamax_Reco_pos+1][0] +  TrackCandClass[deltaetamax_Reco_pos][0])/2 

       
        Px2 =  XPxtot**2 + XPytot**2 +XPztot**2
        Py2 =  YPxtot**2 + YPytot**2 +YPztot**2
        Px = sqrt(Px2)
        Py = sqrt(Py2)
        # Mx2 = XEtot*XEtot - XPxtot*XPxtot - XPytot*XPytot - XPztot*XPztot
        # My2 = YEtot*YEtot - YPxtot*YPxtot - YPytot*YPytot - YPztot*YPztot
        Mx2 = (XEtot+Px)*(XEtot-Px)
        My2 = (YEtot+Py)*(YEtot-Py) 

         # set Mx2, My2 to zero if negative (i.e. the X,Y system is a photon)            
        if Mx2<=0: Mx2=1.01e-6
        if My2<=0: My2=1.01e-6

        Mx = sqrt(Mx2)
        My = sqrt(My2)
            
                

        
        if self.CMenergy > 0 :    
        # // calculate xix and xiy
            # xix = Mx*Mx/self.CMenergy/self.CMenergy
            # xiy = My*My/self.CMenergy/self.CMenergy
           
            xix = Mx2/self.CMenergy/self.CMenergy
            xiy = My2/self.CMenergy/self.CMenergy
            Xi_DD = Mx2*My2/(self.protonmass**2 * self.CMenergy**2)
            
            self.hist["Hist_XiX"].Fill(xix)
            self.hist["Hist_XiY"].Fill(xiy)
            self.hist["Hist_log10XiX"].Fill(log10(xix))
            self.hist["Hist_log10XiY"].Fill(log10(xiy))
            self.hist["Hist_2Dlog10XiXXiY"].Fill(log10(xix),log10(xiy))
            self.hist["Hist_XiX"+Process_ID_Ext].Fill(xix)
            self.hist["Hist_XiY"+Process_ID_Ext].Fill(xiy)
            self.hist["Hist_log10XiX"+Process_ID_Ext].Fill(log10(xix))
            self.hist["Hist_log10XiY"+Process_ID_Ext].Fill(log10(xiy))
            self.hist["Hist_2Dlog10XiXXiY"+Process_ID_Ext].Fill(log10(xix),log10(xiy))
            self.hist["Hist_log10Mx"].Fill(log10(Mx))
            self.hist["Hist_log10My"].Fill(log10(My))
            self.hist["Hist_2Dlog10MxMy"].Fill(log10(Mx),log10(My))
            self.hist["Hist_log10Mx"+ Process_ID_Ext].Fill(log10(Mx))
            self.hist["Hist_log10My"+ Process_ID_Ext].Fill(log10(My))
            self.hist["Hist_2Dlog10MxMy"+ Process_ID_Ext].Fill(log10(Mx),log10(My))
         
            Process_GP = '_NONE'
            if not self.isData:
                self.hist["Hist_2DRecoLogXiXGenLogXiX"].Fill(log10(xix),log10(GenXiX))
                self.hist["Hist_2DRecoLogXiYGenLogXiY"].Fill(log10(xiy),log10(GenXiY))
                self.hist["Hist_2D_genreco_Deltapos"].Fill(ChargedGenParticleClass[deltaetamax_Gen_pos][0].eta(),TrackCandClass[deltaetamax_Reco_pos][0]) 
                self.hist["Hist_2DRecoLogXiXGenLogXiX"+Process_ID_Ext].Fill(log10(xix),log10(GenXiX))
                self.hist["Hist_2DRecoLogXiYGenLogXiY"+Process_ID_Ext].Fill(log10(xiy),log10(GenXiY))
                self.hist["Hist_2Drecogen_EnergyX"].Fill(XEtot,XGenEtot)
                self.hist["Hist_2Drecogen_EnergyY"].Fill(YEtot,YGenEtot)
                self.hist["Hist_2D_recogen_Mean"].Fill(MeanReco, MeanGen)
                
                self.hist["Hist_GP_log10XiX"].Fill(log10(GenXiX))
                self.hist["Hist_GP_log10XiY"].Fill(log10(GenXiY))
                self.hist["Hist_GP_log10XiX"+Process_ID_Ext].Fill(log10(GenXiX))
                self.hist["Hist_GP_log10XiY"+Process_ID_Ext].Fill(log10(GenXiY))
                self.hist["Hist_2DGPLogXiXLogXiY"].Fill(log10(GenXiX),log10(GenXiY))
                self.hist["Hist_2DGPLogXiXLogXiY"+Process_ID_Ext].Fill(log10(GenXiX),log10(GenXiY))
                
                self.hist["Hist_GP_log10Xi_DD"].Fill(log10(GenXi_DD))  
                self.hist["Hist_Reco_log10Xi_DD"].Fill(log10(Xi_DD)) 
                self.hist["Hist_2DRecoLogXi_DDGenLogXi_DD"].Fill(log10(Xi_DD),log10(GenXi_DD))



                if maxeta < 1:
                    self.hist["Hist_2D_FG1_2DGPLogXiXLogXiY"].Fill(log10(GenXiX),log10(GenXiY))
                   
                if mineta > -1:
                    self.hist["Hist_2D_FG2_2DGPLogXiXLogXiY"].Fill(log10(GenXiX),log10(GenXiY))
                   
                if delta_zero > 3:
                    self.hist["Hist_2D_CG_2DGPLogXiXLogXiY"].Fill(log10(GenXiX),log10(GenXiY))
                   
               

                if (log10(GenXiX) + log10(GenXiY)) > -8.3 and (log10(GenXiX) + log10(GenXiY)) == -8.3 :
                    Process_GP = '_ND'
                  
                elif (log10(GenXiY)) < -8:
                    Process_GP = '_SD1'
               
                elif (log10(GenXiX)) < -8:
                    Process_GP = '_SD2'
                  
                # (log10(GenXi_DD))= Process_GP = '_DD'
                     

                  

                self.hist["Hist_GPCut_DeltaMax"].Fill(deltaetamax)
                self.hist["Hist_GPCut_DeltaZero"].Fill(delta_zero)
                self.hist["Hist_GPCut_DeltaMax"+Process_GP].Fill(deltaetamax)
                self.hist["Hist_GPCut_DeltaZero"+Process_GP].Fill(delta_zero)
                self.hist["Hist_GPCut_Eta_Min"].Fill(mineta)
                self.hist["Hist_GPCut_Eta_Max"].Fill(maxeta) 
                self.hist["Hist_GPCut_Eta_Min"+Process_GP].Fill(mineta)
                self.hist["Hist_GPCut_Eta_Max"+Process_GP].Fill(maxeta)  
                
          
                if maxeta < 1:
                    self.hist["Hist_2D_FG1_RecoLogXiXGenLogXiX"].Fill(log10(xix),log10(GenXiX))
                    self.hist["Hist_2D_FG1_RecoLogXiYGenLogXiY"].Fill(log10(xiy),log10(GenXiY))
                    # self.hist["Hist_FG1_DeltaZero"].Fill(delta_zero)
               
                if mineta > -1:
                    self.hist["Hist_2D_FG2_RecoLogXiXGenLogXiX"].Fill(log10(xix),log10(GenXiX))
                    self.hist["Hist_2D_FG2_RecoLogXiYGenLogXiY"].Fill(log10(xiy),log10(GenXiY))
                    # self.hist["Hist_FG1&FG2_DeltaZero"].Fill(delta_zero)
                        
                if delta_zero > 3:
                    self.hist["Hist_2D_CG_RecoLogXiXGenLogXiX"].Fill(log10(xix),log10(GenXiX))
                    self.hist["Hist_2D_CG_RecoLogXiYGenLogXiY"].Fill(log10(xiy),log10(GenXiY))
           

             
              

                if self.fChain.processID == 105 :
                    self.OUTlog10XixGen[0] =log10(GenXiX)
                    self.OUTLog10XiyGen[0] = log10(GenXiY)
                    self.OUTlog10XixReco[0] = log10(xix)
                    self.OUTlog10XiyReco[0] = log10(xiy)
                    self.OUTlog10MxGen[0] = log10(MxGen)
                    self.OUTlog10MyGen[0] = log10(MyGen)
                    self.OUTlog10MxReco[0] = log10(Mx)
                    self.OUTlog10MyReco[0] = log10(My)
                    self.OUTdeltazero[0] = delta_zero
                    self.OUTdeltazero[0] = deltaetamax
                    self.OUTetamin[0] = mineta
                    self.OUTetamax[0] = maxeta
                    self.OUTrapditygapmean [0] = MeanReco
                    self.outTree.Fill()
            
                else:
                    self.OUTlog10XixGen_B[0] = log10(GenXiX)
                    self.OUTLog10XiyGen_B[0] = log10(GenXiY)
                    self.OUTlog10XixReco_B[0] = log10(xix)
                    self.OUTlog10XiyReco_B[0] = log10(xiy)
                    self.OUTlog10MxGen_B[0] = log10(MxGen)
                    self.OUTlog10MyGen_B[0] = log10(MyGen)
                    self.OUTlog10MxReco_B[0] = log10(Mx)
                    self.OUTlog10MyReco_B[0] = log10(My)
                    self.OUTdeltazero_B[0] = delta_zero
                    self.OUTdeltazero_B[0] = deltaetamax
                    self.OUTetamin_B[0] = mineta
                    self.OUTetamax_B[0] = maxeta
                    self.OUTrapditygapmean_B[0] = MeanReco
                    self.outTreeB.Fill()
                
    

        return 1

    def finalize(self):
        print "Finalize:"
        if hasattr(self, 'outTree'):
            self.outTree.AutoSave()
        if hasattr(self, 'outTreeB'):
            self.outTreeB.AutoSave()


if __name__ == "__main__":
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
    ROOT.gSystem.Load("libFWCoreFWLite.so")
    ROOT.AutoLibraryLoader.enable()

    sampleList = []
    sampleList.append("MinBias_TuneMBR_13TeV-pythia8_MagnetOff_CASTORmeasured_newNoise")
    sampleList.append("data_ZeroBias1_CASTOR")
    # sampleList.append("data_ZeroBias1_CASTOR247934")
    maxFilesMC = None# run through all ffiles found
    maxFilesData = None# same
    nWorkers = 8# Use all cpu cores
   
   
    slaveParams = {}
    # slaveParams["maxEta"] = 2.


    # use printTTree.py <sampleName> to see what trees are avaliable inside the skim file
    DiffractiveAndTrack.runAll(treeName="EflowTree",
           slaveParameters=slaveParams,
           sampleList=sampleList,
           maxFilesMC = maxFilesMC,
           maxFilesData = maxFilesData,
           nWorkers= nWorkers,
           maxNevents = 2000000,
           verbosity = 2,
           outFile = "trackanddiffractive.root")
