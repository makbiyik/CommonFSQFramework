#!/usr/bin/env python


import CommonFSQFramework.Core.ExampleProofReader
#from rootpy.math.physics.vector import LorentzVector
import sys, os, time
sys.path.append(os.path.dirname(__file__))

import ROOT
ROOT.gROOT.SetBatch(True)
import ParticleDataTool as pd
from collections import Counter
from bad_calo_channel_list import bad_channels_eta_phi

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



EventSelection_with_Xi = False
Training_Signal = "DD"


HF_energy_scale = 1.00

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
        self.hist["hProcessesIdPythia"] = ROOT.TH1F("hProcessesIdPythia","hProcessesIdPythia",10, 0, 20)
        self.hist["hProcessescut"] = ROOT.TH1F("hProcessescut","hProcessescut",10, 0, 20)
        self.hist["hProcessescuteta"] = ROOT.TH1F("hProcessescuteta","hProcessescuteta",10, 0, 20)
        self.hist["BunchCrossing"] = ROOT.TH1F("BunchCrossing", "BunchCrossing",  3600, 0-0.5, 3600-0.5)
        self.hist["Runs"] =  ROOT.TH1F("Runs", "Runs",  2000, 246000-0.5, 278000-0.5)
        self.hist["HFEnergy"] = ROOT.TH1F("HFEnergy","HFEnergy",100, 0, 200)
        

        self.hist["Hist_sum_CAS_E"] = ROOT.TH1F("Hist_sum_CAS_E", "Hist_sum_CAS_E" ,100,0,600)
        self.hist["hParticleCounts"] = ROOT.TH1F("hParticleCounts","hParticleCounts",10, 0, 20) 
        self.hist["Hist_2Drecogen_EnergyX"] = ROOT.TH2D("Hist_2Drecogen_EnergyX", "Hist_2Drecogen_EnergyX", 100, 0, 8000,100, 0, 8000)    
        self.hist["Hist_2Drecogen_EnergyY"] = ROOT.TH2D("Hist_2Drecogen_EnergyY", "Hist_2Drecogen_EnergyY", 100, 0, 8000,100, 0, 8000)
        self.hist["Hist_numberoftowerebovenoise_endcap"] = ROOT.TH1F("Hist_numberoftowerebovenoise_endcap","Hist_numberoftowerebovenoise_endcap",30, 0,300) 
        self.hist["Hist_numberoftowerebovenoise_barrel"] = ROOT.TH1F("Hist_numberoftowerebovenoise_barrel","Hist_numberoftowerebovenoise_barrel",30, 0,300) 
        self.hist["Hist_numberoftowerebovenoise_endcapforwardtransition"] = ROOT.TH1F("Hist_numberoftowerebovenoise_endcapforwardtransition","Hist_numberoftowerebovenoise_endcapforwardtransition",30, 0,300) 

        self.hist["Hist_numberoftowerebovenoise_forwardplus"] = ROOT.TH1F("Hist_numberoftowerebovenoise_forwardplus","Hist_numberoftowerebovenoise_forwardplus",30, 0,300) 
        self.hist["Hist_numberoftowerebovenoise_forwardminus"] = ROOT.TH1F("Hist_numberoftowerebovenoise_forwardminus","Hist_numberoftowerebovenoise_forwardminus",30, 0,300) 
        self.hist["Hist_numberoftowerebovenoise_castor"] = ROOT.TH1F("Hist_numberoftowerebovenoise_castor","Hist_numberoftowerebovenoise_castor",18, 0,18) 
        self.hist["Hist_eventXiID_numberoftowerebovenoise_forwardplus"] = ROOT.TH1F("Hist_eventXiID_numberoftowerebovenoise_forwardplus","Hist_eventXiID_numberoftowerebovenoise_forwardplus",30, 0,300) 
        self.hist["Hist_eventXiID_numberoftowerebovenoise_forwardminus"] = ROOT.TH1F("Hist_eventXiID_numberoftowerebovenoise_forwardminus","Hist_eventXiID_numberoftowerebovenoise_forwardminus",30, 0,300) 
        self.hist["Hist_eventXiID_numberoftowerebovenoise_castor"] = ROOT.TH1F("Hist_eventXiID_numberoftowerebovenoise_castor","Hist_eventXiID_numberoftowerebovenoise_castor",16, 0,16) 
        
      
         
           

        nEtaBins = 8
        EtaBins = array('d',[-6.6, -5.2, -3.2, -2.8, -1.4, 1.4, 2.8, 3.2, 5.2])
    

        NbrVtxBins = 20
        BinVtxMin = 0
        BinVtxMax = 20


        self.hist["Hist_NrVtx"] = ROOT.TH1F("Hist_NrVtx_","Hist_NrVtx",NbrVtxBins,BinVtxMin, BinVtxMax)  

        

        NbrEtaBins = 50
        BinEtaMin = -5.5
        BinEtaMax = 4.5
        NbrDetaBins = 50
        BinDetaMin = 0
        BinDetaMax = 8
       

        self.hist["Hist_GP_eventXiID_Min"] = ROOT.TH1F("Hist_GP_eventXiID_Min", "Hist_GP_eventXiID_Min", NbrEtaBins, BinEtaMin, BinEtaMax)
        self.hist["Hist_GP_eventXiID_Max"] = ROOT.TH1F("Hist_GP_eventXiID_Max", "Hist_GP_eventXiID_Max", NbrEtaBins, BinEtaMin, BinEtaMax)
        self.hist["Hist_GP_eventXiID_DeltaMax"] = ROOT.TH1F("Hist_GP_eventXiID_DeltaMax", "Hist_GP_eventXiID_DeltaMax", NbrDetaBins, BinDetaMin, BinDetaMax)
        self.hist["Hist_GP_eventXiID_DeltaZero"] = ROOT.TH1F("Hist_GP_eventXiID_DeltaZero", "Hist_GP_eventXiID_DeltaZero", NbrDetaBins, BinDetaMin, BinDetaMax)
        self.hist["Hist_eventXiID_Min"] = ROOT.TH1F("Hist_eventXiID_Min", "Hist_eventXiID_Min", NbrEtaBins, BinEtaMin, BinEtaMax)
        self.hist["Hist_eventXiID_Max"] = ROOT.TH1F("Hist_eventXiID_Max", "Hist_eventXiID_Max", NbrEtaBins, BinEtaMin, BinEtaMax)
        self.hist["Hist_eventXiID_DeltaMax"] = ROOT.TH1F("Hist_eventXiID_DeltaMax", "Hist_eventXiID_DeltaMax", NbrDetaBins, BinDetaMin, BinDetaMax)
        self.hist["Hist_eventXiID_DeltaZero"] = ROOT.TH1F("Hist_eventXiID_DeltaZero", "Hist_eventXiID_DeltaZero", NbrDetaBins, BinDetaMin, BinDetaMax)
        self.hist["Hist_eventEtaID_Min"] = ROOT.TH1F("Hist_eventEtaID_Min", "Hist_eventEtaID_Min", NbrEtaBins, BinEtaMin, BinEtaMax)
        self.hist["Hist_eventEtaID_Max"] = ROOT.TH1F("Hist_eventEtaID_Max", "Hist_eventEtaID_Max", NbrEtaBins, BinEtaMin, BinEtaMax)
        self.hist["Hist_eventEtaID_DeltaMax"] = ROOT.TH1F("Hist_eventEtaID_DeltaMax", "Hist_eventEtaID_DeltaMax", NbrDetaBins, BinDetaMin, BinDetaMax)
        self.hist["Hist_eventEtaID_DeltaZero"] = ROOT.TH1F("Hist_eventEtaID_DeltaZero", "Hist_eventEtaID_DeltaZero", NbrDetaBins, BinDetaMin, BinDetaMax)
        self.hist["Hist_Eta_Min"] = ROOT.TH1F("Hist_Eta_Min", "Hist_Eta_Min", NbrEtaBins, BinEtaMin, BinEtaMax)
        self.hist["Hist_Eta_Max"] = ROOT.TH1F("Hist_Eta_Max", "Hist_Eta_Max", NbrEtaBins, BinEtaMin, BinEtaMax)
        self.hist["Hist_Eta_Delta"] = ROOT.TH1F("Hist_Eta_Delta", "Hist_Eta_Delta", NbrDetaBins, BinDetaMin, BinDetaMax)
        self.hist["Hist_Eta_DeltaZero"] = ROOT.TH1F("Hist_Eta_DeltaZero", "Hist_Eta_DeltaZero", NbrDetaBins, BinDetaMin, BinDetaMax)
        self.hist["Hist_Eta_DeltaMax"] = ROOT.TH1F("Hist_Eta_DeltaMax", "Hist_Eta_DeltaMax", NbrDetaBins, BinDetaMin, BinDetaMax)
        self.hist["Hist_2D_genreco_Deltapos"] = ROOT.TH2D("Hist_2D_genreco_Deltapos", "Hist_2D_genreco_Deltapos", NbrEtaBins, BinEtaMin, BinEtaMax,NbrEtaBins, BinEtaMin, BinEtaMax)
        # Gen PArticle 
        self.hist["Hist_2D_recogen_Mean"] = ROOT.TH2D("Hist_2D_recogen_Mean","Hist_2D_recogen_Mean",NbrEtaBins, BinEtaMin, BinEtaMax,NbrEtaBins, BinEtaMin, BinEtaMax)
        self.hist["Hist_GP_Min"] = ROOT.TH1F("Hist_GP_Min", "Hist_GP_Min", NbrEtaBins, BinEtaMin, BinEtaMax)
        self.hist["Hist_GP_Max"] = ROOT.TH1F("Hist_GP_Max", "Hist_GP_Max", NbrEtaBins, BinEtaMin, BinEtaMax)
        self.hist["Hist_GP_Delta"] = ROOT.TH1F("Hist_GP_Delta","Hist_GP_Delta", NbrDetaBins, BinDetaMin, BinDetaMax)
        self.hist["Hist_GP_DeltaZero"] = ROOT.TH1F("Hist_GP_DeltaZero", "Hist_GP_DeltaZero", NbrDetaBins, BinDetaMin, BinDetaMax)
        self.hist["Hist_GP_DeltaMax"] = ROOT.TH1F("Hist_GP_DeltaMax", "Hist_GP_DeltaMax", NbrDetaBins, BinDetaMin, BinDetaMax)
        self.hist["Hist_Deltazero_deltagenreco"] = ROOT.TH1F("Hist_Deltazero_deltagenreco", "Hist_Deltazero_deltagenreco", NbrDetaBins, -10, BinDetaMax)
        self.hist["Hist_2D_recogen_DeltaZero"] = ROOT.TH2D("Hist_2D_recogen_DeltaZero","Hist_2D_recogen_DeltaZero", NbrDetaBins,BinDetaMin, BinDetaMax,NbrDetaBins,BinDetaMin, BinDetaMax);
        self.hist["Hist_2D_recogen_DeltaMax"] = ROOT.TH2D("Hist_2D_recogen_DeltaMax","Hist_2D_recogen_DeltaMax", NbrDetaBins,BinDetaMin, BinDetaMax,NbrDetaBins,BinDetaMin, BinDetaMax);
        self.hist["Hist_2D_recogen_EtaMiniumum"] = ROOT.TH2D("Hist_2D_recogen_EtaMiniumum","Hist_2D_recogen_EtaMiniumum",NbrEtaBins, BinEtaMin, BinEtaMax,NbrEtaBins, BinEtaMin, BinEtaMax)
        self.hist["Hist_2D_recogen_EtaMax"]= ROOT.TH2D("Hist_2D_recogen_EtaMax","Hist_2D_recogen_EtaMax",NbrEtaBins, BinEtaMin, BinEtaMax,NbrEtaBins, BinEtaMin, BinEtaMax)
        

        NbrSizeBins = 50
        BinSizeEMin = 0
        BinSizeEMax = 50
        
        self.hist["Hist_NbrTracks"] = ROOT.TH1F("Hist_NbrTracks","Hist_NbrTracks",NbrSizeBins, BinSizeEMin,100)
        self.hist["Hist_eventXiID_NbrTracks"] = ROOT.TH1F("Hist_eventXiID_NbrTracks","Hist_eventXiID_NbrTracks",NbrSizeBins, BinSizeEMin,100)
       
        BinPhiMin = -5
        BinPhiMax = 5
        NbrPhiBins = 50
        
        self.hist["Hist_trkPhi"] = ROOT.TH1F("Hist_trkPhi","Hist_trkPhi",NbrPhiBins,  BinPhiMin, BinPhiMax)  
        self.hist["Hist_Eta"] = ROOT.TH1F("Hist_Eta","Hist_Eta",NbrEtaBins, BinEtaMin, BinEtaMax) 
        self.hist["Hist_reducedEta"] = ROOT.TH1F("Hist_reducedEta","Hist_reducedEta",NbrEtaBins, BinEtaMin, BinEtaMax)  
        self.hist["Calotower2D_eta_phi"] =  ROOT.TH2D("Calotower2D_eta_phi","Calotower2D_eta_phi",101,-50.5,50.5,81, -0.5, 80.5))
        self.hist["Calotower2D_Energy_eta_phi"] =  ROOT.TProfile2D("Calotower2D_Energy_eta_phi","Calotower2D_Energy_eta_phi",101,-50.5,50.5,81, -0.5, 80.5))
       

        self.hist["Hist_trkEta"] = ROOT.TH1F("Hist_trkEta","Hist_trkEta",NbrEtaBins, BinEtaMin, BinEtaMax)  
        self.hist["Hist_trkplusEta"] = ROOT.TH1F("Hist_trkplusEta","Hist_trkplusEta",NbrEtaBins, BinEtaMin, BinEtaMax) 
        NbrNtrackBins = 50
        BinNtrackMin = 0
        BinNtrackMax = 150
       
        NbrLogMBins = 100
        BinLogMMin = -3.5
        BinLogMMax = 5.5
        
        NbrPFEBins = 50
        BinPFEMin = 0
        BinPFEMax = 50

       
        self.hist["Hist_log10Mx"] = ROOT.TH1F("Hist_log10Mx", "Hist_log10Mx", NbrLogMBins, BinLogMMin, BinLogMMax)
        self.hist["Hist_log10My"] = ROOT.TH1F("Hist_log10My", "Hist_log10My", NbrLogMBins, BinLogMMin, BinLogMMax)  
        self.hist["Hist_2Dlog10MxMy"] = ROOT.TH2D("Hist_2Dlog10MxMy", "Hist_2Dlog10MxMy", NbrLogMBins, BinLogMMin, BinLogMMax, NbrLogMBins, BinLogMMin, BinLogMMax)
        self.hist["Hist_eventXiID_2Dlog10MxMy"] =  ROOT.TH2D("Hist_eventXiID_2Dlog10MxMy", "Hist_eventXiID_2Dlog10MxMy", NbrLogMBins, BinLogMMin, BinLogMMax, NbrLogMBins, BinLogMMin, BinLogMMax)
        Process_ID = ["_NONE","_Rest","_SD1","_SD2","_DD", "_CD"]
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
        self.hist["Hist_eventXiID_Energy"] =  ROOT.TH1F("Hist_eventXiID_Energy", "Hist_eventXiID_Energy" , NbrPFEBins, BinPFEMin, BinPFEMax)
        self.hist["Hist_eventXiID_Energy_barrel"] =  ROOT.TH1F("Hist_eventXiID_Energy_barrel", "Hist_eventXiID_Energy_barrel" , NbrPFEBins, BinPFEMin, BinPFEMax)
        self.hist["Hist_eventXiID_Energy_endcap"] =  ROOT.TH1F("Hist_eventXiID_Energy_endcap", "Hist_eventXiID_Energy_endcap" , NbrPFEBins, BinPFEMin, BinPFEMax)
        self.hist["Hist_eventXiID_Energy_endcap_forwardtransition"] =  ROOT.TH1F("Hist_eventXiID_Energy_endcap_forwardtransition", "Hist_eventXiID_Energy_endcap_forwardtransition" , NbrPFEBins, BinPFEMin, BinPFEMax)
        self.hist["Hist_eventXiID_Energy_forward"] =  ROOT.TH1F("Hist_eventXiID_Energy_forward", "Hist_eventXiID_Energy_forward" , NbrPFEBins, BinPFEMin, BinPFEMax)
        self.hist["Hist_eventXiID_Energy_forwardplus"] =  ROOT.TH1F("Hist_eventXiID_Energy_forwardplus", "Hist_eventXiID_Energy_forwardplus" , NbrPFEBins, BinPFEMin, BinPFEMax)
        self.hist["Hist_eventXiID_Energy_forwardminus"] =  ROOT.TH1F("Hist_eventXiID_Energy_forwardminus", "Hist_eventXiID_Energy_forwardminus" , NbrPFEBins, BinPFEMin, BinPFEMax)
        self.hist["Hist_eventXiID_Energy_Castor"] =  ROOT.TH1F("Hist_eventXiID_Energy_Castor", "Hist_eventXiID_Energy_Castor" , NbrPFEBins, BinPFEMin, BinPFEMax)
        
        self.hist["Hist_eventXiID_reducedEnergy"] =  ROOT.TH1F("Hist_eventXiID_reducedEnergy", "Hist_eventXiID_reducedEnergy" , NbrPFEBins, BinPFEMin, BinPFEMax)
        self.hist["Hist_eventXiID_reducedEnergy_barrel"] =  ROOT.TH1F("Hist_eventXiID_reducedEnergy_barrel", "Hist_eventXiID_reducedEnergy_barrel" , NbrPFEBins, BinPFEMin, BinPFEMax)
        self.hist["Hist_eventXiID_reducedEnergy_endcap"] =  ROOT.TH1F("Hist_eventXiID_reducedEnergy_endcap", "Hist_eventXiID_reducedEnergy_endcap" , NbrPFEBins, BinPFEMin, BinPFEMax)
        self.hist["Hist_eventXiID_reducedEnergy_endcap_forwardtransition"] =  ROOT.TH1F("Hist_eventXiID_reducedEnergy_endcap_forwardtransition", "Hist_eventXiID_reducedEnergy_endcap_forwardtransition" , NbrPFEBins, BinPFEMin, BinPFEMax)
        self.hist["Hist_eventXiID_reducedEnergy_forward"] =  ROOT.TH1F("Hist_eventXiID_reducedEnergy_forward", "Hist_eventXiID_reducedEnergy_forward" , NbrPFEBins, BinPFEMin, BinPFEMax)
        self.hist["Hist_eventXiID_reducedEnergy_forwardplus"] =  ROOT.TH1F("Hist_eventXiID_reducedEnergy_forwardplus", "Hist_eventXiID_reducedEnergy_forwardplus" , NbrPFEBins, BinPFEMin, BinPFEMax)
        self.hist["Hist_eventXiID_reducedEnergy_forwardminus"] =  ROOT.TH1F("Hist_eventXiID_reducedEnergy_forwardminus", "Hist_eventXiID_reducedEnergy_forwardminus" , NbrPFEBins, BinPFEMin, BinPFEMax)
        self.hist["Hist_eventXiID_reducedEnergy_Castor"] =  ROOT.TH1F("Hist_eventXiID_reducedEnergy_Castor", "Hist_eventXiID_reducedEnergy_Castor" , NbrPFEBins, BinPFEMin, BinPFEMax)
        self.hist["Hist_reducedEnergy"] =  ROOT.TH1F("Hist_reducedEnergy", "Hist_reducedEnergy" , NbrPFEBins, BinPFEMin, BinPFEMax)
        self.hist["Hist_reducedEnergy_barrel"] =  ROOT.TH1F("Hist_reducedEnergy_barrel", "Hist_reducedEnergy_barrel" , NbrPFEBins, BinPFEMin, BinPFEMax)
        self.hist["Hist_reducedEnergy_endcap"] =  ROOT.TH1F("Hist_reducedEnergy_endcap", "Hist_reducedEnergy_endcap" , NbrPFEBins, BinPFEMin, BinPFEMax)
        self.hist["Hist_reducedEnergy_endcap_forwardtransition"] =  ROOT.TH1F("Hist_reducedEnergy_endcap_forwardtransition", "Hist_reducedEnergy_endcap_forwardtransition" , NbrPFEBins, BinPFEMin, BinPFEMax)
        self.hist["Hist_reducedEnergy_forward"] =  ROOT.TH1F("Hist_reducedEnergy_forward", "Hist_reducedEnergy_forward" , NbrPFEBins, BinPFEMin, BinPFEMax)
        self.hist["Hist_reducedEnergy_forwardplus"] =  ROOT.TH1F("Hist_reducedEnergy_forwardplus", "Hist_reducedEnergy_forwardplus" , NbrPFEBins, BinPFEMin, BinPFEMax)
        self.hist["Hist_reducedEnergy_forwardminus"] =  ROOT.TH1F("Hist_reducedEnergy_forwardminus", "Hist_reducedEnergy_forwardminus" , NbrPFEBins, BinPFEMin, BinPFEMax)
        self.hist["Hist_reducedEnergy_Castor"] =  ROOT.TH1F("Hist_reducedEnergy_Castor", "Hist_reducedEnergy_Castor" , NbrPFEBins, BinPFEMin, BinPFEMax)
        self.hist["Hist_CaloReducedenergyClass"]= ROOT.TH1F("Hist_CaloReducedenergyClass","Hist_CaloReducedenergyClass",NbrPFEBins, BinPFEMin, BinPFEMax)
 

        NbrLogXiBins = 100
        BinLogXiMin = -11.5
        BinLogXiMax =0.5
        NbrXiBins = 50
        BinXiMin = 0
        BinXiMax = 5
        NbrLogXiBins = 100
        BinLogXiMin = -11.5
        BinLogXiMax = 0.5

        
        self.hist["Hist_XiX"] =  ROOT.TH1F("Hist_XiX", "Hist_XiX", NbrXiBins, BinXiMin, BinXiMax)
        self.hist["Hist_XiY"] =  ROOT.TH1F("Hist_XiY", "Hist_XiY", NbrXiBins, BinXiMin, BinXiMax)
        self.hist["Hist_calculated_log10XiDD"] =  ROOT.TH1F("Hist_calculated_log10XiDD", "Hist_calculated_log10XiDD", NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        self.hist["Hist_2D_calculated_log10XiDD_Deltamax"]= ROOT.TH2D("Hist_2D_calculated_log10XiDD_Deltamax","Hist_2D_calculated_log10XiDD_Deltamax",NbrLogXiBins, BinLogXiMin,BinLogXiMax,NbrDetaBins, BinDetaMin, BinDetaMax)
        self.hist["Hist_Reco_log10XiDD"] =  ROOT.TH1F("Hist_Reco_log10XiDD", "Hist_Reco_log10XiDD", NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        self.hist["Hist_eventXiID_Reco_log10XiDD"] =  ROOT.TH1F("Hist_eventXiID_Reco_log10XiDD", "Hist_eventXiID_Reco_log10XiDD", NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        self.hist["Hist_2DRecoLogXi_DDGenLogXi_DD"] = ROOT.TH2D("Hist_2DRecoLogXi_DDGenLogXi_DD", "Hist_2DRecoLogXi_DDGenLogXi_DD", NbrLogXiBins, BinLogXiMin, BinLogXiMax, NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        self.hist["Hist_log10XiX"] =  ROOT.TH1F("Hist_log10XiX", "Hist_log10XiX", NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        self.hist["Hist_log10XiY"] =  ROOT.TH1F("Hist_log10XiY", "Hist_log10XiY", NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        self.hist["Hist_GP_log10XiX"] =  ROOT.TH1F("Hist_GP_log10XiX", "Hist_GP_log10XiX", NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        self.hist["Hist_GP_log10XiY"] =  ROOT.TH1F("Hist_GP_log10XiY", "Hist_GP_log10XiY", NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        self.hist["Hist_2Dlog10XiXXiY"] = ROOT.TH2D("Hist_2Dlog10XiXXiY", "Hist_2Dlog10XiXXiY", NbrLogXiBins, BinLogXiMin, BinLogXiMax, NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        self.hist["Hist_2DLogRecoXiX_logGenXiX"] = ROOT.TH2D("Hist_2DLogRecoXiX_logGenXiX", "Hist_2DLogRecoXiX_logGenXiX", NbrLogXiBins, BinLogXiMin, BinLogXiMax, NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        self.hist["Hist_2DLogRecoXiY_logGenLogXiY"] = ROOT.TH2D("Hist_2DLogRecoXiY_logGenLogXiY", "Hist_2DLogRecoXiY_logGenLogXiY", NbrLogXiBins, BinLogXiMin, BinLogXiMax, NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        self.hist["Hist_2DLogGenXiX_LogGenXiY"] = ROOT.TH2D("Hist_2DLogGenXiX_LogGenXiY", "Hist_2DLogGenXiX_LogGenXiY", NbrLogXiBins, BinLogXiMin, BinLogXiMax, NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        self.hist["Hist_2D_FG2_RecoLogXiXGenLogXiX"] = ROOT.TH2D("Hist_2D_FG2_RecoLogXiXGenLogXiX", "Hist_2D_FG2_RecoLogXiXGenLogXiX", NbrLogXiBins, BinLogXiMin, BinLogXiMax, NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        self.hist["Hist_2D_FG2_RecoLogXiYGenLogXiY"] = ROOT.TH2D("Hist_2D_FG2_RecoLogXiYGenLogXiY", "Hist_2D_FG2_RecoLogXiYGenLogXiY", NbrLogXiBins, BinLogXiMin, BinLogXiMax, NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        self.hist["Hist_2D_FG1_RecoLogXiXGenLogXiX"] = ROOT.TH2D("Hist_2D_FG1_RecoLogXiXGenLogXiX", "Hist_2D_FG1_RecoLogXiXGenLogXiX", NbrLogXiBins, BinLogXiMin, BinLogXiMax, NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        self.hist["Hist_2D_FG1_RecoLogXiYGenLogXiY"] = ROOT.TH2D("Hist_2D_FG1_RecoLogXiYGenLogXiY", "Hist_2D_FG1_RecoLogXiYGenLogXiY", NbrLogXiBins, BinLogXiMin, BinLogXiMax, NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        self.hist["Hist_2D_CG_RecoLogXiXGenLogXiX"] = ROOT.TH2D("Hist_2D_CG_RecoLogXiXGenLogXiX", "Hist_2D_CG_RecoLogXiXGenLogXiX", NbrLogXiBins, BinLogXiMin, BinLogXiMax, NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        self.hist["Hist_2D_CG_RecoLogXiYGenLogXiY"] = ROOT.TH2D("Hist_2D_CG_RecoLogXiYGenLogXiY", "Hist_2D_CG_RecoLogXiYGenLogXiY", NbrLogXiBins, BinLogXiMin, BinLogXiMax, NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        self.hist["Hist_2D_FG2_2DLogGenXiX_LogGenXiY"] = ROOT.TH2D("Hist_2D_FG2_2DLogGenXiX_LogGenXiY", "Hist_2D_FG2_2DLogGenXiX_LogGenXiY", NbrLogXiBins, BinLogXiMin, BinLogXiMax, NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        self.hist["Hist_2D_FG1_2DLogGenXiX_LogGenXiY"] = ROOT.TH2D("Hist_2D_FG1_2DLogGenXiX_LogGenXiY", "Hist_2D_FG1_2DLogGenXiX_LogGenXiY", NbrLogXiBins, BinLogXiMin, BinLogXiMax, NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        self.hist["Hist_2D_CG_2DLogGenXiX_LogGenXiY"] = ROOT.TH2D("Hist_2D_CG_2DLogGenXiX_LogGenXiY", "Hist_2D_CG_2DLogGenXiX_LogGenXiY", NbrLogXiBins, BinLogXiMin, BinLogXiMax, NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        self.hist["Hist_eventXiID_log10XiX"] =  ROOT.TH1F("Hist_eventXiID_log10XiX", "Hist_eventXiID_log10XiX", NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        self.hist["Hist_eventXiID_log10XiY"] =  ROOT.TH1F("Hist_eventXiID_log10XiY", "Hist_eventXiID_log10XiY", NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        self.hist["Hist_GP_eventXiID_log10XiX"] =  ROOT.TH1F("Hist_GP_eventXiID_log10XiX", "Hist_GP_eventXiID_log10XiX", NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        self.hist["Hist_GP_eventXiID_log10XiY"] =  ROOT.TH1F("Hist_GP_eventXiID_log10XiY", "Hist_GP_eventXiID_log10XiY", NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        
        
       
        for ip in Process_ID:
            self.hist["Hist_Eta_Min"+str(ip)] = ROOT.TH1D("Hist_Eta_Min"+str(ip),"Hist_Eta_Min ", NbrEtaBins, BinEtaMin, BinEtaMax)
            self.hist["Hist_Eta_Max"+str(ip)] = ROOT.TH1D("Hist_Eta_Max"+str(ip),"Hist_Eta_Max ", NbrEtaBins, BinEtaMin, BinEtaMax) 
            self.hist["Hist_Eta_Delta"+str(ip)] = ROOT.TH1D("Hist_Eta_Delta"+str(ip),"Hist_Eta_Delta ", NbrDetaBins, BinDetaMin, BinDetaMax)
            self.hist["Hist_Eta_DeltaZero"+str(ip)] = ROOT.TH1D("Hist_Eta_DeltaZero"+str(ip),"Hist_Eta_DeltaZero ", NbrDetaBins, BinDetaMin, BinDetaMax)
            self.hist["Hist_Eta_DeltaMax"+str(ip)] =  ROOT.TH1F("Hist_Eta_DeltaMax"+str(ip), "Hist_Eta_DeltaMax"+str(ip), NbrDetaBins, BinDetaMin, BinDetaMax)               
            self.hist["Hist_Eta"+str(ip)] =  ROOT.TH1F("Hist_Eta"+str(ip), "Hist_Eta"+str(ip), nEtaBins, EtaBins)
            self.hist["Hist_reducedEta"+str(ip)] =  ROOT.TH1F("Hist_reducedEta"+str(ip), "Hist_reducedEta"+str(ip), nEtaBins, EtaBins)
            self.hist["Hist_GP_DeltaMax"+str(ip)] =  ROOT.TH1F("Hist_GP_DeltaMax"+str(ip), "Hist_GP_DeltaMax"+str(ip), NbrDetaBins, BinDetaMin, BinDetaMax)               
            self.hist["Hist_GP_Min"+str(ip)] = ROOT.TH1D("Hist_GP_Min"+str(ip),"Hist_GP_Min ", NbrEtaBins, BinEtaMin, BinEtaMax)
            self.hist["Hist_GP_Max"+str(ip)] = ROOT.TH1D("Hist_GP_Max"+str(ip),"Hist_GP_Max ", NbrEtaBins, BinEtaMin, BinEtaMax) 
            self.hist["Hist_GP_Delta"+str(ip)] = ROOT.TH1D("Hist_GP_Delta"+str(ip),"Hist_GP_Delta ", NbrDetaBins, BinDetaMin, BinDetaMax)
            self.hist["Hist_GP_DeltaZero"+str(ip)] = ROOT.TH1D("Hist_GP_DeltaZero"+str(ip),"Hist_GP_DeltaZero ", NbrDetaBins, BinDetaMin, BinDetaMax)
            self.hist["Hist_Energy"+str(ip)] =  ROOT.TH1F("Hist_Energy"+str(ip), "Hist_Energy"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_Energy_barrel"+str(ip)] =  ROOT.TH1F("Hist_Energy_barrel"+str(ip), "Hist_Energy_barrel"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_Energy_endcap"+str(ip)] =  ROOT.TH1F("Hist_Energy_endcap"+str(ip), "Hist_Energy_endcap"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_Energy_endcap_forwardtransition"+str(ip)] =  ROOT.TH1F("Hist_Energy_endcap_forwardtransition"+str(ip), "Hist_Energy_endcap_forwardtransition"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_Energy_forward"+str(ip)] =  ROOT.TH1F("Hist_Energy_forward"+str(ip), "Hist_Energy_forward"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_Energy_forwardplus"+str(ip)] =  ROOT.TH1F("Hist_Energy_forwardplus"+str(ip), "Hist_Energy_forwardplus"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_Energy_forwardminus"+str(ip)] =  ROOT.TH1F("Hist_Energy_forwardminus"+str(ip), "Hist_Energy_forwardminus"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_Energy_Castor"+str(ip)] =  ROOT.TH1F("Hist_Energy_Castor"+str(ip), "Hist_Energy_Castor"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
           
            self.hist["Hist_CaloReducedenergyClass"+str(ip)]= ROOT.TH1F("Hist_CaloReducedenergyClass"+str(ip),"Hist_CaloReducedenergyClass"+str(ip),NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_reducedEnergy"+str(ip)] =  ROOT.TH1F("Hist_reducedEnergy"+str(ip), "Hist_reducedEnergy"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_reducedEnergy_barrel"+str(ip)] =  ROOT.TH1F("Hist_reducedEnergy_barrel"+str(ip), "Hist_reducedEnergy_barrel"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_reducedEnergy_endcap"+str(ip)] =  ROOT.TH1F("Hist_reducedEnergy_endcap"+str(ip), "Hist_reducedEnergy_endcap"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_reducedEnergy_endcap_forwardtransition"+str(ip)] =  ROOT.TH1F("Hist_reducedEnergy_endcap_forwardtransition"+str(ip), "Hist_reducedEnergy_endcap_forwardtransition"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_reducedEnergy_forward"+str(ip)] =  ROOT.TH1F("Hist_reducedEnergy_forward"+str(ip), "Hist_reducedEnergy_forward"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_reducedEnergy_forwardplus"+str(ip)] =  ROOT.TH1F("Hist_reducedEnergy_forwardplus"+str(ip), "Hist_reducedEnergy_forwardplus"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_reducedEnergy_forwardminus"+str(ip)] =  ROOT.TH1F("Hist_reducedEnergy_forwardminus"+str(ip), "Hist_reducedEnergy_forwardminus"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_reducedEnergy_Castor"+str(ip)] =  ROOT.TH1F("Hist_reducedEnergy_Castor"+str(ip), "Hist_reducedEnergy_Castor"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            
            self.hist["Hist_2Dlog10MxMy"+str(ip)] =  ROOT.TH2D("Hist_2Dlog10MxMy"+str(ip), "Hist_2Dlog10MxMy"+str(ip), NbrLogMBins, BinLogMMin, BinLogMMax, NbrLogMBins, BinLogMMin, BinLogMMax)
            self.hist["Hist_eventXiID_2Dlog10MxMy"+str(ip)] =  ROOT.TH2D("Hist_eventXiID_2Dlog10MxMy"+str(ip), "Hist_eventXiID_2Dlog10MxMy"+str(ip), NbrLogMBins, BinLogMMin, BinLogMMax, NbrLogMBins, BinLogMMin, BinLogMMax)
            self.hist["Hist_log10Mx"+str(ip)] =  ROOT.TH1D("Hist_log10Mx"+str(ip), "Hist_log10Mx"+str(ip), NbrLogMBins, BinLogMMin, BinLogMMax)
            self.hist["Hist_log10My"+str(ip)] =  ROOT.TH1D("Hist_log10My"+str(ip), "Hist_log10My"+str(ip), NbrLogMBins, BinLogMMin, BinLogMMax)
            self.hist["Hist_GP_log10Mx"+str(ip)] =  ROOT.TH1D("Hist_GP_log10Mx"+str(ip), "Hist_GP_log10Mx"+str(ip), NbrLogMBins, BinLogMMin, BinLogMMax)
            self.hist["Hist_GP_log10My"+str(ip)] =  ROOT.TH1D("Hist_GP_log10My"+str(ip), "Hist_GP_log10My"+str(ip), NbrLogMBins, BinLogMMin, BinLogMMax)
            self.hist["Hist_GP_2Dlog10MxMy"+str(ip)] =  ROOT.TH2D("Hist_GP_2Dlog10MxMy"+str(ip), "Hist_GP_2Dlog10MxMy"+str(ip), NbrLogMBins, BinLogMMin, BinLogMMax, NbrLogMBins, BinLogMMin, BinLogMMax)
            self.hist["Hist_GP_log10XiX"+str(ip)] =  ROOT.TH1F("Hist_GP_log10XiX"+str(ip), "Hist_GP_log10XiX"+str(ip), NbrLogXiBins, BinLogXiMin, BinLogXiMax)
            self.hist["Hist_GP_log10XiY"+str(ip)] =  ROOT.TH1F("Hist_GP_log10XiY"+str(ip), "Hist_GP_log10XiY"+str(ip), NbrLogXiBins, BinLogXiMin, BinLogXiMax)
            self.hist["Hist_2D_calculated_log10XiDD_Deltamax"+str(ip)]= ROOT.TH2D("Hist_2D_calculated_log10XiDD_Deltamax"+str(ip),"Hist_2D_calculated_log10XiDD_Deltamax"+str(ip),NbrLogXiBins, BinLogXiMin,BinLogXiMax,NbrDetaBins, BinDetaMin, BinDetaMax)
            self.hist["Hist_Xi"+str(ip)] =  ROOT.TH1F("Hist_Xi"+str(ip), "Hist_Xi"+str(ip), NbrXiBins, BinXiMin, BinXiMax)
            self.hist["Hist_Xi"+str(ip)] =  ROOT.TH1F("Hist_Xi"+str(ip), "Hist_Xi"+str(ip), NbrXiBins, BinXiMin, BinXiMax)
            self.hist["Hist_XiX"+str(ip)] =  ROOT.TH1F("Hist_XiX"+str(ip), "Hist_XiX"+str(ip), NbrXiBins, BinXiMin, BinXiMax)
            self.hist["Hist_XiY"+str(ip)] =  ROOT.TH1F("Hist_XiY"+str(ip), "Hist_XiY"+str(ip), NbrXiBins, BinXiMin, BinXiMax)
            self.hist["Hist_log10Xi"+str(ip)] =  ROOT.TH1F("Hist_log10Xi"+str(ip), "Hist_log10Xi"+str(ip), NbrLogXiBins, BinLogXiMin, BinLogXiMax)
            self.hist["Hist_log10Xi"+str(ip)] =  ROOT.TH1F("Hist_log10Xi"+str(ip), "Hist_log10Xi"+str(ip), NbrLogXiBins, BinLogXiMin, BinLogXiMax)
            self.hist["Hist_log10XiX"+str(ip)] =  ROOT.TH1F("Hist_log10XiX"+str(ip), "Hist_log10XiX"+str(ip), NbrLogXiBins, BinLogXiMin, BinLogXiMax)
            self.hist["Hist_log10XiY"+str(ip)] =  ROOT.TH1F("Hist_log10XiY"+str(ip), "Hist_log10XiY"+str(ip), NbrLogXiBins, BinLogXiMin, BinLogXiMax)
            self.hist["Hist_2Dlog10XiXXiY"+str(ip)] = ROOT.TH2D("Hist_2Dlog10XiXXiY"+str(ip), "Hist_2Dlog10XiXXiY"+str(ip), NbrLogXiBins, BinLogXiMin, BinLogXiMax, NbrLogXiBins, BinLogXiMin, BinLogXiMax)
            self.hist["Hist_Reco_log10XiDD"+str(ip)] =  ROOT.TH1F("Hist_Reco_log10XiDD"+str(ip), "Hist_Reco_log10XiDD"+str(ip), NbrLogXiBins, BinLogXiMin, BinLogXiMax)
            self.hist["Hist_2DLogRecoXiX_logGenXiX"+str(ip)] = ROOT.TH2D("Hist_2DLogRecoXiX_logGenXiX"+str(ip), "Hist_2DLogRecoXiX_logGenXiX"+str(ip), NbrLogXiBins, BinLogXiMin, BinLogXiMax, NbrLogXiBins, BinLogXiMin, BinLogXiMax)
            self.hist["Hist_2DLogRecoXiY_logGenLogXiY"+str(ip)] = ROOT.TH2D("Hist_2DLogRecoXiY_logGenLogXiY"+str(ip), "Hist_2DLogRecoXiY_logGenLogXiY"+str(ip), NbrLogXiBins, BinLogXiMin, BinLogXiMax, NbrLogXiBins, BinLogXiMin, BinLogXiMax)
            self.hist["Hist_2DLogGenXiX_LogGenXiY"+str(ip)] = ROOT.TH2D("Hist_2DLogGenXiX_LogGenXiY"+str(ip), "Hist_2DLogGenXiX_LogGenXiY"+str(ip), NbrLogXiBins,BinLogXiMin, BinLogXiMax, NbrLogXiBins, BinLogXiMin, BinLogXiMax)
            self.hist["Hist_calculated_log10XiDD"+str(ip)] =  ROOT.TH1F("Hist_calculated_log10XiDD"+str(ip), "Hist_calculated_log10XiDD"+str(ip), NbrLogXiBins, BinLogXiMin, BinLogXiMax)
            self.hist["Hist_numberoftowerebovenoise_forwardplus"+str(ip)] = ROOT.TH1F("Hist_numberoftowerebovenoise_forwardplus"+str(ip),"Hist_numberoftowerebovenoise_forwardplus"+str(ip),30, 0,300) 
            self.hist["Hist_numberoftowerebovenoise_forwardminus"+str(ip)] = ROOT.TH1F("Hist_numberoftowerebovenoise_forwardminus"+str(ip),"Hist_numberoftowerebovenoise_forwardminus"+str(ip),30, 0,300) 
            self.hist["Hist_numberoftowerebovenoise_castor"+str(ip)] = ROOT.TH1F("Hist_numberoftowerebovenoise_castor"+str(ip),"Hist_numberoftowerebovenoise_castor"+str(ip),16, 0,16) 
            self.hist["Hist_NbrTracks"+str(ip)] = ROOT.TH1F("Hist_NbrTracks"+str(ip),"Hist_NbrTracks"+str(ip),NbrSizeBins, BinSizeEMin,100)
            self.hist["Hist_eventXiID_NbrTracks"+str(ip)] = ROOT.TH1F("Hist_eventXiID_NbrTracks"+str(ip),"Hist_eventXiID_NbrTracks"+str(ip),NbrSizeBins, BinSizeEMin,100)
            
            self.hist["Hist_numberoftowerebovenoise_endcap"+str(ip)] = ROOT.TH1F("Hist_numberoftowerebovenoise_endcap"+str(ip),"Hist_numberoftowerebovenoise_endcap"+str(ip),30, 0,300) 
            self.hist["Hist_numberoftowerebovenoise_barrel"+str(ip)] = ROOT.TH1F("Hist_numberoftowerebovenoise_barrel"+str(ip),"Hist_numberoftowerebovenoise_barrel"+str(ip),30, 0,300) 
            self.hist["Hist_numberoftowerebovenoise_endcapforwardtransition"+str(ip)] = ROOT.TH1F("Hist_numberoftowerebovenoise_endcapforwardtransition"+str(ip),"Hist_numberoftowerebovenoise_endcapforwardtransition"+str(ip),30, 0,300) 

            


             # eventID is process Id which is defined by the cuts that are applied on Xi , no using process ID from Pythi8
            self.hist["Hist_GP_eventXiID_Min"+str(ip)] = ROOT.TH1D("Hist_GP_eventXiID_Min"+str(ip),"Hist_GP_eventXiID_Min ", NbrEtaBins, BinEtaMin, BinEtaMax)
            self.hist["Hist_GP_eventXiID_Max"+str(ip)] = ROOT.TH1D("Hist_GP_eventXiID_Max"+str(ip),"Hist_GP_eventXiID_Max ", NbrEtaBins, BinEtaMin, BinEtaMax) 
            self.hist["Hist_GP_eventXiID_DeltaMax"+str(ip)] =  ROOT.TH1F("Hist_GP_eventXiID_DeltaMax"+str(ip), "Hist_GP_eventXiID_DeltaMax"+str(ip), NbrDetaBins, BinDetaMin, BinDetaMax)
            self.hist["Hist_GP_eventXiID_DeltaZero"+str(ip)] =  ROOT.TH1F("Hist_GP_eventXiID_DeltaZero"+str(ip), "Hist_GP_eventXiID_DeltaZero"+str(ip), NbrDetaBins, BinDetaMin, BinDetaMax)
            self.hist["Hist_eventXiID_Min"+str(ip)] = ROOT.TH1D("Hist_eventXiID_Min"+str(ip),"Hist_eventXiID_Min ", NbrEtaBins, BinEtaMin, BinEtaMax)
            self.hist["Hist_eventXiID_Max"+str(ip)] = ROOT.TH1D("Hist_eventXiID_Max"+str(ip),"Hist_eventXiID_Max ", NbrEtaBins, BinEtaMin, BinEtaMax) 
            self.hist["Hist_eventXiID_DeltaMax"+str(ip)] = ROOT.TH1F("Hist_eventXiID_DeltaMax"+str(ip), "Hist_eventXiID_DeltaMax"+str(ip), NbrDetaBins, BinDetaMin, BinDetaMax)
            self.hist["Hist_eventXiID_DeltaZero"+str(ip)] = ROOT.TH1F("Hist_eventXiID_DeltaZero"+str(ip), "Hist_eventXiID_DeltaZero"+str(ip), NbrDetaBins, BinDetaMin, BinDetaMax)
            self.hist["Hist_eventXiID_log10Mx"+str(ip)] = ROOT.TH1D("Hist_eventXiID_log10Mx"+str(ip), "Hist_eventXiID_log10Mx"+str(ip), NbrLogMBins, BinLogMMin, BinLogMMax)
            self.hist["Hist_eventXiID_log10My"+str(ip)] = ROOT.TH1D("Hist_eventXiID_log10My"+str(ip), "Hist_eventXiID_log10My"+str(ip), NbrLogMBins, BinLogMMin, BinLogMMax)
            self.hist["Hist_eventXiID_GP_2Dlog10MxMy"+str(ip)] =  ROOT.TH2D("Hist_eventXiID_GP_2Dlog10MxMy"+str(ip), "Hist_eventXiID_GP_2Dlog10MxMy"+str(ip), NbrLogMBins, BinLogMMin, BinLogMMax, NbrLogMBins, BinLogMMin, BinLogMMax)
            self.hist["Hist_eventXiID_log10XiX"+str(ip)] = ROOT.TH1F("Hist_eventXiID_log10XiX"+str(ip), "Hist_eventXiID_log10XiX"+str(ip), NbrLogXiBins, BinLogXiMin, BinLogXiMax)
            self.hist["Hist_eventXiID_log10XiY"+str(ip)] = ROOT.TH1F("Hist_eventXiID_log10XiY"+str(ip), "Hist_eventXiID_log10XiY"+str(ip), NbrLogXiBins, BinLogXiMin, BinLogXiMax)
            
          
            self.hist["Hist_GP_eventXiID_log10XiX"+str(ip)] = ROOT.TH1F("Hist_GP_eventXiID_log10XiX"+str(ip), "Hist_GP_eventXiID_log10XiX"+str(ip), NbrLogXiBins, BinLogXiMin, BinLogXiMax)
            self.hist["Hist_GP_eventXiID_log10XiY"+str(ip)] = ROOT.TH1F("Hist_GP_eventXiID_log10XiY"+str(ip), "Hist_GP_eventXiID_log10XiY"+str(ip), NbrLogXiBins, BinLogXiMin, BinLogXiMax)
            self.hist["Hist_eventXiID_2DLogGenXiX_LogGenXiY"+str(ip)] = ROOT.TH2D("Hist_eventXiID_2DLogGenXiX_LogGenXiY"+str(ip), "Hist_eventXiID_2DLogGenXiX_LogGenXiY"+str(ip), NbrLogXiBins,BinLogXiMin, BinLogXiMax, NbrLogXiBins, BinLogXiMin, BinLogXiMax)
            self.hist["Hist_eventXiID_Reco_log10XiDD"+str(ip)] = ROOT.TH1F("Hist_eventXiID_Reco_log10XiDD"+str(ip), "Hist_eventXiID_Reco_log10XiDD"+str(ip), NbrLogXiBins, BinLogXiMin, BinLogXiMax)
            self.hist["Hist_eventXiID_Energy"+str(ip)] =  ROOT.TH1F("Hist_eventXiID_Energy"+str(ip), "Hist_eventXiID_Energy"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_eventXiID_Energy_barrel"+str(ip)] = ROOT.TH1F("Hist_eventXiID_Energy_barrel"+str(ip), "Hist_eventXiID_Energy_barrel"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_eventXiID_Energy_endcap"+str(ip)] = ROOT.TH1F("Hist_eventXiID_Energy_endcap"+str(ip), "Hist_eventXiID_Energy_endcap"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_eventXiID_Energy_endcap_forwardtransition"+str(ip)] =  ROOT.TH1F("Hist_eventXiID_Energy_endcap_forwardtransition"+str(ip), "Hist_eventXiID_Energy_endcap_forwardtransition"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_eventXiID_Energy_forward"+str(ip)] =  ROOT.TH1F("Hist_eventXiID_Energy_forward"+str(ip), "Hist_eventXiID_Energy_forward"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_eventXiID_Energy_forwardplus"+str(ip)] =  ROOT.TH1F("Hist_eventXiID_Energy_forwardplus"+str(ip), "Hist_eventXiID_Energy_forwardplus"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_eventXiID_Energy_forwardminus"+str(ip)] =  ROOT.TH1F("Hist_eventXiID_Energy_forwardminus"+str(ip), "Hist_eventXiID_Energy_forwardminus"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_eventXiID_Energy_Castor"+str(ip)] =  ROOT.TH1F("Hist_eventXiID_Energy_Castor"+str(ip), "Hist_eventXiID_Energy_Castor"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_eventXiID_reducedEnergy"+str(ip)] =  ROOT.TH1F("Hist_eventXiID_reducedEnergy"+str(ip), "Hist_eventXiID_reducedEnergy"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_eventXiID_reducedEnergy_barrel"+str(ip)] =  ROOT.TH1F("Hist_eventXiID_reducedEnergy_barrel"+str(ip), "Hist_eventXiID_reducedEnergy_barrel"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_eventXiID_reducedEnergy_endcap"+str(ip)] =  ROOT.TH1F("Hist_eventXiID_reducedEnergy_endcap"+str(ip), "Hist_eventXiID_reducedEnergy_endcap"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_eventXiID_reducedEnergy_endcap_forwardtransition"+str(ip)] =  ROOT.TH1F("Hist_eventXiID_reducedEnergy_endcap_forwardtransition"+str(ip), "Hist_eventXiID_reducedEnergy_endcap_forwardtransition"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_eventXiID_reducedEnergy_forward"+str(ip)] =  ROOT.TH1F("Hist_eventXiID_reducedEnergy_forward"+str(ip), "Hist_eventXiID_reducedEnergy_forward"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_eventXiID_reducedEnergy_forwardplus"+str(ip)] =  ROOT.TH1F("Hist_eventXiID_reducedEnergy_forwardplus"+str(ip), "Hist_eventXiID_reducedEnergy_forwardplus"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_eventXiID_reducedEnergy_forwardminus"+str(ip)] =  ROOT.TH1F("Hist_eventXiID_reducedEnergy_forwardminus"+str(ip), "Hist_eventXiID_reducedEnergy_forwardminus"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_eventXiID_reducedEnergy_Castor"+str(ip)] =  ROOT.TH1F("Hist_eventXiID_reducedEnergy_Castor"+str(ip), "Hist_eventXiID_reducedEnergy_Castor"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_eventXiID_numberoftowerebovenoise_forwardplus"+str(ip)] = ROOT.TH1F("Hist_eventXiID_numberoftowerebovenoise_forwardplus"+str(ip),"Hist_eventXiID_numberoftowerebovenoise_forwardplus"+str(ip),30, 0,300) 
            self.hist["Hist_eventXiID_numberoftowerebovenoise_forwardminus"+str(ip)] = ROOT.TH1F("Hist_eventXiID_numberoftowerebovenoise_forwardminus"+str(ip),"Hist_eventXiID_numberoftowerebovenoise_forwardminus"+str(ip),30, 0,300) 
            self.hist["Hist_eventXiID_numberoftowerebovenoise_castor"+str(ip)] = ROOT.TH1F("Hist_eventXiID_numberoftowerebovenoise_castor"+str(ip),"Hist_eventXiID_numberoftowerebovenoise_castor"+str(ip),16, 0,16) 
          
            



      
        for h in self.hist:
            self.hist[h].Sumw2()
            self.GetOutputList().Add(self.hist[h])

        self.pdg_helper = pd.PYTHIAParticleData()
        self.castor_tower_p4 = []
        self.CMenergy = 13000 # GeV
        self.protonmass = 0.938 # GeV
        self.Xi_p = -8.28 # Mp*2/CMenergylog10(1/13e3/13e3)
        for isec in xrange(0,16):
            self.castor_tower_p4.append( ROOT.ROOT.Math.LorentzVector('ROOT::Math::PxPyPzE4D<double>')(0,0,0,0) )

        sigTree = ROOT.TTree("sigTree", "selected DD events")

        self.OUTlog10XixGen = array( 'f', 1 * [0] )
        self.OUTlog10XiyGen = array( 'f', 1 * [0] )
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
        self.OUTCastorNtowers = array( 'i', 1 * [0] )
        self.OUTHFminusNtowers = array( 'i', 1 * [0] )
        self.OUTNtracks = array( 'i', 1 * [0] )
        self.OUTHFplusNtowers = array( 'i', 1 * [0] )
        self.OUTlog10XiDD = array( 'f', 1 * [0] )
        self.OUTPythia8processid = array( 'i', 1 * [0] )
        self.OUTEventselectionXiprocessid = array( 'i', 1 * [0] )

        sigTree.Branch('EventselectionXiprocessid', self.OUTEventselectionXiprocessid,'EventselectionXiprocessid/I')
        sigTree.Branch('Pythia8processid', self.OUTPythia8processid,'Pythia8processid/I')
        sigTree.Branch('log10XixGen', self.OUTlog10XixGen,'log10XixGen/F')
        sigTree.Branch('log10XiyGen', self.OUTlog10XiyGen,'log10XiyGen/F')
        sigTree.Branch('log10XixReco', self.OUTlog10XixReco,'log10XixReco/F')
        sigTree.Branch('log10XiyReco', self.OUTlog10XiyReco,'log10XiyReco/F')
        sigTree.Branch('deltazero', self.OUTdeltazero,'deltazero/F')
        sigTree.Branch('delta', self.OUTdelta,'delta/F')
        sigTree.Branch('etamin', self.OUTetamin, 'etamin/F')
        sigTree.Branch('RGmean', self.OUTrapditygapmean,'RGmean/F')
        sigTree.Branch('etamax', self.OUTetamax, 'etamax/F')
        sigTree.Branch('CastorNtowers', self.OUTCastorNtowers, 'CastorNtowers/I')
        sigTree.Branch('HFminusNtowers', self.OUTHFminusNtowers,'HFminusNtowers/I')
        sigTree.Branch('HFplusNtowers', self.OUTHFplusNtowers,'HFplusNtowers/I')
        sigTree.Branch('Ntracks', self.OUTNtracks,'Ntracks/I')

        

        sigTree.Branch('log10XiDD', self.OUTlog10XiDD,'log10XiDD/F')

        setattr(self, "sigTree", sigTree)
        self.addToOutput(self.sigTree)
        
        bkgTree = ROOT.TTree("bkgTree", "all events except DD")
        bkgTree.Branch('EventselectionXiprocessid', self.OUTEventselectionXiprocessid,'EventselectionXiprocessid/I')
        bkgTree.Branch('Pythia8processid', self.OUTPythia8processid,'Pythia8processid/I')
        bkgTree.Branch('log10XixGen', self.OUTlog10XixGen, 'log10XixGen/F')
        bkgTree.Branch('log10XiyGen', self.OUTlog10XiyGen, 'log10XiyGen/F')
        bkgTree.Branch('log10XixReco', self.OUTlog10XixReco, 'log10XixReco/F')
        bkgTree.Branch('log10XiyReco', self.OUTlog10XiyReco, 'log10XiyReco/F')
        bkgTree.Branch('delta', self.OUTdelta, 'delta/F')
        bkgTree.Branch('deltazero', self.OUTdeltazero, 'deltazero/F')
        bkgTree.Branch('etamin', self.OUTetamin, 'etamin/F')
        bkgTree.Branch('etamax', self.OUTetamax, 'etamax/F')
        bkgTree.Branch('RGmean', self.OUTrapditygapmean,'RGmean/F')
        bkgTree.Branch('CastorNtowers', self.OUTCastorNtowers, 'CastorNtowers/I')
        bkgTree.Branch('HFminusNtowers', self.OUTHFminusNtowers, 'HFminusNtowers/I')
        bkgTree.Branch('HFplusNtowers', self.OUTHFplusNtowers, 'HFplusNtowers/I')
        bkgTree.Branch('log10XiDD', self.OUTlog10XiDD,'log10XiDD/F')
        bkgTree.Branch('Ntracks', self.OUTNtracks,'Ntracks/I')
        setattr(self, "bkgTree",bkgTree)
        self.addToOutput(self.bkgTree)
        



        AllTree = ROOT.TTree("AllTree", "all events")
        AllTree.Branch('EventselectionXiprocessid', self.OUTEventselectionXiprocessid,'EventselectionXiprocessid/I')
        AllTree.Branch('Pythia8processid', self.OUTPythia8processid,'Pythia8processid/I')
        AllTree.Branch('log10XixGen', self.OUTlog10XixGen, 'log10XixGen/F')
        AllTree.Branch('log10XiyGen', self.OUTlog10XiyGen, 'log10XiyGen/F')
        AllTree.Branch('log10XixReco', self.OUTlog10XixReco, 'log10XixReco/F')
        AllTree.Branch('log10XiyReco', self.OUTlog10XiyReco, 'log10XiyReco/F')
        AllTree.Branch('delta', self.OUTdelta, 'delta/F')
        AllTree.Branch('deltazero', self.OUTdeltazero, 'deltazero/F')
        AllTree.Branch('etamin', self.OUTetamin, 'etamin/F')
        AllTree.Branch('etamax', self.OUTetamax, 'etamax/F')
        AllTree.Branch('RGmean', self.OUTrapditygapmean,'RGmean/F')
        AllTree.Branch('CastorNtowers', self.OUTCastorNtowers, 'CastorNtowers/I')
        AllTree.Branch('HFminusNtowers', self.OUTHFminusNtowers, 'HFminusNtowers/I')
        AllTree.Branch('HFplusNtowers', self.OUTHFplusNtowers, 'HFplusNtowers/I')
        AllTree.Branch('log10XiDD', self.OUTlog10XiDD,'log10XiDD/F')
        AllTree.Branch('Ntracks', self.OUTNtracks,'Ntracks/I')
        setattr(self, "AllTree",AllTree)
        self.addToOutput(self.AllTree)
        

    def get_Pythia_Process_ID(self):
        # if self.fChain.processID == 101:
        #     return '_Rest', self.fChain.processID
        if self.fChain.processID == 103:
            return '_SD1', self.fChain.processID
        if self.fChain.processID == 104:
            return '_SD2', self.fChain.processID
        if self.fChain.processID == 105:
            return '_DD', self.fChain.processID
        # if self.fChain.processID == 106:
        #     return '_CD', self.fChain.processID

        return '_Rest', -1


        
    def get_EventSelectionXiProcess_ID(self,GenXi_DD,GenXiX,GenXiY):
        if (log10(GenXi_DD) > -3) :
            return '_Rest', -1
        elif (log10(GenXiY) < self.Xi_p + 0.04) and (log10(GenXiY) > self.Xi_p-0.04):
            return '_SD1', 103 
        elif (log10(GenXiX) < self.Xi_p + 0.04) and (log10(GenXiX) > self.Xi_p -0.04):
            return '_SD2', 104
        
        return '_DD', 105
          

    def get_Process_ID_from_String(self,process):
        if process == 'Rest':
            return -1
        if process == 'SD1':
            return 103
        if process == 'SD2':
            return 104
        if process == 'DD':
            return 105
        if process == 'CD':
            return -1

        return -1


    def analyze(self):
        Nbrvertex = 1 

        if self.isData:
            # if not self.fChain.run == 247324 and not self.fChain.run == 247934: return 1 
        
            Nbrvertex = self.fChain.ZeroTeslaPixelnoPreSplittingVtx_vrtxX.size()    
            self.hist["Hist_NrVtx"].Fill(Nbrvertex)

            if Nbrvertex > 2:  return 0

            if Nbrvertex == 2:
                if abs(self.fChain.ZeroTeslaPixelnoPreSplittingVtx_vrtxZ[0] - self.fChain.ZeroTeslaPixelnoPreSplittingVtx_vrtxZ[1])> 0.5 : return 0
                Nbrvertex = 1

        

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
        
        self.hist["hProcessescut"].Fill("all",1)
        self.hist["hProcessesIdPythia"].Fill("all",1)

        Pythia_Process_ID = '_NONE'
        int_Pythia_Process_ID = -11
        EventSelectionXiProcess_ID = '_NONE'
        int_EventSelectionXiProcess_ID = -11
        
        if not self.isData:
            Pythia_Process_ID, int_Pythia_Process_ID = self.get_Pythia_Process_ID()
            self.hist["hProcessesIdPythia"].Fill(Pythia_Process_ID[1:],1)
   

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
                    

        
        # if HFCut == False : return 0
        
        Eta = 0
        GenParticleClass = []
        ChargedGenParticleClass = []
        theta = 0
        mingeneta = -1
        maxgeneta = -1
        deltaeta=-1
        delta_zero_gen = -1
        delta_max_gen = -1
        delta_Gen_zero_pos = -1
        deltaetamax_Gen_pos = -1
        # deltagenreco = -1
        Etarange = -1
       
        # self.hist["hNentriess"].Fill("hf cut",1)         
       
        if  not self.isData:
           
            ngenParticle = self.fChain.genParticlesp4.size()
            # final state particles from the genParticles collection
            for igenP in xrange(ngenParticle):
                genp4 = self.fChain.genParticlesp4[igenP]
                genid = self.fChain.genParticlespdg[igenP]
                genst = self.fChain.genParticlesstatus[igenP]
              
                # if genst != 1: continue
                GenParticleClass.append([genp4,genid])
                if self.pdg_helper.charge(genid) == 0 : continue ######### only use charged particles
                ChargedGenParticleClass.append([genp4,genid])
       
       
            # if len(ChargedGenParticleClass) == 0:
            #     return 0

            ChargedGenParticleClass.sort(cmp=compareGeneta)
            mingeneta = ChargedGenParticleClass[0][0].eta()
            maxgeneta = ChargedGenParticleClass[len(ChargedGenParticleClass)-1][0].eta()
            self.hist["Hist_GP_Min"].Fill(mingeneta)
            self.hist["Hist_GP_Max"].Fill(maxgeneta)
            Etarange = maxgeneta - mingeneta
            self.hist["Hist_GP_Delta"].Fill(Etarange)
           

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

            
            self.hist["Hist_GP_DeltaMax"].Fill(delta_max_gen)
            self.hist["Hist_GP_DeltaZero"].Fill(delta_zero_gen)
            self.hist["Hist_GP_Min" + Pythia_Process_ID].Fill(mingeneta)
            self.hist["Hist_GP_Max" + Pythia_Process_ID].Fill(maxgeneta)  
            self.hist["Hist_GP_Delta" + Pythia_Process_ID].Fill(Etarange)
            self.hist["Hist_GP_DeltaMax" + Pythia_Process_ID].Fill(delta_max_gen)
            self.hist["Hist_GP_DeltaZero" + Pythia_Process_ID].Fill(delta_zero_gen)
            
           

            # if len(GenParticleClass) == 0:
            #     return 0

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
            MeanGen =0
            Px = 0
            Py= 0
            Px2 = 0
            Py2= 0
            GenXi_DD = 0

            for igp in xrange(0,len(GenParticleClass)): 
                if GenParticleClass[igp][0].eta() <= ChargedGenParticleClass[deltaetamax_Gen_pos][0].eta():
                    XGenEtot += GenParticleClass[igp][0].E()
                    XPxtot += GenParticleClass[igp][0].Px()
                    XPytot += GenParticleClass[igp][0].Py()
                    XPztot += GenParticleClass[igp][0].Pz()
                    
                   

                if GenParticleClass[igp][0].eta() >= ChargedGenParticleClass[deltaetamax_Gen_pos+1][0].eta():
                    YGenEtot += GenParticleClass[igp][0].E()
                    YPxtot += GenParticleClass[igp][0].Px()
                    YPytot += GenParticleClass[igp][0].Py()
                    YPztot += GenParticleClass[igp][0].Pz()
                    




                MeanGen = (ChargedGenParticleClass[deltaetamax_Gen_pos+1][0].eta() + ChargedGenParticleClass[deltaetamax_Gen_pos][0].eta())/2 
               

            Px2 =  XPxtot**2 + XPytot**2 +XPztot**2
            Py2 =  YPxtot**2 + YPytot**2 +YPztot**2
            Px = sqrt(Px2)
            Py = sqrt(Py2)

            Mx2 = (XGenEtot+Px)*(XGenEtot-Px)
            My2 = (YGenEtot+Py)*(YGenEtot-Py)  
            if Mx2<=0: Mx2=1.01e-6
            if My2<=0: My2=1.01e-6
          
           
            MyGen = sqrt(My2)
            MxGen = sqrt(Mx2)
            self.hist["Hist_GP_Mx"].Fill(MxGen)
            self.hist["Hist_GP_log10Mx"].Fill(log10(MxGen))
            self.hist["Hist_GP_My"].Fill(MyGen)
            self.hist["Hist_GP_log10My"].Fill(log10(MyGen))
            self.hist["Hist_GP_2Dlog10MxMy"].Fill(log10(MxGen),log10(MyGen))
            
            self.hist["Hist_GP_log10Mx"+ Pythia_Process_ID].Fill(log10(MxGen))
            self.hist["Hist_GP_log10My"+ Pythia_Process_ID].Fill(log10(MyGen))
            self.hist["Hist_GP_2Dlog10MxMy"+ Pythia_Process_ID].Fill(log10(MxGen),log10(MyGen))

            
           

          
            GenXiX = Mx2/self.CMenergy/self.CMenergy
            GenXiY = My2/self.CMenergy/self.CMenergy
            GenXi_DD = Mx2*My2/(self.protonmass**2 * self.CMenergy**2)

            self.hist["Hist_GP_log10XiX"].Fill(log10(GenXiX))
            self.hist["Hist_GP_log10XiY"].Fill(log10(GenXiY))
            self.hist["Hist_GP_log10XiX"+Pythia_Process_ID].Fill(log10(GenXiX))
            self.hist["Hist_GP_log10XiY"+Pythia_Process_ID].Fill(log10(GenXiY))
            self.hist["Hist_2DLogGenXiX_LogGenXiY"].Fill(log10(GenXiX),log10(GenXiY))
            self.hist["Hist_2DLogGenXiX_LogGenXiY"+Pythia_Process_ID].Fill(log10(GenXiX),log10(GenXiY))
            
            self.hist["Hist_calculated_log10XiDD"].Fill(log10(GenXi_DD))  
            self.hist["Hist_calculated_log10XiDD"+Pythia_Process_ID].Fill(log10(GenXi_DD)) 
            
            self.hist["Hist_2D_calculated_log10XiDD_Deltamax"].Fill(log10(GenXi_DD), delta_max_gen)
            self.hist["Hist_2D_calculated_log10XiDD_Deltamax"+Pythia_Process_ID].Fill(log10(GenXi_DD), delta_max_gen)
           

            EventSelectionXiProcess_ID, int_EventSelectionXiProcess_ID = self.get_EventSelectionXiProcess_ID(GenXi_DD,GenXiX,GenXiY)
            self.hist["hProcessescut"].Fill(EventSelectionXiProcess_ID[1:],1)
           

                
            self.hist["Hist_GP_eventXiID_DeltaMax"].Fill(delta_max_gen)
            self.hist["Hist_GP_eventXiID_DeltaZero"].Fill(delta_zero_gen)
            self.hist["Hist_GP_eventXiID_DeltaMax"+ EventSelectionXiProcess_ID].Fill(delta_max_gen)
            self.hist["Hist_GP_eventXiID_DeltaZero"+ EventSelectionXiProcess_ID].Fill(delta_zero_gen)
            self.hist["Hist_GP_eventXiID_Min"].Fill(mingeneta)
            self.hist["Hist_GP_eventXiID_Max"].Fill(maxgeneta) 
            self.hist["Hist_GP_eventXiID_Min"+ EventSelectionXiProcess_ID].Fill(mingeneta)
            self.hist["Hist_GP_eventXiID_Max"+ EventSelectionXiProcess_ID].Fill(maxgeneta)  
            
            self.hist["Hist_eventXiID_log10Mx"+ EventSelectionXiProcess_ID].Fill(log10(MxGen))
            self.hist["Hist_eventXiID_log10My"+ EventSelectionXiProcess_ID].Fill(log10(MyGen))
            self.hist["Hist_eventXiID_GP_2Dlog10MxMy"+ EventSelectionXiProcess_ID].Fill(log10(MxGen),log10(MyGen))

          
            self.hist["Hist_GP_eventXiID_log10XiX"].Fill(log10(GenXiX))
            self.hist["Hist_GP_eventXiID_log10XiY"].Fill(log10(GenXiY)) 
            self.hist["Hist_GP_eventXiID_log10XiX"+EventSelectionXiProcess_ID].Fill(log10(GenXiX))
            self.hist["Hist_GP_eventXiID_log10XiY"+EventSelectionXiProcess_ID].Fill(log10(GenXiY))
            self.hist["Hist_eventXiID_2DLogGenXiX_LogGenXiY"+EventSelectionXiProcess_ID].Fill(log10(GenXiX),log10(GenXiY))


           
            
    ##################Track##############################################################3
        TrackCandClass = []
        Nbrtracks = 0
        nTrackCand = self.fChain.ZeroTeslaPixelnoPreSplittingVtx_trktheta.size()
        for itrk in xrange(nTrackCand):
            theta= self.fChain.ZeroTeslaPixelnoPreSplittingVtx_trktheta[itrk]
            trkphi = self.fChain.ZeroTeslaPixelnoPreSplittingVtx_trkphi[itrk]
            Eta = -np.log(math.tan(theta/2))
            TrackCandClass.append([Eta,trkphi])
            
       
        mineta = -5
        maxeta = 5
        Etarange = -1

        # if len(TrackCandClass) == 0:
        #     return 0

        if len(TrackCandClass) > 0:
            TrackCandClass.sort(cmp=compareTracketa)
            mineta =  TrackCandClass[0][0]
            maxeta =  TrackCandClass[len(TrackCandClass)-1][0] #eta()pseduorapidty
     
        #self.hist["Hist_TrackCandClass"].Fill(len(TrackCandClass))  
        self.hist["Hist_NbrTracks"].Fill(len(TrackCandClass))  
        self.hist["Hist_NbrTracks"+ Pythia_Process_ID].Fill(len(TrackCandClass))
        self.hist["Hist_eventXiID_NbrTracks"].Fill(len(TrackCandClass))  
        self.hist["Hist_eventXiID_NbrTracks"+EventSelectionXiProcess_ID].Fill(len(TrackCandClass))
        
    
        Nbrtracks = len(TrackCandClass)
        
        self.hist["Hist_Eta_Min"].Fill(mineta)
        self.hist["Hist_Eta_Max"].Fill(maxeta)
        self.hist["Hist_Eta_Delta"].Fill(Etarange)  
        self.hist["Hist_Eta_Min" + Pythia_Process_ID].Fill(mineta)
        self.hist["Hist_Eta_Max" + Pythia_Process_ID].Fill(maxeta)  
        self.hist["Hist_Eta_Delta" + Pythia_Process_ID].Fill(Etarange) 
        self.hist["Hist_eventXiID_Min"].Fill(mineta)
        self.hist["Hist_eventXiID_Max"].Fill(maxeta) 
        self.hist["Hist_eventXiID_Min"+ EventSelectionXiProcess_ID].Fill(mineta)
        self.hist["Hist_eventXiID_Max"+ EventSelectionXiProcess_ID].Fill(maxeta)  
        # self.hist["hNentries"].Fill("Track",1)    

        deltaeta = -1
        delta_zero = -1
#        delta_Reco_zero_pos = -1
        deltaetamax = -1
 #       deltaetamax_Reco_pos = -1
        minangle = float("inf")
        # r = -10000
        rapidityGapeta= 0

        if len(TrackCandClass) > 1:
            for jtrk in xrange(0,len(TrackCandClass)-1): #change   GenParticleClass to  TrackCandClass for testing
                tracketa  =  TrackCandClass[jtrk][0]
                trackphi = TrackCandClass[jtrk][1]
                # trackid  =  TrackCandClass[itrack][1]

                self.hist["Hist_trkEta"].Fill(TrackCandClass[jtrk][0])
                # deltaeta =  TrackCandClass[itrack+1][0].eta() -  TrackCandClass[itrack][0].eta()
                deltaeta =  TrackCandClass[jtrk+1][0] - TrackCandClass[jtrk][0] #eta()pseduorapidty
                self.hist["Hist_trkplusEta"].Fill(TrackCandClass[jtrk+1][0])
                if  (deltaeta > deltaetamax):
                    deltaetamax = deltaeta
#                    deltaetamax_Reco_pos = jtrk
                    rapidityGapeta = (TrackCandClass[jtrk+1][0] +  TrackCandClass[jtrk][0])/2 
                    
                if  TrackCandClass[jtrk+1][0] > 0 and TrackCandClass[jtrk][0]< 0:
                    delta_zero = deltaeta
                    #delta_Reco_zero_pos = jtrk
                


         ####################################Calotower######################################


        CaloCandClass = []
        CaloReducedenergyClass = []
        CaloTower = self.fChain.CaloTowersp4.size()
       
        #noise cut i am using the vrtx cut ==0 and vrtx cut ==1
         
      
        CASTOR_Numberoftowerebovenoise = 0
        HFplus_Numberoftowerebovenoise = 0 
        HFminus_Numberoftowerebovenoise = 0 
        Barrel_Numberoftowerebovenoise = 0 
        Endcap_Numberoftowerebovenoise = 0 
        endcapforwardtransition_Numberoftowerebovenoise =0

       
    

        for icalo in xrange(0,CaloTower):
            calop4 = self.fChain.CaloTowersp4[icalo]
            caloem = self.fChain.CaloTowersemEnergy[icalo]
            calohad = self.fChain.CaloTowershadEnergy[icalo]
            caloieta = self.fChain.CaloTowersieta[icalo]
            caloiphi = self.fChain.CaloTowersiphi[icalo] 

            if is in bad_channels_eta_phi continue

            CaloCandClass.append([calop4,caloem,calohad])
            
           
            if abs(calop4.eta()) < 1.4:
               
                if (calop4.e()) < 2.00: continue
                Barrel_Numberoftowerebovenoise += 1 


            if abs( calop4.eta()) > 1.4 and abs( calop4.eta()) < 2.8:
                if (calop4.e()) < 1.80: continue
                Endcap_Numberoftowerebovenoise += 1

            if abs( calop4.eta()) > 2.8 and abs( calop4.eta()) < 3.2: 
                if (calop4.e()) < 3.8: continue
                endcapforwardtransition_Numberoftowerebovenoise += 1  
                 
            # if abs(calop4.eta()) > 3.2 and abs(calop4.eta()) < 5.2 :
            #     if (calop4.e()) < 2.2: continue
            #     endcapforwardtransition_Numberoftowerebovenoise += 1  

            if  calop4.eta() > 3.2 and calop4.eta() < 5.2:
                calop4 *= HF_energy_scale
                if (calop4.e()) <5: continue
                HFplus_Numberoftowerebovenoise += 1
                # self.hist["Hist_Energy_forwardplus"]
            if  calop4.eta() > -5.2 and calop4.eta() < -3.2:
                calop4 *= HF_energy_scale
                if (calop4.e()) <5: continue
                HFminus_Numberoftowerebovenoise += 1
                # self.hist["Hist_Energy_forwardminus"]


            CaloReducedenergyClass.append([calop4,caloem,calohad,caloieta,caloiphi])
         
      
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

            if (energy) < 1.5:continue   #Threshold for castor: 5.600000 ############# Castor noise cut
            CASTOR_Numberoftowerebovenoise += 1

            CaloReducedenergyClass.append([self.castor_tower_p4[isec], 
                                # self.castor_id[isec],
                                self.sum_CAS_E_em[isec],
                                self.sum_CAS_E_had[isec],
                                1111,1111]) # something strange for ieta, iphi
    


        for icalo in CaloReducedenergyClass:
          
            CaloTwriEta = icalo[3]
            CaloTwrsiPhi = icalo[4]

            self.hist["Calotower2D_eta_phi"].Fill(CaloTwriEta,CaloTwrsiPhi)
            self.hist["Calotower2D_Energy_eta_phi"].Fill(CaloTwriEta, CaloTwrsiPhi, icalo[0].e() )
     

        ####### Vrtx cut######  
        if self.isData:
            if Nbrtracks== 0 and len(CaloReducedenergyClass) == 0: return 0
            # if not self.fChain.ZeroTeslaPixelnoPreSplittingVtx_vrtxX.size() == 1 and len(CaloReducedenergyClass) < 1: return 0
       
            
        # if len(CaloReducedenergyClass) == 0:
        #     return 0
        # self.hist["hNentries"].Fill("CaloReducedenergyClass1",1)
    
        for icalo in xrange(0,len(CaloReducedenergyClass)):
            if calop4.eta() < mineta:
                mineta = calop4.eta() 
            if calop4.eta() > maxeta:   
                maxeta = calop4.eta() 
           
            calop4  = CaloReducedenergyClass[icalo][0]
            caloem  = CaloReducedenergyClass[icalo][1]
            calohad  = CaloReducedenergyClass[icalo][2]
           
            
            self.hist["Hist_reducedEta"].Fill(calop4.eta()) 
            self.hist["Hist_reducedEnergy"].Fill(calop4.e())
            self.hist["Hist_eventXiID_reducedEnergy"].Fill(calop4.e())         

            self.hist["Hist_reducedEta" + Pythia_Process_ID].Fill(calop4.eta())     
            self.hist["Hist_reducedEnergy" + Pythia_Process_ID].Fill(calop4.e()) 
            self.hist["Hist_reducedEnergy" + EventSelectionXiProcess_ID].Fill(calop4.e())      
           
            self.hist["hParticleCounts"].Fill("all",1)
          
            

            if abs( calop4.eta() ) < 1.4:
                self.hist["Hist_reducedEnergy_barrel"].Fill(calop4.e()) 
                self.hist["Hist_reducedEnergy_barrel" + Pythia_Process_ID].Fill(calop4.e()) 
                self.hist["Hist_eventXiID_reducedEnergy_barrel"].Fill(calop4.e()) 
                self.hist["Hist_eventXiID_reducedEnergy_barrel" + EventSelectionXiProcess_ID].Fill(calop4.e()) 


            if  abs( calop4.eta() ) > 1.4 and abs( calop4.eta() ) < 2.8:
                self.hist["Hist_reducedEnergy_endcap"].Fill(calop4.e()) 
                self.hist["Hist_reducedEnergy_endcap" + Pythia_Process_ID].Fill(calop4.e()) 
                self.hist["Hist_eventXiID_reducedEnergy_endcap"].Fill(calop4.e()) 
                self.hist["Hist_eventXiID_reducedEnergy_endcap" + EventSelectionXiProcess_ID].Fill(calop4.e()) 
                                       
           
            if  abs( calop4.eta() ) > 2.8 and abs( calop4.eta() ) < 3.2:
                self.hist["Hist_reducedEnergy_endcap_forwardtransition"].Fill(calop4.e()) 
                self.hist["Hist_reducedEnergy_endcap_forwardtransition" + Pythia_Process_ID].Fill(calop4.e()) 
                self.hist["Hist_eventXiID_reducedEnergy_endcap_forwardtransition"].Fill(calop4.e()) 
                self.hist["Hist_eventXiID_reducedEnergy_endcap_forwardtransition" + EventSelectionXiProcess_ID].Fill(calop4.e()) 
                            

            if  abs (calop4.eta()) > 3.2 and abs(calop4.eta()) < 5.2:
                self.hist["Hist_reducedEnergy_forward"].Fill(calop4.e())
                self.hist["Hist_reducedEnergy_forward" + Pythia_Process_ID].Fill(calop4.e()) 
                self.hist["Hist_eventXiID_reducedEnergy_forward"].Fill(calop4.e())
                self.hist["Hist_eventXiID_reducedEnergy_forward" + EventSelectionXiProcess_ID].Fill(calop4.e()) 
                    
            if calop4.eta() > 3.2 and calop4.eta() < 5.2:
                self.hist["Hist_reducedEnergy_forwardplus"].Fill(calop4.e())
                self.hist["Hist_reducedEnergy_forwardplus" + Pythia_Process_ID].Fill(calop4.e()) 
                self.hist["Hist_eventXiID_reducedEnergy_forwardplus"].Fill(calop4.e())
                self.hist["Hist_eventXiID_reducedEnergy_forwardplus" + EventSelectionXiProcess_ID].Fill(calop4.e()) 
                

            if calop4.eta() > -5.2 and calop4.eta() < -3.2:
                self.hist["Hist_reducedEnergy_forwardminus"].Fill(calop4.e())
                self.hist["Hist_reducedEnergy_forwardminus" + Pythia_Process_ID].Fill(calop4.e()) 
                self.hist["Hist_eventXiID_reducedEnergy_forwardminus"].Fill(calop4.e())
                self.hist["Hist_eventXiID_reducedEnergy_forwardminus" + EventSelectionXiProcess_ID].Fill(calop4.e()) 
               
           
            if  (calop4.eta()) > -6.6 and (calop4.eta()) < -5.2 :
                self.hist["Hist_reducedEnergy_Castor"].Fill(calop4.e())
                # CASTOR_Numberoftowerebovenoise += calop4.e()
                self.hist["Hist_reducedEnergy_Castor" + Pythia_Process_ID].Fill(calop4.e()) 
                self.hist["Hist_eventXiID_reducedEnergy_Castor"].Fill(calop4.e())
                self.hist["Hist_eventXiID_reducedEnergy_Castor" + EventSelectionXiProcess_ID].Fill(calop4.e()) 
            
        Etarange = maxeta - mineta
        self.hist["Hist_Eta_DeltaZero"].Fill(delta_zero)
        self.hist["Hist_Eta_DeltaMax"].Fill(deltaetamax)
        self.hist["Hist_Eta_DeltaMax"+ Pythia_Process_ID].Fill(deltaetamax)
        self.hist["Hist_Eta_DeltaZero"+ Pythia_Process_ID].Fill(delta_zero)
      
        self.hist["Hist_eventXiID_DeltaMax"].Fill(deltaetamax)
        self.hist["Hist_eventXiID_DeltaZero"].Fill(delta_zero)
        self.hist["Hist_eventXiID_DeltaMax"+ EventSelectionXiProcess_ID].Fill(deltaetamax)
        self.hist["Hist_eventXiID_DeltaZero"+ EventSelectionXiProcess_ID].Fill(delta_zero)
        

        deltagenreco = (delta_zero_gen - delta_zero)
        self.hist["Hist_Deltazero_deltagenreco"].Fill(deltagenreco)
        self.hist["Hist_2D_recogen_DeltaZero"].Fill(delta_zero, delta_zero_gen)
        self.hist["Hist_2D_recogen_DeltaMax"].Fill(deltaetamax, delta_max_gen) 
        self.hist["Hist_2D_recogen_EtaMiniumum"].Fill(mineta,mingeneta)
        self.hist["Hist_2D_recogen_EtaMax"].Fill(maxeta,maxgeneta)
            # self.hist["hNentries"].Fill("CaloReducedenergyClass2",1) 



               
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

          

        # if len(CaloCandClass) == 0:
        #     return 0
        
       
        self.hist["hNentries"].Fill("CaloCandClass1",1)    
        for icalo in xrange(0,len(CaloCandClass)):
            calop4  = CaloCandClass[icalo][0]
            caloem  = CaloCandClass[icalo][1]
            calohad  = CaloCandClass[icalo][2]
           
            
            self.hist["Hist_Eta"].Fill(calop4.eta()) 
            self.hist["Hist_Energy"].Fill(calop4.e())     

            self.hist["Hist_Eta" + Pythia_Process_ID].Fill(calop4.eta())     
            self.hist["Hist_Energy" + Pythia_Process_ID].Fill(calop4.e())     
            self.hist["Hist_eventXiID_Energy" + EventSelectionXiProcess_ID].Fill(calop4.e())  
            self.hist["hParticleCounts"].Fill("all",1)
           
            

            if abs( calop4.eta() ) < 1.4:
                self.hist["Hist_Energy_barrel"].Fill(calop4.e()) 
                self.hist["Hist_Energy_barrel" + Pythia_Process_ID].Fill(calop4.e()) 
                self.hist["Hist_eventXiID_Energy_barrel"].Fill(calop4.e()) 
                self.hist["Hist_eventXiID_Energy_barrel" + EventSelectionXiProcess_ID].Fill(calop4.e()) 
               

            if  abs( calop4.eta() ) > 1.4 and abs( calop4.eta() ) <2.8:
                self.hist["Hist_Energy_endcap"].Fill(calop4.e()) 
                self.hist["Hist_Energy_endcap" + Pythia_Process_ID].Fill(calop4.e()) 
                self.hist["Hist_eventXiID_Energy_endcap"].Fill(calop4.e()) 
                self.hist["Hist_eventXiID_Energy_endcap" + EventSelectionXiProcess_ID].Fill(calop4.e()) 
                                       
           
            if  abs( calop4.eta() ) > 2.8 and abs( calop4.eta() ) < 3.2:
                self.hist["Hist_Energy_endcap_forwardtransition"].Fill(calop4.e()) 
                self.hist["Hist_Energy_endcap_forwardtransition" + Pythia_Process_ID].Fill(calop4.e()) 
                self.hist["Hist_eventXiID_Energy_endcap_forwardtransition"].Fill(calop4.e()) 
                self.hist["Hist_eventXiID_Energy_endcap_forwardtransition" + EventSelectionXiProcess_ID].Fill(calop4.e()) 
                            

            if  abs (calop4.eta()) > 3.2 and abs(calop4.eta()) < 5.2:
                self.hist["Hist_Energy_forward"].Fill(calop4.e())
                self.hist["Hist_Energy_forward" + Pythia_Process_ID].Fill(calop4.e()) 
                self.hist["Hist_eventXiID_Energy_forward"].Fill(calop4.e())
                self.hist["Hist_eventXiID_Energy_forward" + EventSelectionXiProcess_ID].Fill(calop4.e()) 
                    
            if calop4.eta() > 3.2 and calop4.eta() < 5.2:
                self.hist["Hist_Energy_forwardplus"].Fill(calop4.e())
                self.hist["Hist_Energy_forwardplus" + Pythia_Process_ID].Fill(calop4.e()) 
                self.hist["Hist_eventXiID_Energy_forwardplus"].Fill(calop4.e())
                self.hist["Hist_eventXiID_Energy_forwardplus" + EventSelectionXiProcess_ID].Fill(calop4.e())
         
            if calop4.eta() > -5.2 and calop4.eta() < -3.2:
                self.hist["Hist_Energy_forwardminus"].Fill(calop4.e())
                self.hist["Hist_Energy_forwardminus" + Pythia_Process_ID].Fill(calop4.e()) 
               
                self.hist["Hist_eventXiID_Energy_forwardminus"].Fill(calop4.e())
                self.hist["Hist_eventXiID_Energy_forwardminus" + EventSelectionXiProcess_ID].Fill(calop4.e()) 

            if  (calop4.eta()) > -6.6 and (calop4.eta()) < -5.2 :
                self.hist["Hist_Energy_Castor"].Fill(calop4.e())
                self.hist["Hist_Energy_Castor" + Pythia_Process_ID].Fill(calop4.e()) 
                self.hist["Hist_eventXiID_Energy_Castor"].Fill(calop4.e())
                self.hist["Hist_eventXiID_Energy_Castor" + EventSelectionXiProcess_ID].Fill(calop4.e()) 


      
            # self.hist["hNentries"].Fill("CaloCandClass2",1)    
            
            if calop4.eta() <= rapidityGapeta:
               
                XEtot += calop4.E()
                XPxtot += calop4.Px()
                XPytot += calop4.Py()
                XPztot += calop4.Pz()
                

       
            if calop4.eta() >= rapidityGapeta:
                  
                YEtot += calop4.E()
                YPxtot += calop4.Px()
                YPytot += calop4.Py()
                YPztot += calop4.Pz()

            
        
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
            self.hist["Hist_XiX"+Pythia_Process_ID].Fill(xix)
            self.hist["Hist_XiY"+Pythia_Process_ID].Fill(xiy)
            self.hist["Hist_log10XiX"+Pythia_Process_ID].Fill(log10(xix))
            self.hist["Hist_log10XiY"+Pythia_Process_ID].Fill(log10(xiy))
            
            
            self.hist["Hist_2Dlog10XiXXiY"+Pythia_Process_ID].Fill(log10(xix),log10(xiy))
            self.hist["Hist_log10Mx"].Fill(log10(Mx))
            self.hist["Hist_log10My"].Fill(log10(My))
            self.hist["Hist_2Dlog10MxMy"].Fill(log10(Mx),log10(My))
            self.hist["Hist_log10Mx"+ Pythia_Process_ID].Fill(log10(Mx))
            self.hist["Hist_log10My"+ Pythia_Process_ID].Fill(log10(My))
            self.hist["Hist_2Dlog10MxMy"+ Pythia_Process_ID].Fill(log10(Mx),log10(My))
            self.hist["Hist_eventXiID_2Dlog10MxMy"].Fill(log10(Mx),log10(My))
            self.hist["Hist_eventXiID_2Dlog10MxMy"+ EventSelectionXiProcess_ID].Fill(log10(Mx),log10(My))
            self.hist["Hist_eventXiID_log10XiY"].Fill(log10(xiy))
            self.hist["Hist_eventXiID_log10XiX"].Fill(log10(xix))
            self.hist["Hist_eventXiID_log10XiX"+EventSelectionXiProcess_ID].Fill(log10(xix))
            self.hist["Hist_eventXiID_log10XiY"+EventSelectionXiProcess_ID].Fill(log10(xiy))
            # self.hist["hNentries"].Fill("Xi",1)
            self.hist["Hist_numberoftowerebovenoise_castor"].Fill(CASTOR_Numberoftowerebovenoise)
            self.hist["Hist_eventXiID_numberoftowerebovenoise_castor"].Fill(CASTOR_Numberoftowerebovenoise)
            self.hist["Hist_numberoftowerebovenoise_castor"+ Pythia_Process_ID].Fill(CASTOR_Numberoftowerebovenoise)
            self.hist["Hist_eventXiID_numberoftowerebovenoise_castor"+ EventSelectionXiProcess_ID].Fill(CASTOR_Numberoftowerebovenoise)
            
            self.hist["Hist_numberoftowerebovenoise_forwardplus"].Fill(HFplus_Numberoftowerebovenoise)
            self.hist["Hist_eventXiID_numberoftowerebovenoise_forwardplus"].Fill(HFplus_Numberoftowerebovenoise)
            self.hist["Hist_numberoftowerebovenoise_forwardplus"+ Pythia_Process_ID].Fill(HFplus_Numberoftowerebovenoise)
            self.hist["Hist_eventXiID_numberoftowerebovenoise_forwardplus"+ EventSelectionXiProcess_ID].Fill(HFplus_Numberoftowerebovenoise)

            self.hist["Hist_numberoftowerebovenoise_forwardminus"].Fill(HFminus_Numberoftowerebovenoise)
            self.hist["Hist_eventXiID_numberoftowerebovenoise_forwardminus"].Fill(HFminus_Numberoftowerebovenoise)
            self.hist["Hist_numberoftowerebovenoise_forwardminus"+ Pythia_Process_ID].Fill(HFminus_Numberoftowerebovenoise)
            self.hist["Hist_eventXiID_numberoftowerebovenoise_forwardminus"+ EventSelectionXiProcess_ID].Fill(HFminus_Numberoftowerebovenoise)

           
            self.hist["Hist_numberoftowerebovenoise_barrel"].Fill(Barrel_Numberoftowerebovenoise)
            self.hist["Hist_numberoftowerebovenoise_barrel"+Pythia_Process_ID].Fill(Barrel_Numberoftowerebovenoise)
            self.hist["Hist_numberoftowerebovenoise_endcap"].Fill(Endcap_Numberoftowerebovenoise)
            self.hist["Hist_numberoftowerebovenoise_endcap"+Pythia_Process_ID].Fill(Endcap_Numberoftowerebovenoise)
            self.hist["Hist_numberoftowerebovenoise_endcapforwardtransition"].Fill(endcapforwardtransition_Numberoftowerebovenoise)
            self.hist["Hist_numberoftowerebovenoise_endcapforwardtransition"+Pythia_Process_ID].Fill(endcapforwardtransition_Numberoftowerebovenoise)

            self.hist ["Hist_CaloReducedenergyClass"] .Fill(len(CaloReducedenergyClass))
            self.hist ["Hist_CaloReducedenergyClass"+ Pythia_Process_ID].Fill(len(CaloReducedenergyClass))
              

            self.OUTlog10XiDD[0] =log10(Xi_DD)
            # self.OUTlog10XiyGen[0] = log10(GenXiY)
            self.OUTlog10XixReco[0] = log10(xix)
            self.OUTlog10XiyReco[0] = log10(xiy)
            self.OUTdeltazero[0] = delta_zero
            self.OUTdeltazero[0] = deltaetamax
            self.OUTetamin[0] = mineta
            self.OUTetamax[0] = maxeta
            self.OUTrapditygapmean [0] = rapidityGapeta
            self.OUTCastorNtowers[0] = CASTOR_Numberoftowerebovenoise
            self.OUTHFminusNtowers[0] = HFminus_Numberoftowerebovenoise
            self.OUTHFplusNtowers[0] = HFplus_Numberoftowerebovenoise
            self.OUTNtracks[0] = Nbrtracks
            self.OUTPythia8processid[0] = int_Pythia_Process_ID
            self.OUTEventselectionXiprocessid[0] = int_EventSelectionXiProcess_ID
          

            Signal_ID = int_Pythia_Process_ID
            if EventSelection_with_Xi:
                Signal_ID = int_EventSelectionXiProcess_ID

            self.AllTree.Fill()
            if Signal_ID == self.get_Process_ID_from_String(Training_Signal):
                self.sigTree.Fill()
            else:
                self.bkgTree.Fill()
                


            if not self.isData:
                self.hist["Hist_2DLogRecoXiX_logGenXiX"].Fill(log10(xix),log10(GenXiX))
                self.hist["Hist_2DLogRecoXiY_logGenLogXiY"].Fill(log10(xiy),log10(GenXiY))
                # self.hist["Hist_2D_genreco_Deltapos"].Fill(ChargedGenParticleClass[deltaetamax_Gen_pos][0].eta(),TrackCandClass[deltaetamax_Reco_pos][0]) 
                self.hist["Hist_2DLogRecoXiX_logGenXiX"+Pythia_Process_ID].Fill(log10(xix),log10(GenXiX))
                self.hist["Hist_2DLogRecoXiY_logGenLogXiY"+Pythia_Process_ID].Fill(log10(xiy),log10(GenXiY))
                self.hist["Hist_2Drecogen_EnergyX"].Fill(XEtot,XGenEtot)
                self.hist["Hist_2Drecogen_EnergyY"].Fill(YEtot,YGenEtot)
                self.hist["Hist_2D_recogen_Mean"].Fill(rapidityGapeta, MeanGen)
                self.hist["Hist_Reco_log10XiDD"].Fill(log10(Xi_DD)) 
                self.hist["Hist_eventXiID_Reco_log10XiDD"].Fill(log10(Xi_DD)) 
                self.hist["Hist_Reco_log10XiDD"+ Pythia_Process_ID].Fill(log10(Xi_DD)) 
                self.hist["Hist_eventXiID_Reco_log10XiDD"+ EventSelectionXiProcess_ID].Fill(log10(Xi_DD)) 
                self.hist["Hist_2DRecoLogXi_DDGenLogXi_DD"].Fill(log10(Xi_DD),log10(GenXi_DD))
                

                # if maxeta < 1:
                #     self.hist["Hist_2D_FG1_2DLogGenXiX_LogGenXiY"].Fill(log10(GenXiX),log10(GenXiY))
                #     self.hist["Hist_2D_FG1_RecoLogXiXGenLogXiX"].Fill(log10(xix),log10(GenXiX))
                #     self.hist["Hist_2D_FG1_RecoLogXiYGenLogXiY"].Fill(log10(xiy),log10(GenXiY))
                # if mineta > -1:
                #     self.hist["Hist_2D_FG2_2DLogGenXiX_LogGenXiY"].Fill(log10(GenXiX),log10(GenXiY))
                #     self.hist["Hist_2D_FG2_RecoLogXiXGenLogXiX"].Fill(log10(xix),log10(GenXiX))
                #     self.hist["Hist_2D_FG2_RecoLogXiYGenLogXiY"].Fill(log10(xiy),log10(GenXiY))
                # if delta_zero > 3:
                #     self.hist["Hist_2D_CG_2DLogGenXiX_LogGenXiY"].Fill(log10(GenXiX),log10(GenXiY))
                #     self.hist["Hist_2D_CG_RecoLogXiXGenLogXiX"].Fill(log10(xix),log10(GenXiX))
                #     self.hist["Hist_2D_CG_RecoLogXiYGenLogXiY"].Fill(log10(xiy),log10(GenXiY))

           
               

            
              
               
    

        return 1

    def finalize(self):
        print "Finalize:"
        if hasattr(self, 'AllTree'):
            self.AllTree.AutoSave()    
        if hasattr(self, 'sigTree'):
            self.sigTree.AutoSave()
        if hasattr(self, 'bkgTree'):
            self.bkgTree.AutoSave()       
       
    
if __name__ == "__main__":
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
    ROOT.gSystem.Load("libFWCoreFWLite.so")
    ROOT.AutoLibraryLoader.enable()

    sampleList = []
    sampleList.append("MinBias_TuneMBR_13TeV-pythia8_MagnetOff_CASTORmeasured_newNoise")
    # sampleList.append("MinBias_EPOS_13TeV_MagnetOff_CASTORmeasured_newNoise")
    # sampleList.append("data_ZeroBias_27Jan2016_LHCf") #247934 #sebastians tree for HF towers
    # sampleList.append("data_ZeroBias1_CASTOR247934")
    # sampleList.append("data_ZeroBias1_CASTOR")
    maxFilesMC = None# run through all ffiles found
    maxFilesData = None # same
    nWorkers = 8# Use all cpu cores
   
   
    slaveParams = {}
    # slaveParams["maxEta"] = 2.


    # use printTTree.py <sampleName> to see what trees are avaliable inside the skim file
    DiffractiveAndTrack.runAll(treeName="EflowTree",
    # DiffractiveAndTrack.runAll(treeName="CFFTree", # if you use the sebastians tree    
           slaveParameters=slaveParams,
           sampleList=sampleList,
           maxFilesMC = maxFilesMC,
           maxFilesData = maxFilesData,
           nWorkers= nWorkers,
           maxNevents = 20000,
           verbosity = 2,
           outFile = "trackanddiffractive_sigDD_pythia8.root")# self.fChain.ZeroTeslaPixelnoPreSplittingVtx_vrtxX.size() > 0: 