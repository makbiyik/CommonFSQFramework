#!/usr/bin/env python


import CommonFSQFramework.Core.ExampleProofReader
#from rootpy.math.physics.vector import LorentzVector
import sys, os, time
sys.path.append(os.path.dirname(__file__))

import ROOT
ROOT.gROOT.SetBatch(True)
import ParticleDataTool as pd

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
        self.hist["BunchCrossing"] =  ROOT.TH1F("BunchCrossing", "BunchCrossing",  3600, 0-0.5, 3600-0.5)
        self.hist["Runs"] =  ROOT.TH1F("Runs", "Runs",  2000, 246000-0.5, 278000-0.5)
        self.hist["HFEnergy"] = ROOT.TH1F("HFEnergy","HFEnergy",100, 0, 200)
        self.hist["Hist_sum_CAS_E"] =  ROOT.TH1F("Hist_sum_CAS_E", "Hist_sum_CAS_E" ,100,0,600)
        self.hist["hParticleCounts"] = ROOT.TH1F("hParticleCounts","hParticleCounts",10, 0, 20) 
           
        nEtaBins = 8
        EtaBins = array('d',[-6.6, -5.2, -3.2, -2.6, -1.4, 1.4, 2.6, 3.2, 5.2])
    

        NbrVtxzBins = 50
        BinVtxzMin = -20
        BinVtxzMax = 20


        self.hist["Hist_NrVtx"] = ROOT.TH1F("Hist_NrVtx_","Hist_NrVtx",NbrVtxzBins,BinVtxzMin, BinVtxzMax)  

        NbrEtaBins = 50
        BinEtaMin = -6.5
        BinEtaMax = 5.5
        NbrDetaBins = 50
        BinDetaMin = 0
        BinDetaMax = 10

        self.hist["Hist_Eta_Min"] =  ROOT.TH1F("Hist_Eta_Min", "Hist_Eta_Min", NbrEtaBins, BinEtaMin, BinEtaMax)
        self.hist["Hist_Eta_Max"] =  ROOT.TH1F("Hist_Eta_Max", "Hist_Eta_Max", NbrEtaBins, BinEtaMin, BinEtaMax)
        self.hist["Hist_Eta_Delta"] =  ROOT.TH1F("Hist_Eta_Delta", "Hist_Eta_Delta", NbrDetaBins, BinDetaMin, BinDetaMax)
        self.hist["Hist_Eta_DeltaZero"] = ROOT.TH1F("Hist_Eta_DeltaZero", "Hist_Eta_DeltaZero", NbrDetaBins, BinDetaMin, BinDetaMax)
        self.hist["Hist_Eta_DeltaMax"] =  ROOT.TH1F("Hist_Eta_DeltaMax", "Hist_Eta_DeltaMax", NbrDetaBins, BinDetaMin, BinDetaMax)
        # Gen PArticle 
        self.hist["Hist_GP_Eta_Min"] =  ROOT.TH1F("Hist_GP_Eta_Min", "Hist_GP_Eta_Min", NbrEtaBins, BinEtaMin, BinEtaMax)
        self.hist["Hist_GP_Eta_Max"] =  ROOT.TH1F("Hist_GP_Eta_Max", "Hist_GP_Eta_Max", NbrEtaBins, BinEtaMin, BinEtaMax)
        self.hist["Hist_GP_Eta_Delta"] =  ROOT.TH1F("Hist_GP_Eta_Delta","Hist_GP_Eta_Delta", NbrDetaBins, BinDetaMin, BinDetaMax)
        self.hist["Hist_GP_Eta_DeltaZero"] =  ROOT.TH1F("Hist_GP_Eta_DeltaZero", "Hist_GP_Eta_DeltaZero", NbrDetaBins, BinDetaMin, BinDetaMax)
        self.hist["Hist_GP_Eta_DeltaMax"] =  ROOT.TH1F("Hist_GP_Eta_DeltaMax", "Hist_GP_Eta_DeltaMax", NbrDetaBins, BinDetaMin, BinDetaMax)
        self.hist["Hist_Deltazero_deltagenreco"] =  ROOT.TH1F("Hist_Deltazero_deltagenreco", "Hist_Deltazero_deltagenreco", NbrDetaBins, -10, BinDetaMax)
        self.hist["Hist_2D_genrecoEta_DeltaZero"] = ROOT.TH2D("Hist_2D_genrecoEta_DeltaZero","Hist_2D_genrecoEta_DeltaZero", NbrDetaBins,BinDetaMin, BinDetaMax,NbrDetaBins,BinDetaMin, BinDetaMax);
        self.hist["Hist_2D_genrecoEta_DeltaMax"] = ROOT.TH2D("Hist_2D_genrecoEta_DeltaMax","Hist_2D_genrecoEta_DeltaMax", NbrDetaBins,BinDetaMin, BinDetaMax,NbrDetaBins,BinDetaMin, BinDetaMax);


        NbrSizeBins = 50
        BinSizeEMin = 0
        BinSizeEMax = 50
        
        self.hist["Hist_TrackCandClass"] = ROOT.TH1F("Hist_TrackCandClass","Hist_TrackCandClass",NbrSizeBins, BinSizeEMin,100)

        NbrPhiBins = 50
        BinPhiMin = -5
        BinPhiMax = 5

        self.hist["Hist_trkPhi"] = ROOT.TH1F("Hist_trkPhi","Hist_trkPhi",NbrPhiBins,  BinPhiMin, BinPhiMax)  
        self.hist["Hist_Eta"] = ROOT.TH1F("Hist_Eta","Hist_Eta",NbrEtaBins, BinEtaMin, BinEtaMax)  
        self.hist["Hist_trkEta"] = ROOT.TH1F("Hist_trkEta","Hist_trkEta",NbrEtaBins, BinEtaMin, BinEtaMax)  
        self.hist["Hist_trkplusEta"] = ROOT.TH1F("Hist_trkplusEta","Hist_trkplusEta",NbrEtaBins, BinEtaMin, BinEtaMax) 
        NbrNtrackBins = 50
        BinNtrackMin = 0
        BinNtrackMax = 150
       
        NbrLogMBins = 70
        BinLogMMin = -2
        BinLogMMax = 5
        
        NbrPFEBins = 50
        BinPFEMin = 0
        BinPFEMax = 50

       

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
        self.hist["Hist_Energy_Castor"] =  ROOT.TH1F("Hist_Energy_Castor", "Hist_Energy_Castor" , NbrPFEBins, BinPFEMin, BinPFEMax)
 


        for ip in Process_ID:
            self.hist["Hist_Eta_Min"+str(ip)] = ROOT.TH1D("Hist_Eta_Min"+str(ip),"Hist_Eta_Min ", NbrEtaBins, BinEtaMin, BinEtaMax)
            self.hist["Hist_Eta_Max"+str(ip)] = ROOT.TH1D("Hist_Eta_Max"+str(ip),"Hist_Eta_Max ", NbrEtaBins, BinEtaMin, BinEtaMax) 
            self.hist["Hist_Eta_Delta"+str(ip)] = ROOT.TH1D("Hist_Eta_Delta"+str(ip),"Hist_Eta_Delta ", NbrDetaBins, BinDetaMin, BinDetaMax)
            self.hist["Hist_Eta_DeltaZero"+str(ip)] = ROOT.TH1D("Hist_Eta_DeltaZero"+str(ip),"Hist_Eta_DeltaZero ", NbrDetaBins, BinDetaMin, BinDetaMax)
            self.hist["Hist_Eta"+str(ip)] =  ROOT.TH1F("Hist_Eta"+str(ip), "Hist_Eta"+str(ip), nEtaBins, EtaBins)
            self.hist["Hist_Eta_DeltaMax"+str(ip)] =  ROOT.TH1F("Hist_Eta_DeltaMax"+str(ip), "Hist_Eta_DeltaMax"+str(ip), NbrDetaBins, BinDetaMin, BinDetaMax)               
            self.hist["Hist_Energy"+str(ip)] =  ROOT.TH1F("Hist_Energy"+str(ip), "Hist_Energy"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_Energy_barrel"+str(ip)] =  ROOT.TH1F("Hist_Energy_barrel"+str(ip), "Hist_Energy_barrel"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_Energy_endcap"+str(ip)] =  ROOT.TH1F("Hist_Energy_endcap"+str(ip), "Hist_Energy_endcap"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_Energy_endcap_forwardtransition"+str(ip)] =  ROOT.TH1F("Hist_Energy_endcap_forwardtransition"+str(ip), "Hist_Energy_endcap_forwardtransition"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_Energy_forward"+str(ip)] =  ROOT.TH1F("Hist_Energy_forward"+str(ip), "Hist_Energy_forward"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_Energy_Castor"+str(ip)] =  ROOT.TH1F("Hist_Energy_Castor"+str(ip), "Hist_Energy_Castor"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)


        
        NbrLogXiBins = 50
        BinLogXiMin = -7
        BinLogXiMax = -2

        # self.hist["Hist_log10XiSD"] =  ROOT.TH1F("Hist_log10XiSD", "Hist_log10XiSD", NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        # self.hist["Hist_log10XiDD"] =  ROOT.TH1F("Hist_log10XiDD", "Hist_log10XiDD", NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        # self.hist["Hist_log10XiX"] =  ROOT.TH1F("Hist_log10XiX", "Hist_log10XiX", NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        # self.hist["Hist_log10XiY"] =  ROOT.TH1F("Hist_log10XiY", "Hist_log10XiY", NbrLogXiBins, BinLogXiMin, BinLogXiMax)

        # self.hist["Hist_2Dlog10XiXXiY"] = ROOT.TH2D("Hist_2Dlog10XiXXiY", "Hist_2Dlog10XiXXiY", NbrLogXiBins, BinLogXiMin, BinLogXiMax, NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        # self.hist["Hist_GenLogXiXRecoLogXiX"] = ROOT.TH2D("Hist_GenLogXiXRecoLogXiX", "Hist_GenLogXiXRecoLogXiX", NbrLogXiBins, BinLogXiMin, BinLogXiMax, NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        # self.hist["Hist_GenLogXiYRecoLogXiY"] = ROOT.TH2D("Hist_GenLogXiYRecoLogXiY", "Hist_GenLogXiYRecoLogXiY", NbrLogXiBins, BinLogXiMin, BinLogXiMax, NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        









      
        for h in self.hist:
            self.hist[h].Sumw2()
            self.GetOutputList().Add(self.hist[h])

        self.pdg_helper = pd.PYTHIAParticleData()
        self.castor_tower_p4 = []
        self.CMenergy = 13000 # GeV
        for isec in xrange(0,16):
            self.castor_tower_p4.append( ROOT.ROOT.Math.LorentzVector('ROOT::Math::PxPyPzE4D<double>')(0,0,0,0) )

        

    def analyze(self):
        # return 1
        

        # if self.isData:
        #     if not self.fChain.run == 247324: return 1 

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
        ReduceGenParticleClass = []
        theta = 0
       
        # self.hist["hNentries"].Fill("hf cut",1)         
        if self.fChain.ZeroTeslaPixelnoPreSplittingVtx_vrtxX.size() > 0: 
            self.hist["Hist_NrVtx"].Fill(self.fChain.ZeroTeslaStripVtx_vrtxX.size())

        if not self.fChain.ZeroTeslaPixelnoPreSplittingVtx_vrtxX.size() == 1: return 0

        if  not self.isData:
            GenParticleClass = []
            ngenParticle = self.fChain.genParticlesp4.size()

            # self.CMenergy= self.fChain.cmenergy
           
            # final state particles from the genParticles collection
            for igenP in xrange(ngenParticle):
                genp4 = self.fChain.genParticlesp4[igenP]
                genid = self.fChain.genParticlespdg[igenP]
                genst = self.fChain.genParticlesstatus[igenP]
                
              
                if genst != 1: continue

                GenParticleClass.append([genp4,genid])

                if self.pdg_helper.charge(genid) == 0 : continue 
              
                
                ReduceGenParticleClass.append([genp4,genid])

    ##################Track##############################################################3
        TrackCandClass = []
        nTrackCand = self.fChain.ZeroTeslaPixelnoPreSplittingVtx_trktheta.size()
        for itrk in xrange(nTrackCand):
            
            theta= self.fChain.ZeroTeslaPixelnoPreSplittingVtx_trktheta[itrk]
            trkphi = self.fChain.ZeroTeslaPixelnoPreSplittingVtx_trkphi[itrk]
       
            Eta = -np.log(math.tan(theta/2))
            TrackCandClass.append([Eta,trkphi])


        mineta =-10000
        maxeta = -10000
        Deltaeta = -10000
        self.hist["Hist_TrackCandClass"].Fill(len(TrackCandClass))  

        TrackCandClass.sort(cmp=compareTracketa)
        mineta =  TrackCandClass[0][0]
        maxeta =  TrackCandClass[len(TrackCandClass)-1][0] #eta()pseduorapidty


        self.hist["Hist_Eta_Min"].Fill(mineta)
        self.hist["Hist_Eta_Max"].Fill(maxeta)
           
        Deltaeta = maxeta - mineta

        self.hist["Hist_Eta_Delta"].Fill(Deltaeta)  
        deltaeta = 1
        delta_zero = -1
        delta_zero_pos = -1
        deltaetamax = -1
        deltaetamax_pos = -1
        
        for jtrk in xrange(0,len(TrackCandClass)): #change   GenParticleClass to  TrackCandClass for testing
            tracketa  =  TrackCandClass[jtrk][0]
            # trackid  =  TrackCandClass[itrack][1]

            self.hist["Hist_trkEta"].Fill(TrackCandClass[jtrk][0])

            if jtrk < len(TrackCandClass)-1:
                # deltaeta =  TrackCandClass[itrack+1][0].eta() -  TrackCandClass[itrack][0].eta()
                deltaeta =  TrackCandClass[jtrk+1][0]-  TrackCandClass[jtrk][0] #eta()pseduorapidty
                self.hist["Hist_trkplusEta"].Fill(TrackCandClass[jtrk+1][0])
                if  (deltaeta > deltaetamax):
                    deltaetamax = deltaeta
                    deltaetamax_pos = jtrk

                if  TrackCandClass[jtrk+1][0] > 0 and  TrackCandClass[jtrk][0]< 0:
                    delta_zero = deltaeta
                    delta_zero_pos = jtrk


            
            self.hist["Hist_Eta_DeltaZero"].Fill(delta_zero)
            
        
        if not self.isData: #Rapidity -> chanded to eta again :)

            if len(ReduceGenParticleClass) == 0:
                return 0

            ReduceGenParticleClass.sort(cmp=compareGeneta)
            mineta = ReduceGenParticleClass[0][0].eta()
            maxeta = ReduceGenParticleClass[len(ReduceGenParticleClass)-1][0].eta()
            self.hist["Hist_GP_Eta_Min"].Fill(mineta)
            self.hist["Hist_GP_Eta_Max"].Fill(maxeta)
           
            Deltaeta = maxeta - mineta
            self.hist["Hist_GP_Eta_Delta"].Fill(Deltaeta)

            deltaeta=-1
            delta_zero_gen = -1
            delta_max_gen = -1
            delta_zero_pos = -1
            deltaetamax_pos = -1
            deltagenreco = -1
            for igp in xrange(len(ReduceGenParticleClass)):
                genp4  = ReduceGenParticleClass[igp][0]
                genid  = ReduceGenParticleClass[igp][1]
    

                if igp < len(ReduceGenParticleClass)-1:
                 
                    deltaeta = ReduceGenParticleClass[igp+1][0].eta() - ReduceGenParticleClass[igp][0].eta() 

                    if  (deltaeta > delta_max_gen):
                        delta_max_gen = deltaeta
                        deltaetamax_pos = igp

                    if ReduceGenParticleClass[igp+1][0].eta() > 0 and ReduceGenParticleClass[igp][0].eta() < 0:
                        delta_zero_gen = deltaeta
                        delta_zero_pos = igp

            deltagenreco = (delta_zero_gen - delta_zero)
            self.hist["Hist_GP_Eta_DeltaMax"].Fill(delta_max_gen)
            self.hist["Hist_GP_Eta_DeltaZero"].Fill(delta_zero_gen)
            self.hist["Hist_Deltazero_deltagenreco"].Fill(deltagenreco)
            self.hist["Hist_2D_genrecoEta_DeltaZero"].Fill(delta_zero_gen,delta_zero)
            self.hist["Hist_2D_genrecoEta_DeltaMax"].Fill(delta_max_gen,deltaetamax) 
            # xi_sd = self.fChain.XiSD
            # xi_dd = self.fChain.XiDD
            mx = -1
            my = -1
            xi_x = self.fChain.Xix
            xi_y= self.fChain.Xiy   
           
           
            
            if self.CMenergy>0 :    
                xisd = max(xi_x,xi_y);
                xidd = xi_x*xi_y*self.CMenergy * self.CMenergy/(0.938*0.938);

                mx2 = (xi_x * (self.CMenergy)*(self.CMenergy))
                my2 = (xi_y * (self.CMenergy) * self.CMenergy)

                if mx2<=0: mx2=1e-10
                if my2<=0: my2=1e-10

                mx = sqrt(mx2)
                my = sqrt(my2)

                # self.hist["Hist_HMC_log10Mx"].Fill(log10(mx))
                # self.hist["Hist_HMC_log10My"].Fill(log10(my))
                # self.hist["Hist_HMC_2Dlog10MxMy"].Fill(log10(mx),log10(my))


            # calculate Mx2 and My2
            XEtot =  0
            XPxtot = 0
            XPytot = 0
            XPztot = 0
            YEtot =  0
            YPxtot = 0
            YPytot = 0
            YPztot = 0
            Mx2 = 0
            My2 = 0
            for igp in xrange(0,deltaetamax_pos+1): 
                XEtot += ReduceGenParticleClass[igp][0].E()
                XPxtot += ReduceGenParticleClass[igp][0].Px()
                XPytot += ReduceGenParticleClass[igp][0].Py()
                XPztot += ReduceGenParticleClass[igp][0].Pz()
           
            Mx2 = XEtot*XEtot - XPxtot*XPxtot - XPytot*XPytot - XPztot*XPztot
               
            for igp in xrange ((deltaetamax_pos+1),len(ReduceGenParticleClass)):
                YEtot += ReduceGenParticleClass[igp][0].E()
                YPxtot += ReduceGenParticleClass[igp][0].Px()
                YPytot += ReduceGenParticleClass[igp][0].Py()
                YPztot += ReduceGenParticleClass[igp][0].Pz()

            My2 = YEtot*YEtot - YPxtot*YPxtot - YPytot*YPytot - YPztot*YPztot

            # set Mx2, My2 to zero if negative (i.e. the X,Y system is a photon)
            if Mx2<=0: Mx2=1e-20
            if My2<=0: My2=1e-20
            
            Mx = sqrt(Mx2)
            self.hist["Hist_GP_Mx"].Fill(Mx)
            self.hist["Hist_GP_log10Mx"].Fill(log10(Mx))

            My = sqrt(My2)
            self.hist["Hist_GP_My"].Fill(My)
            self.hist["Hist_GP_log10My"].Fill(log10(My))

            self.hist["Hist_GP_2Dlog10MxMy"].Fill(log10(Mx),log10(My))

            GenXiX = Mx2/self.CMenergy/self.CMenergy
            GenXiY = My2/self.CMenergy/self.CMenergy
           
      
         ####################################Calotower######################################


        TrackCaloCandClass = []
        CaloTower = self.fChain.CaloTowersp4.size()
        for icalo in xrange(0,CaloTower):
            calop4 = self.fChain.CaloTowersp4[icalo]
            caloem = self.fChain.CaloTowersemEnergy[icalo]
            calohad = self.fChain.CaloTowershadEnergy[icalo]
            
            if abs(calop4.eta()) < 1.4:
                if (calop4.e()) < 1.40: continue
                   
            if abs( calop4.eta()) > 1.4 and abs( calop4.eta()) < 2.6:
                if (calop4.e()) < 1.80: continue
                   
            if abs( calop4.eta()) > 2.6 and abs( calop4.eta()) < 3.2: 
                if (calop4.e()) < 2.40: continue
                   
            if abs(calop4.eta()) > 3.2 and abs(calop4.eta()) < 5.2 :
                if (calop4.e()) < 1.8: continue
 


            TrackCaloCandClass.append([calop4,caloem,calohad])
           
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


        miny= 0
        maxy= 0
        DeltaY =0 
        deltaeta = 0
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

            if (energy) < 3.6: continue       #Threshold for castor: 5.600000

            TrackCaloCandClass.append([self.castor_tower_p4[isec],
                                self.castor_id[isec],
                                self.sum_CAS_E_em[isec],
                                self.sum_CAS_E_had[isec]])
           

       

       

        
        if len(TrackCaloCandClass) == 0:
            return 0

       

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
         
            self.hist["Hist_Eta_Min" + Process_ID_Ext].Fill(miny)
            self.hist["Hist_Eta_Max" + Process_ID_Ext].Fill(maxy)  
            self.hist["Hist_Eta_Delta" + Process_ID_Ext].Fill(DeltaY)  

        delta_zero_pos = -1
        delta_zero = -1
        deltaetamax = -1
        deltaetamax_pos = -1
     
       
        for icalo in xrange(0,len(TrackCaloCandClass)):
            calop4  = TrackCaloCandClass[icalo][0]
            caloem  = TrackCaloCandClass[icalo][1]
            calohad  = TrackCaloCandClass[icalo][2]
           
            
            self.hist["Hist_Eta"].Fill(calop4.eta()) 
            self.hist["Hist_Energy"].Fill(calop4.e())     

            self.hist["Hist_Eta" + Process_ID_Ext].Fill(calop4.eta())     
            self.hist["Hist_Energy" + Process_ID_Ext].Fill(calop4.e())     
           
            self.hist["hParticleCounts"].Fill("all",1)
           
            

            if abs( calop4.eta() ) < 1.4:
                self.hist["Hist_Energy_barrel"].Fill(calop4.e()) 
                self.hist["Hist_Energy_barrel" + Process_ID_Ext].Fill(calop4.e()) 
               


            if  abs( calop4.eta() ) > 1.4 and abs( calop4.eta() ) < 2.6:
                self.hist["Hist_Energy_endcap"].Fill(calop4.e()) 
                self.hist["Hist_Energy_endcap" + Process_ID_Ext].Fill(calop4.e()) 
               
                                       
           
            if  abs( calop4.eta() ) > 2.6 and abs( calop4.eta() ) < 3.2:
                self.hist["Hist_Energy_endcap_forwardtransition"].Fill(calop4.e()) 
                self.hist["Hist_Energy_endcap_forwardtransition" + Process_ID_Ext].Fill(calop4.e()) 
               
                            

            if  abs (calop4.eta()) > 3.2 and abs(calop4.eta()) < 5.2:
                self.hist["Hist_Energy_forward"].Fill(calop4.e())
                self.hist["Hist_Energy_forward" + Process_ID_Ext].Fill(calop4.e()) 
               
                    
            if  (calop4.eta()) > -6.6 and (calop4.eta()) < -5.2 :
                self.hist["Hist_Energy_Castor"].Fill(calop4.e())
                self.hist["Hist_Energy_Castor" + Process_ID_Ext].Fill(calop4.e()) 
                
            
            if icalo != len(TrackCaloCandClass)-1:
                deltaeta = TrackCaloCandClass[icalo+1][0].eta() - TrackCaloCandClass[icalo][0].eta()

                if  (deltaeta > deltaetamax):


                    deltaetamax = deltaeta
                    deltaetamax_pos = icalo

                if TrackCaloCandClass[icalo+1][0].eta() > 0 and TrackCaloCandClass[icalo][0].eta() < 0:
                    delta_zero = deltaeta
                    delta_zero_pos = icalo
                    # self.hist["hNentries"].Fill("find #Delta#eta^{0}",1)

 
        self.hist["Hist_Eta_DeltaMax"].Fill(deltaetamax)
        self.hist["Hist_Eta_DeltaMax"+ Process_ID_Ext].Fill(deltaetamax)
        self.hist["Hist_Eta_DeltaZero"+ Process_ID_Ext].Fill(delta_zero)


        # # calculate Mx2 and My2
        # XEtot =  0
        # XPxtot = 0
        # XPytot = 0
        # XPztot = 0
        # YEtot =  0
        # YPxtot = 0
        # YPytot = 0
        # YPztot = 0
        # xix = 0 
        # xiy = 0 
        # Mx2 = 0
        # My2 = 0
       
        # for icalo in xrange(0, deltaetamax_pos+1):  
        #     XEtot += TrackCaloCandClass[icalo][0].E()
        #     XPxtot += TrackCaloCandClass[icalo][0].Px()
        #     XPytot += TrackCaloCandClass[icalo][0].Py()
        #     XPztot += TrackCaloCandClass[icalo][0].Pz()

        # Mx2 = XEtot*XEtot - XPxtot*XPxtot - XPytot*XPytot - XPztot*XPztot
       
        # for icalo in xrange (deltaetamax_pos+1,len(TrackCaloCandClass)):
        #     YEtot += TrackCaloCandClass[icalo][0].E()
        #     YPxtot += TrackCaloCandClass[icalo][0].Px()
        #     YPytot += TrackCaloCandClass[icalo][0].Py()
        #     YPztot += TrackCaloCandClass[icalo][0].Pz()

        # My2 = YEtot*YEtot - YPxtot*YPxtot - YPytot*YPytot - YPztot*YPztot


        # # set Mx2, My2 to zero if negative (i.e. the X,Y system is a photon)            
        # if Mx2<=0: Mx2=1e-20
        # if My2<=0: My2=1e-20

        # Mx = sqrt(Mx2)
        # My = sqrt(My2)
            
            
        
        # if self.CMenergy > 0 :    
        # # // calculate xix and xiy
        #     xix = Mx*Mx/self.CMenergy/self.CMenergy
        #     xiy = My*My/self.CMenergy/self.CMenergy
           
        #     xisd = max(xix,xiy);
        #     xidd = xix*xiy*self.CMenergy * self.CMenergy/(0.938*0.938);
               
        #     self.hist["Hist_XiX"].Fill(xix)
        #     self.hist["Hist_XiY"].Fill(xiy)
        #     self.hist["Hist_XiSD"].Fill(xisd)
        #     self.hist["Hist_XiDD"].Fill(xidd)

        #     self.hist["Hist_log10XiX"].Fill(log10(xix))
        #     self.hist["Hist_log10XiY"].Fill(log10(xiy))
        #     self.hist["Hist_log10XiSD"].Fill(log10(xisd))
        #     self.hist["Hist_log10XiDD"].Fill(log10(xidd))

        #     self.hist["Hist_2Dlog10XiXXiY"].Fill(log10(xix),log10(xiy))

        #     self.hist["Hist_XiX"+Process_ID_Ext].Fill(xix)
        #     self.hist["Hist_XiY"+Process_ID_Ext].Fill(xiy)
        #     self.hist["Hist_XiSD"+Process_ID_Ext].Fill(xisd)
        #     self.hist["Hist_XiDD"+Process_ID_Ext].Fill(xidd)

        #     self.hist["Hist_log10XiX"+Process_ID_Ext].Fill(log10(xix))
        #     self.hist["Hist_log10XiY"+Process_ID_Ext].Fill(log10(xiy))
        #     self.hist["Hist_log10XiSD"+Process_ID_Ext].Fill(log10(xisd))
        #     self.hist["Hist_log10XiDD"+Process_ID_Ext].Fill(log10(xidd))

        #     self.hist["Hist_2Dlog10XiXXiY"+Process_ID_Ext].Fill(log10(xix),log10(xiy))

        #     self.hist["Hist_log10Mx"].Fill(log10(Mx))
        #     self.hist["Hist_log10My"].Fill(log10(My))
        #     self.hist["Hist_2Dlog10MxMy"].Fill(log10(Mx),log10(My))

        #     self.hist["Hist_log10Mx"+ Process_ID_Ext].Fill(log10(Mx))
        #     self.hist["Hist_log10My"+ Process_ID_Ext].Fill(log10(My))
        #     self.hist["Hist_2Dlog10MxMy"+ Process_ID_Ext].Fill(log10(Mx),log10(My))

        #     if not self.isData:
        #         self.hist["Hist_GenLogXiXRecoLogXiX"].Fill(log10(xix),log10(GenXiX))
        #         self.hist["Hist_GenLogXiYRecoLogXiY"].Fill(log10(xiy),log10(GenXiY))
        #         self.hist["Hist_GenLogXiXRecoLogXiX"+Process_ID_Ext].Fill(log10(xix),log10(GenXiX))
        #         self.hist["Hist_GenLogXiYRecoLogXiY"+Process_ID_Ext].Fill(log10(xiy),log10(GenXiY))







        return 1

    def finalize(self):
        print "Finalize:"
        # normFactor = self.getNormalizationFactor()
        # print "  applying norm", normFactor
        # for h in self.hist:
        #     self.hist[h].Scale(normFactor)

if __name__ == "__main__":
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
    ROOT.gSystem.Load("libFWCoreFWLite.so")
    ROOT.AutoLibraryLoader.enable()

    sampleList = []
    sampleList.append("data_ZeroBias1_CASTOR")
    sampleList.append("MinBias_CUETP8M1_13TeV-pythia8_MagnetOff_CASTOR")
    maxFilesMC = 1# run through all ffiles found
    maxFilesData = 1# same
    nWorkers = 8# Use all cpu cores
    


    slaveParams = {}
    # slaveParams["maxEta"] = 2.


    # use printTTree.py <sampleName> to see what trees are avaliable inside the skim file
    DiffractiveAndTrack.runAll(treeName="EflowTree",
           slaveParameters=slaveParams,
           sampleList=sampleList,
           maxFilesMC = maxFilesMC,
           maxFilesData = maxFilesData,
           nWorkers=nWorkers,
           # maxNevents = 2000,
           verbosity = 2,
           outFile = "trackanddiffractive.root" )
