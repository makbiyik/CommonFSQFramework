#!/usr/bin/env python


import CommonFSQFramework.Core.ExampleProofReader
#from rootpy.math.physics.vector import LorentzVector
import sys, os, time
sys.path.append(os.path.dirname(__file__))

import ROOT
ROOT.gROOT.SetBatch(True)
from ROOT import edm

from array import *
from math import cosh
from math import sinh
from math import sin
from math import cos
from math import log10
from math import pi
from math import sqrt
from BadChannels2015 import badChannelsSecMod

def comparePFeta(first,second):
    if first[0].eta() > second[0].eta(): return 1
    if first[0].eta() == second[0].eta(): return 0
    if first[0].eta() < second[0].eta(): return -1

def comparePFrapidiy(first,second):
    if first[0].Rapidity() > second[0].Rapidity(): return 1
    if first[0].Rapidity() == second[0].Rapidity(): return 0
    if first[0].Rapidity() < second[0].Rapidity(): return -1

class Diffractive(CommonFSQFramework.Core.ExampleProofReader.ExampleProofReader):
    def init(self,maxEvents = None):
        
        self.maxEvents = maxEvents

        self.CMenergy = 13000 # GeV


        self.hist = {}
        self.hist["hNentries"] = ROOT.TH1F("hNentries","hNentries",10, 0, 20)
        self.hist["hParticleCounts"] = ROOT.TH1F("hParticleCounts","hParticleCounts",10, 0, 20)
       
        self.hist["BunchCrossing"] =  ROOT.TH1F("BunchCrossing", "BunchCrossing",  3600, 0-0.5, 3600-0.5)
        self.hist["Runs"] =  ROOT.TH1F("Runs", "Runs",  2000, 246000-0.5, 278000-0.5)
        self.hist["numGenTracks"] =  ROOT.TH1F("numGenTracks", "numGenTracks",  100, -0.5, 99.5)
        self.hist["Hist_PFCandidatesId"] =  ROOT.TH1F("Hist_PFCandidatesId", "Hist_PFCandidatesId",  100, 0-0.5, 100-0.5)
        

        nEtaBins = 8
        EtaBins = array('d',[-6.6, -5.2, -3.2, -2.6, -1.4, 1.4, 2.6, 3.2, 5.2])

        NbrEtaBins = 50
        BinEtaMin = -6.5
        BinEtaMax = 5.5
        
        NbrDetaBins = 50
        BinDetaMin = 0
        BinDetaMax = 10

        self.hist["Hist_Y"] =  ROOT.TH1F("Hist_Y", "Hist_Y", nEtaBins, EtaBins)
        self.hist["Hist_Y_Min"] =  ROOT.TH1F("Hist_Y_Min", "Hist_Y_Min", NbrEtaBins, BinEtaMin, BinEtaMax)
        self.hist["Hist_Y_Max"] =  ROOT.TH1F("Hist_Y_Max", "Hist_Y_Max", NbrEtaBins, BinEtaMin, BinEtaMax)
        self.hist["Hist_Y_Delta"] =  ROOT.TH1F("Hist_Y_Delta", "Hist_Y_Delta", NbrDetaBins, BinDetaMin, BinDetaMax)
        self.hist["Hist_Y_DeltaZero"] = ROOT.TH1F("Hist_Y_DeltaZero", "Hist_Y_DeltaZero", NbrDetaBins, BinDetaMin, BinDetaMax)

        NbrLogMBins = 70
        BinLogMMin = -2
        BinLogMMax = 5

        self.hist["Hist_log10Mx"] =  ROOT.TH1F("Hist_log10Mx", "Hist_log10Mx", NbrLogMBins, BinLogMMin, BinLogMMax)
        self.hist["Hist_log10My"] =  ROOT.TH1F("Hist_log10My", "Hist_log10My", NbrLogMBins, BinLogMMin, BinLogMMax)  
        self.hist["Hist_2Dlog10MxMy"] =  ROOT.TH2D("Hist_2Dlog10MxMy", "Hist_2Dlog10MxMy", NbrLogMBins, BinLogMMin, BinLogMMax, NbrLogMBins, BinLogMMin, BinLogMMax)
        self.hist["Hist_Y_DeltaMax"] =  ROOT.TH1F("Hist_Y_DeltaMax", "Hist_Y_DeltaMax", NbrDetaBins, BinDetaMin, BinDetaMax)

        NbrXiBins = 50
        BinXiMin = 0
        BinXiMax = 5

        self.hist["Hist_XiSD"] =  ROOT.TH1F("Hist_XiSD", "Hist_XiSD", NbrXiBins, BinXiMin, BinXiMax)
        self.hist["Hist_XiDD"] =  ROOT.TH1F("Hist_XiDD", "Hist_XiDD", NbrXiBins, BinXiMin, BinXiMax)
        self.hist["Hist_XiX"] =  ROOT.TH1F("Hist_XiX", "Hist_XiX", NbrXiBins, BinXiMin, BinXiMax)
        self.hist["Hist_XiY"] =  ROOT.TH1F("Hist_XiY", "Hist_XiY", NbrXiBins, BinXiMin, BinXiMax)

        NbrLogXiBins = 50
        BinLogXiMin = -7
        BinLogXiMax = -2

        self.hist["Hist_log10XiSD"] =  ROOT.TH1F("Hist_log10XiSD", "Hist_log10XiSD", NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        self.hist["Hist_log10XiDD"] =  ROOT.TH1F("Hist_log10XiDD", "Hist_log10XiDD", NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        self.hist["Hist_log10XiX"] =  ROOT.TH1F("Hist_log10XiX", "Hist_log10XiX", NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        self.hist["Hist_log10XiY"] =  ROOT.TH1F("Hist_log10XiY", "Hist_log10XiY", NbrLogXiBins, BinLogXiMin, BinLogXiMax)

        self.hist["Hist_2Dlog10XiXXiY"] = ROOT.TH2D("Hist_2Dlog10XiXXiY", "Hist_2Dlog10XiXXiY", NbrLogXiBins, BinLogXiMin, BinLogXiMax, NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        self.hist["Hist_GenLogXiXRecoLogXiX"] = ROOT.TH2D("Hist_GenLogXiXRecoLogXiX", "Hist_GenLogXiXRecoLogXiX", NbrLogXiBins, BinLogXiMin, BinLogXiMax, NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        self.hist["Hist_GenLogXiYRecoLogXiY"] = ROOT.TH2D("Hist_GenLogXiYRecoLogXiY", "Hist_GenLogXiYRecoLogXiY", NbrLogXiBins, BinLogXiMin, BinLogXiMax, NbrLogXiBins, BinLogXiMin, BinLogXiMax)
        
        NbrPFEBins = 50
        BinPFEMin = 0
        BinPFEMax = 50

        self.hist["Hist_sum_CAS_E"] =  ROOT.TH1F("Hist_sum_CAS_E", "Hist_sum_CAS_E" ,100,0,600)

        self.hist["Hist_PF"] =  ROOT.TH1F("Hist_PF", "Hist_PF" , NbrPFEBins, BinPFEMin, BinPFEMax)
        self.hist["Hist_PF_barrel"] =  ROOT.TH1F("Hist_PF_barrel", "Hist_PF_barrel" , NbrPFEBins, BinPFEMin, BinPFEMax)
        self.hist["Hist_PF_endcap"] =  ROOT.TH1F("Hist_PF_endcap", "Hist_PF_endcap" , NbrPFEBins, BinPFEMin, BinPFEMax)
        self.hist["Hist_PF_endcap_forwardtransition"] =  ROOT.TH1F("Hist_PF_endcap_forwardtransition", "Hist_PF_endcap_forwardtransition" , NbrPFEBins, BinPFEMin, BinPFEMax)
        self.hist["Hist_PF_forward"] =  ROOT.TH1F("Hist_PF_forward", "Hist_PF_forward" , NbrPFEBins, BinPFEMin, BinPFEMax)
        self.hist["Hist_PF_Castor"] =  ROOT.TH1F("Hist_PF_Castor", "Hist_PF_Castor" , NbrPFEBins, BinPFEMin, BinPFEMax)

        Particle_ID = ["_NONE","_ch","_e","_m","_gamma", "_nh","_ch_HF", "_e_HF","_ch_Castor","_e_Castor"]
        for pdg in Particle_ID:
            self.hist["Hist_PF_barrel"+str(pdg)] =  ROOT.TH1F("Hist_PF_barrel"+str(pdg), "Hist_PF_barrel"+str(pdg) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_PF_endcap"+str(pdg)] =  ROOT.TH1F("Hist_PF_endcap"+str(pdg), "Hist_PF_endcap"+str(pdg) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_PF_endcap_forwardtransition"+str(pdg)] =  ROOT.TH1F("Hist_PF_endcap_forwardtransition"+str(pdg), "Hist_PF_endcap_forwardtransition"+str(pdg) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_PF_forward"+str(pdg)] =  ROOT.TH1F("Hist_PF_forward"+str(pdg), "Hist_PF_forward"+str(pdg) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_PF_Castor"+str(pdg)] =  ROOT.TH1F("Hist_PF_Castor"+str(pdg), "Hist_PF_Castor"+str(pdg) , NbrPFEBins, BinPFEMin, BinPFEMax)

        Process_ID = ["_NONE","_ND","_SD1","_SD2","_DD", "_CD"]
  
        self.hist["Hist_GP_Mx"] =  ROOT.TH1F("Hist_GP_Mx", "Hist_GP_Mx", NbrLogMBins, BinLogMMin, BinLogMMax)
        self.hist["Hist_GP_My"] =  ROOT.TH1F("Hist_GP_My", "Hist_GP_My", NbrLogMBins, BinLogMMin, BinLogMMax)  
        self.hist["Hist_GP_log10Mx"] =  ROOT.TH1F("Hist_GP_log10Mx", "Hist_GP_log10Mx", NbrLogMBins, BinLogMMin, BinLogMMax)
        self.hist["Hist_GP_log10My"] =  ROOT.TH1F("Hist_GP_log10My", "Hist_GP_log10My", NbrLogMBins, BinLogMMin, BinLogMMax)  
        self.hist["Hist_GP_2Dlog10MxMy"] =  ROOT.TH2D("Hist_GP_2Dlog10MxMy", "Hist_GP_2Dlog10MxMy", NbrLogMBins, BinLogMMin, BinLogMMax, NbrLogMBins, BinLogMMin, BinLogMMax)

        self.hist["Hist_HMC_log10Mx"] =  ROOT.TH1F("Hist_HMC_log10Mx", "Hist_HMC_log10Mx",  NbrLogMBins, BinLogMMin, BinLogMMax)
        self.hist["Hist_HMC_log10My"] =  ROOT.TH1F("Hist_HMC_log10My", "Hist_HMC_log10My",  NbrLogMBins, BinLogMMin, BinLogMMax)  
        self.hist["Hist_HMC_2Dlog10MxMy"] =  ROOT.TH2D("Hist_HMC_2Dlog10MxMy", "Hist_HMC_2Dlog10MxMy", NbrLogMBins, BinLogMMin, BinLogMMax, NbrLogMBins, BinLogMMin, BinLogMMax)

        self.hist["Hist_Y_GP_Min"] =  ROOT.TH1F("Hist_Y_GP_Min", "Hist_Y_GP_Min", NbrEtaBins, BinEtaMin, BinEtaMax)
        self.hist["Hist_Y_GP_Max"] =  ROOT.TH1F("Hist_Y_GP_Max", "Hist_Y_GP_Max", NbrEtaBins, BinEtaMin, BinEtaMax)

        self.hist["Hist_GP_Y_Delta"] =  ROOT.TH1F("Hist_GP_Y_Delta", "Hist_GP_Y_Delta", NbrDetaBins, BinDetaMin, BinDetaMax)
        self.hist["Hist_GP_eta_Min"] =  ROOT.TH1F("Hist_GP_eta_Min", "Hist_GP_eta_Min", NbrEtaBins, BinEtaMin, BinEtaMax)
        self.hist["Hist_GP_eta_Max"] =  ROOT.TH1F("Hist_GP_eta_Max", "Hist_GP_eta_Max", NbrEtaBins, BinEtaMin, BinEtaMax)
        self.hist["Hist_GP_eta_Delta"] =  ROOT.TH1F("Hist_GP_eta_Delta","Hist_GP_eta_Delta", NbrDetaBins, BinDetaMin, BinDetaMax)

        self.hist["Hist_GP_Y_DeltaMax"] =  ROOT.TH1F("Hist_GP_Y_DeltaMax", "Hist_GP_Y_DeltaMax", NbrDetaBins, BinDetaMin, BinDetaMax)
        self.hist["Hist_GP_Y_DeltaZero"] =  ROOT.TH1F("Hist_GP_Y_DeltaZero", "Hist_GP_Y_DeltaZero", NbrDetaBins, BinDetaMin, BinDetaMax)

        for ip in Process_ID:
            self.hist["Hist_Y_Min"+str(ip)] = ROOT.TH1D("Hist_Y_Min"+str(ip),"Hist_Y_Min ", NbrEtaBins, BinEtaMin, BinEtaMax)
            self.hist["Hist_Y_Max"+str(ip)] = ROOT.TH1D("Hist_Y_Max"+str(ip),"Hist_Y_Max ", NbrEtaBins, BinEtaMin, BinEtaMax) 
            self.hist["Hist_Y_Delta"+str(ip)] = ROOT.TH1D("Hist_Y_Delta"+str(ip),"Hist_Y_Delta ", NbrDetaBins, BinDetaMin, BinDetaMax)
            self.hist["Hist_Y_DeltaZero"+str(ip)] = ROOT.TH1D("Hist_Y_DeltaZero"+str(ip),"Hist_Y_DeltaZero ", NbrDetaBins, BinDetaMin, BinDetaMax)
           
            self.hist["Hist_2Dlog10MxMy"+str(ip)] =  ROOT.TH2D("Hist_2Dlog10MxMy"+str(ip), "Hist_2Dlog10MxMy"+str(ip), NbrLogMBins, BinLogMMin, BinLogMMax, NbrLogMBins, BinLogMMin, BinLogMMax)
            self.hist["Hist_log10Mx"+str(ip)] =  ROOT.TH1D("Hist_log10Mx"+str(ip), "Hist_log10Mx"+str(ip), NbrLogMBins, BinLogMMin, BinLogMMax)
            self.hist["Hist_log10My"+str(ip)] =  ROOT.TH1D("Hist_log10My"+str(ip), "Hist_log10My"+str(ip), NbrLogMBins, BinLogMMin, BinLogMMax)

            self.hist["Hist_XiSD"+str(ip)] =  ROOT.TH1F("Hist_XiSD"+str(ip), "Hist_XiSD"+str(ip), NbrXiBins, BinXiMin, BinXiMax)
            self.hist["Hist_XiDD"+str(ip)] =  ROOT.TH1F("Hist_XiDD"+str(ip), "Hist_XiDD"+str(ip), NbrXiBins, BinXiMin, BinXiMax)
            self.hist["Hist_XiX"+str(ip)] =  ROOT.TH1F("Hist_XiX"+str(ip), "Hist_XiX"+str(ip), NbrXiBins, BinXiMin, BinXiMax)
            self.hist["Hist_XiY"+str(ip)] =  ROOT.TH1F("Hist_XiY"+str(ip), "Hist_XiY"+str(ip), NbrXiBins, BinXiMin, BinXiMax)

            self.hist["Hist_log10XiSD"+str(ip)] =  ROOT.TH1F("Hist_log10XiSD"+str(ip), "Hist_log10XiSD"+str(ip), NbrLogXiBins, BinLogXiMin, BinLogXiMax)
            self.hist["Hist_log10XiDD"+str(ip)] =  ROOT.TH1F("Hist_log10XiDD"+str(ip), "Hist_log10XiDD"+str(ip), NbrLogXiBins, BinLogXiMin, BinLogXiMax)
            self.hist["Hist_log10XiX"+str(ip)] =  ROOT.TH1F("Hist_log10XiX"+str(ip), "Hist_log10XiX"+str(ip), NbrLogXiBins, BinLogXiMin, BinLogXiMax)
            self.hist["Hist_log10XiY"+str(ip)] =  ROOT.TH1F("Hist_log10XiY"+str(ip), "Hist_log10XiY"+str(ip), NbrLogXiBins, BinLogXiMin, BinLogXiMax)

            self.hist["Hist_2Dlog10XiXXiY"+str(ip)] = ROOT.TH2D("Hist_2Dlog10XiXXiY"+str(ip), "Hist_2Dlog10XiXXiY"+str(ip), NbrLogXiBins, BinLogXiMin, BinLogXiMax, NbrLogXiBins, BinLogXiMin, BinLogXiMax)
            self.hist["Hist_GenLogXiXRecoLogXiX"+str(ip)] = ROOT.TH2D("Hist_GenLogXiXRecoLogXiX"+str(ip), "Hist_GenLogXiXRecoLogXiX"+str(ip), NbrLogXiBins, BinLogXiMin, BinLogXiMax, NbrLogXiBins, BinLogXiMin, BinLogXiMax)
            self.hist["Hist_GenLogXiYRecoLogXiY"+str(ip)] = ROOT.TH2D("Hist_GenLogXiYRecoLogXiY"+str(ip), "Hist_GenLogXiYRecoLogXiY"+str(ip), NbrLogXiBins, BinLogXiMin, BinLogXiMax, NbrLogXiBins, BinLogXiMin, BinLogXiMax)

            self.hist["Hist_PF"+str(ip)] =  ROOT.TH1F("Hist_PF"+str(ip), "Hist_PF"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_PF_barrel"+str(ip)] =  ROOT.TH1F("Hist_PF_barrel"+str(ip), "Hist_PF_barrel"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_PF_endcap"+str(ip)] =  ROOT.TH1F("Hist_PF_endcap"+str(ip), "Hist_PF_endcap"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_PF_endcap_forwardtransition"+str(ip)] =  ROOT.TH1F("Hist_PF_endcap_forwardtransition"+str(ip), "Hist_PF_endcap_forwardtransition"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_PF_forward"+str(ip)] =  ROOT.TH1F("Hist_PF_forward"+str(ip), "Hist_PF_forward"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)
            self.hist["Hist_PF_Castor"+str(ip)] =  ROOT.TH1F("Hist_PF_Castor"+str(ip), "Hist_PF_Castor"+str(ip) , NbrPFEBins, BinPFEMin, BinPFEMax)

            self.hist["Hist_Y"+str(ip)] =  ROOT.TH1F("Hist_Y"+str(ip), "Hist_Y"+str(ip), nEtaBins, EtaBins)
            self.hist["Hist_Y_DeltaMax"+str(ip)] =  ROOT.TH1F("Hist_Y_DeltaMax"+str(ip), "Hist_Y_DeltaMax"+str(ip), NbrDetaBins, BinDetaMin, BinDetaMax)               

            for pdg in Particle_ID:
                t = ip + pdg
                self.hist["Hist_PF_barrel"+str(t)] =  ROOT.TH1F("Hist_PF_barrel"+str(t), "Hist_PF_barrel"+str(t) , NbrPFEBins, BinPFEMin, BinPFEMax)
                self.hist["Hist_PF_endcap"+str(t)] =  ROOT.TH1F("Hist_PF_endcap"+str(t), "Hist_PF_endcap"+str(t) , NbrPFEBins, BinPFEMin, BinPFEMax)
                self.hist["Hist_PF_endcap_forwardtransition"+str(t)] =  ROOT.TH1F("Hist_PF_endcap_forwardtransition"+str(t), "Hist_PF_endcap_forwardtransition"+str(t) , NbrPFEBins, BinPFEMin, BinPFEMax)
                self.hist["Hist_PF_forward"+str(t)] =  ROOT.TH1F("Hist_PF_forward"+str(t), "Hist_PF_forward"+str(t) , NbrPFEBins, BinPFEMin, BinPFEMax)
                self.hist["Hist_PF_Castor"+str(t)] =  ROOT.TH1F("Hist_PF_Castor"+str(t), "Hist_PF_Castor"+str(t) , NbrPFEBins, BinPFEMin, BinPFEMax)


        for h in self.hist:
            self.hist[h].Sumw2()
            self.GetOutputList().Add(self.hist[h])
        
        self.castor_tower_p4 = []
        for isec in xrange(0,16):
            self.castor_tower_p4.append( ROOT.ROOT.Math.LorentzVector('ROOT::Math::PxPyPzE4D<double>')(0,0,0,0) )

     # /// particle types
            # enum ParticleType {
            #   X=0,     // undefined
            #   h,       // charged hadron
            #   e,       //_e 
            #   mu,      // muon 
            #   gamma,   // photon
            #   h0,      // neutral hadron
            #   h_HF,        // HF tower identified as a hadron
            #   e_HF    // HF tower identified as an EM particle 
            #   h_CASTOR
            #   e_CASTOR

    def analyze(self):
        # return 1
        # not self.fChain.run == 247324 247920
      
        
        
        if self.isData:
            if not self.fChain.run == 247920: return 1 
       
        weight = 1
        num = 0
        self.hist["hNentries"].Fill("all",1)
        self.hist["BunchCrossing"].Fill(self.fChain.bx)
        self.hist["Runs"].Fill(self.fChain.run)
         

        # genTracks
        #num = self.fChain.genTracks.size()
        #print num
        #print self.maxEta # see slaveParams below
        #self.hist["numGenTracks"].Fill(1)
        PFCandL4 = []
        PFCandID = []
        PFCandem = []
        PFCandhad = []

        
        GenParticleClass = []
        ReduceGenParticleClass = []
        if  not self.isData:
            GenParticleClass = []
            ngenParticle = self.fChain.genParticlesp4.size()

            # self.CMenergy= self.fChain.cmenergy
           
            # final state particles from the genParticles collection
            for igenP in xrange(0,ngenParticle):
                genp4 = self.fChain.genParticlesp4[igenP]
                genid = self.fChain.genParticlespdg[igenP]
                genst = self.fChain.genParticlesstatus[igenP]
                
                # if genp4.px() == 0.0 and genp4.py() == 0.0 and abs(genp4.pz()) > 0.0 and genid == 2212: continue
                if genst != 1: continue

                GenParticleClass.append([genp4,genid])
            
                if genp4.eta() < -6.6 or genp4.eta() > 5: continue
                if genp4.E() < 5: continue

                ReduceGenParticleClass.append([genp4,genid])


        # create array of PF candidates LorentzVectors + Castor
       
        PFCandClass = []
        
        # assumtion is self.fChain.PFCandidatesparticleId.size() == self.fChain.PFCandidatesp4.size()
        nPFCand = self.fChain.PFCandidatesp4.size()
        for ipfc in xrange(0,nPFCand+1):
            if ipfc < nPFCand:
                pfp4 = self.fChain.PFCandidatesp4[ipfc]
                pfid = self.fChain.PFCandidatesparticleId[ipfc]
                pfem = self.fChain.PFCandidatesrawEcalEnergy[ipfc]
                pfhad = self.fChain.PFCandidatesrawHcalEnergy[ipfc]
                   
                # Threshold for barrel  < 1.4: 3.400000
                # Threshold for endcap 1.4 < #eta< 2.6 : 5.600000
                # Threshold for endcapforwardtransition 2.6 < #eta< 3.2: 5.600000
                # Threshold for forward n > 3.2: 4.000000
                # Threshold for castor: 5.600000

                #Threshold for barrel: 3.400000
                #Threshold for endcap: 5.400000
                #Threshold for endcapforwardtransition: 8.000000
                #Threshold for forward: 6.600000Threshold for castor: 1.000000

                if abs( pfp4.eta() ) < 1.4:
                    if (pfp4.e()) < 3.40: continue

                if abs( pfp4.eta() ) > 1.4 and abs( pfp4.eta() ) < 2.6:
                    if (pfp4.e()) < 5.40: continue   

                if abs( pfp4.eta() ) > 2.6 and abs( pfp4.eta() ) < 3.2: 
                   if (pfp4.e()) < 8.0: continue  

                if  abs (pfp4.eta()) > 3.2 and abs( pfp4.eta() ) < 5.2:
                    if (pfp4.e()) < 6.60: continue 

                PFCandClass.append([pfp4,pfid,pfem,pfhad])
                 


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
        deltay = 0
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

            if (energy) < 5.6: continue       #Threshold for castor: 5.600000

            # PFCandL4.append(self.castor_tower_p4[isec])
            # PFCandID.append(self.castor_id[isec])
            # PFCandem.append(self.sum_CAS_E_em[isec])
            # PFCandhad.append(self.sum_CAS_E_had[isec])

            PFCandClass.append([self.castor_tower_p4[isec],
                                self.castor_id[isec],
                                self.sum_CAS_E_em[isec],
                                self.sum_CAS_E_had[isec]])
       
        
        
        # if  not self.isData: #Eta

        #     # if len(ReduceGenParticleClass)== 0:
        #     #     return 0
        #     # ReduceGenParticleClass.sort(cmp=comparePFrapidiy)
        #     # miny = ReduceGenParticleClass[0][0].eta()
        #     # maxy = ReduceGenParticleClass[len(ReduceGenParticleClass)-1][0].eta()
            
        #     if len(GenParticleClass)== 0:
        #         return 0
        #     GenParticleClass.sort(cmp=comparePFeta)
        #     miny = GenParticleClass[0][0].eta()
        #     maxy = GenParticleClass[len(GenParticleClass)-1][0].eta() #eta()pseduorapidty
            


        #     self.hist["Hist_GP_eta_Min"].Fill(miny)
        #     self.hist["Hist_GP_eta_Max"].Fill(maxy)
           
        #     DeltaY = maxy - miny
        #     self.hist["Hist_GP_eta_Delta"].Fill(DeltaY)



        if  not self.isData: #Rapidity -> chanded to eta again :)

            # if len(ReduceGenParticleClass)== 0:
            #     return 0
            # ReduceGenParticleClass.sort(cmp=comparePFrapidiy)
            # miny = ReduceGenParticleClass[0][0].eta()
            # maxy = ReduceGenParticleClass[len(ReduceGenParticleClass)-1][0].eta()
            
            if len(GenParticleClass)== 0:
                return 0
            GenParticleClass.sort(cmp=comparePFeta)
            miny = GenParticleClass[0][0].eta()
            maxy = GenParticleClass[len(GenParticleClass)-1][0].eta() #eta()pseduorapidty
            


            self.hist["Hist_Y_GP_Min"].Fill(miny)
            self.hist["Hist_Y_GP_Max"].Fill(maxy)
           
            DeltaY = maxy - miny
            self.hist["Hist_GP_Y_Delta"].Fill(DeltaY)

            delta_zero = -1
            delta_zero_pos = -1
            deltaymax = -1
            deltaymax_pos = -1
            # for igp in xrange(0,len(ReduceGenParticleClass)-1):
            #     genp4  = ReduceGenParticleClass[igp][0]
            #     genid  = ReduceGenParticleClass[igp][1]
            for igp in xrange(0,len(ReduceGenParticleClass)): #change   GenParticleClass to ReduceGenParticleClass for testing
                genp4  = ReduceGenParticleClass[igp][0]
                genid  = ReduceGenParticleClass[igp][1]
    

                if igp != len(ReduceGenParticleClass)-1:
                    # deltay = ReduceGenParticleClass[igp+1][0].eta() - ReduceGenParticleClass[igp][0].eta()
                    deltay = ReduceGenParticleClass[igp+1][0].eta() - ReduceGenParticleClass[igp][0].eta() #eta()pseduorapidty

                    if  (deltay > deltaymax):
                        deltaymax = deltay
                        deltaymax_pos = igp

                    if ReduceGenParticleClass[igp+1][0].eta() > 0 and ReduceGenParticleClass[igp][0].eta() < 0:
                        delta_zero = deltay
                        delta_zero_pos = igp


            self.hist["Hist_GP_Y_DeltaMax"].Fill(deltaymax)
            self.hist["Hist_GP_Y_DeltaZero"].Fill(delta_zero)
             
            
            # xi_sd = self.fChain.XiSD
            # xi_dd = self.fChain.XiDD
            mx = -1
            my = -1
            xi_x = self.fChain.Xix
            xi_y= self.fChain.Xiy   
            # self.hist["Hist_MCH_SD"].Fill(xi_sd)
            # self.hist["Hist_MCH_DD"].Fill(xi_dd)
           
            
            if self.CMenergy>0 :    
                xisd = max(xi_x,xi_y);
                xidd = xi_x*xi_y*self.CMenergy * self.CMenergy/(0.938*0.938);

                mx2 = (xi_x * (self.CMenergy)*(self.CMenergy))
                my2 = (xi_y * (self.CMenergy) * self.CMenergy)

                if mx2<=0: mx2=1e-10
                if my2<=0: my2=1e-10

                mx = sqrt(mx2)
                my = sqrt(my2)

                self.hist["Hist_HMC_log10Mx"].Fill(log10(mx))
                self.hist["Hist_HMC_log10My"].Fill(log10(my))
                self.hist["Hist_HMC_2Dlog10MxMy"].Fill(log10(mx),log10(my))


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
            for igp in xrange(0,deltaymax_pos+1): 
                XEtot += ReduceGenParticleClass[igp][0].E()
                XPxtot += ReduceGenParticleClass[igp][0].Px()
                XPytot += ReduceGenParticleClass[igp][0].Py()
                XPztot += ReduceGenParticleClass[igp][0].Pz()
           
            Mx2 = XEtot*XEtot - XPxtot*XPxtot - XPytot*XPytot - XPztot*XPztot
               
            for igp in xrange ((deltaymax_pos+1),len(ReduceGenParticleClass)):
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
        

        if len(PFCandClass) == 0:
            return 0

        PFCandClass.sort(cmp=comparePFeta)
       
        miny = PFCandClass[0][0].eta()
        maxy = PFCandClass[len(PFCandClass)-1][0].eta() # For data i have to use eta
      
        self.hist["Hist_Y_Min"].Fill(miny)
        self.hist["Hist_Y_Max"].Fill(maxy) 
        
        DeltaY = maxy - miny
        self.hist["Hist_Y_Delta"].Fill(DeltaY)

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
         
            self.hist["Hist_Y_Min" + Process_ID_Ext].Fill(miny)
            self.hist["Hist_Y_Max" + Process_ID_Ext].Fill(maxy)  
            self.hist["Hist_Y_Delta" + Process_ID_Ext].Fill(DeltaY)  

        delta_zero_pos = -1
        delta_zero = -1
        deltaymax = -1
        deltaymax_pos = -1
        ParticleFlow_pdg= "_NONE"
         # /// particle types
            # enum ParticleType {
            #   X=0,     // undefined
            #   h,       // charged hadron
            #   e,       //_e 
            #   mu,      // muon 
            #   gamma,   // photon
            #   h0,      // neutral hadron
            #   h_HF,        // HF tower identified as a hadron
            #   e_HF    // HF tower identified as an EM particle 
            #   h_CASTOR
            #   e_CASTOR
        for ipf in xrange(0,len(PFCandClass)):
            pfp4  = PFCandClass[ipf][0]
            pfid  = PFCandClass[ipf][1]
            pfem  = PFCandClass[ipf][2]
            pfhad = PFCandClass[ipf][3]
            
            self.hist["Hist_Y"].Fill(pfp4.eta()) 
            self.hist["Hist_PF"].Fill(pfp4.e())     

            self.hist["Hist_Y" + Process_ID_Ext].Fill(pfp4.eta())     
            self.hist["Hist_PF" + Process_ID_Ext].Fill(pfp4.e())     
           
            self.hist["hParticleCounts"].Fill("all",1)
           
            if pfid == 1:
                ParticleFlow_pdg= "_ch"
                self.hist["hParticleCounts"].Fill("ch",1)
            if pfid == 2:
                ParticleFlow_pdg= "_e" 
                self.hist["hParticleCounts"].Fill("e",1)
            if pfid == 3:
                ParticleFlow_pdg= "_m"
                self.hist["hParticleCounts"].Fill("mu",1) 
            if pfid == 4:
                ParticleFlow_pdg = "_gamma"
                self.hist["hParticleCounts"].Fill("gamma",1)
            if pfid == 5:  
                ParticleFlow_pdg = "_nh"
                self.hist["hParticleCounts"].Fill("nh",1)
            if pfid == 6:
                ParticleFlow_pdg = "_ch_HF"
                self.hist["hParticleCounts"].Fill("ch_HF",1)
            if pfid == 7:  
                ParticleFlow_pdg = "_e_HF"
                self.hist["hParticleCounts"].Fill("e_HF",1)
            if pfid == 9:
                ParticleFlow_pdg= "_e_Castor"
                self.hist["hParticleCounts"].Fill("e_Castor",1)
            if pfid == 8:
                ParticleFlow_pdg= "_ch_Castor"
                self.hist["hParticleCounts"].Fill("ch_Castor",1)
            
            if  abs( pfp4.eta() ) < 1.4:
                self.hist["Hist_PF_barrel"].Fill(pfp4.e()) 
                self.hist["Hist_PF_barrel" + ParticleFlow_pdg].Fill(pfp4.e()) 
                
            if  abs( pfp4.eta() ) > 1.4 and abs( pfp4.eta() ) < 2.6:
                self.hist["Hist_PF_endcap"].Fill(pfp4.e())
                self.hist["Hist_PF_endcap" + ParticleFlow_pdg].Fill(pfp4.e()) 
            if  abs( pfp4.eta() ) > 2.6 and abs( pfp4.eta() ) < 3.2:
                self.hist["Hist_PF_endcap_forwardtransition"].Fill(pfp4.e())
                self.hist["Hist_PF_endcap_forwardtransition" + ParticleFlow_pdg].Fill(pfp4.e())

            if  abs (pfp4.eta()) > 3.2 and abs(pfp4.eta()) < 5.2:
                self.hist["Hist_PF_forward"].Fill(pfp4.e())
                self.hist["Hist_PF_forward" + ParticleFlow_pdg].Fill(pfp4.e()) 
            
            if  (pfp4.eta()) > -6.6 and (pfp4.eta()) < -5.2 :
                self.hist["Hist_PF_Castor"].Fill(pfp4.e())
                self.hist["Hist_PF_Castor" + ParticleFlow_pdg].Fill(pfp4.e()) 

            if abs( pfp4.eta() ) < 1.4:
                self.hist["Hist_PF_barrel"].Fill(pfp4.e()) 
                self.hist["Hist_PF_barrel" + Process_ID_Ext].Fill(pfp4.e()) 
                self.hist["Hist_PF_barrel" + ParticleFlow_pdg].Fill(pfp4.e()) 
                self.hist["Hist_PF_barrel" + Process_ID_Ext + ParticleFlow_pdg].Fill(pfp4.e()) 


            if  abs( pfp4.eta() ) > 1.4 and abs( pfp4.eta() ) < 2.6:
                self.hist["Hist_PF_endcap"].Fill(pfp4.e()) 
                self.hist["Hist_PF_endcap" + Process_ID_Ext].Fill(pfp4.e()) 
                self.hist["Hist_PF_endcap" + ParticleFlow_pdg].Fill(pfp4.e()) 
                self.hist["Hist_PF_endcap"+Process_ID_Ext + ParticleFlow_pdg].Fill(pfp4.e()) 
                                       
           
            if  abs( pfp4.eta() ) > 2.6 and abs( pfp4.eta() ) < 3.2:
                self.hist["Hist_PF_endcap_forwardtransition"].Fill(pfp4.e()) 
                self.hist["Hist_PF_endcap_forwardtransition" + Process_ID_Ext].Fill(pfp4.e()) 
                self.hist["Hist_PF_endcap_forwardtransition" + ParticleFlow_pdg].Fill(pfp4.e()) 
                self.hist["Hist_PF_endcap_forwardtransition" + Process_ID_Ext + ParticleFlow_pdg].Fill(pfp4.e())
                            

            if  abs (pfp4.eta()) > 3.2 and abs(pfp4.eta()) < 5.2:
                self.hist["Hist_PF_forward"].Fill(pfp4.e())
                self.hist["Hist_PF_forward" + Process_ID_Ext].Fill(pfp4.e()) 
                self.hist["Hist_PF_forward" + ParticleFlow_pdg].Fill(pfp4.e()) 
                self.hist["Hist_PF_forward" + Process_ID_Ext + ParticleFlow_pdg].Fill(pfp4.e())
                    
            if  (pfp4.eta()) > -6.6 and (pfp4.eta()) < -5.2 :
                self.hist["Hist_PF_Castor"].Fill(pfp4.e())
                self.hist["Hist_PF_Castor" + Process_ID_Ext].Fill(pfp4.e()) 
                self.hist["Hist_PF_Castor" + ParticleFlow_pdg].Fill(pfp4.e()) 
                self.hist["Hist_PF_Castor"+ Process_ID_Ext + ParticleFlow_pdg].Fill(pfp4.e())
            
            if ipf != len(PFCandClass)-1:
                deltay = PFCandClass[ipf+1][0].eta() - PFCandClass[ipf][0].eta()

                if  (deltay > deltaymax):


                    deltaymax = deltay
                    deltaymax_pos = ipf

                if PFCandClass[ipf+1][0].eta() > 0 and PFCandClass[ipf][0].eta() < 0:
                    delta_zero = deltay
                    delta_zero_pos = ipf
                    self.hist["hNentries"].Fill("find #Delta#eta^{0}",1)

 
        self.hist["Hist_Y_DeltaMax"].Fill(deltaymax)
        self.hist["Hist_Y_DeltaMax"+ Process_ID_Ext].Fill(deltaymax)

        self.hist["Hist_Y_DeltaZero"].Fill(delta_zero)
        self.hist["Hist_Y_DeltaZero"+ Process_ID_Ext].Fill(delta_zero)


        # calculate Mx2 and My2
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
       
        for ipf in xrange(0, deltaymax_pos+1):  
            XEtot += PFCandClass[ipf][0].E()
            XPxtot += PFCandClass[ipf][0].Px()
            XPytot += PFCandClass[ipf][0].Py()
            XPztot += PFCandClass[ipf][0].Pz()

        Mx2 = XEtot*XEtot - XPxtot*XPxtot - XPytot*XPytot - XPztot*XPztot
       
        for ipf in xrange (deltaymax_pos+1,len(PFCandClass)):
            YEtot += PFCandClass[ipf][0].E()
            YPxtot += PFCandClass[ipf][0].Px()
            YPytot += PFCandClass[ipf][0].Py()
            YPztot += PFCandClass[ipf][0].Pz()

        My2 = YEtot*YEtot - YPxtot*YPxtot - YPytot*YPytot - YPztot*YPztot


        # set Mx2, My2 to zero if negative (i.e. the X,Y system is a photon)            
        if Mx2<=0: Mx2=1e-20
        if My2<=0: My2=1e-20

        Mx = sqrt(Mx2)
        My = sqrt(My2)
            
            
        
        if self.CMenergy > 0 :    
        # // calculate xix and xiy
            xix = Mx*Mx/self.CMenergy/self.CMenergy
            xiy = My*My/self.CMenergy/self.CMenergy
           
            xisd = max(xix,xiy);
            xidd = xix*xiy*self.CMenergy * self.CMenergy/(0.938*0.938);
               
            self.hist["Hist_XiX"].Fill(xix)
            self.hist["Hist_XiY"].Fill(xiy)
            self.hist["Hist_XiSD"].Fill(xisd)
            self.hist["Hist_XiDD"].Fill(xidd)

            self.hist["Hist_log10XiX"].Fill(log10(xix))
            self.hist["Hist_log10XiY"].Fill(log10(xiy))
            self.hist["Hist_log10XiSD"].Fill(log10(xisd))
            self.hist["Hist_log10XiDD"].Fill(log10(xidd))

            self.hist["Hist_2Dlog10XiXXiY"].Fill(log10(xix),log10(xiy))

            self.hist["Hist_XiX"+Process_ID_Ext].Fill(xix)
            self.hist["Hist_XiY"+Process_ID_Ext].Fill(xiy)
            self.hist["Hist_XiSD"+Process_ID_Ext].Fill(xisd)
            self.hist["Hist_XiDD"+Process_ID_Ext].Fill(xidd)

            self.hist["Hist_log10XiX"+Process_ID_Ext].Fill(log10(xix))
            self.hist["Hist_log10XiY"+Process_ID_Ext].Fill(log10(xiy))
            self.hist["Hist_log10XiSD"+Process_ID_Ext].Fill(log10(xisd))
            self.hist["Hist_log10XiDD"+Process_ID_Ext].Fill(log10(xidd))

            self.hist["Hist_2Dlog10XiXXiY"+Process_ID_Ext].Fill(log10(xix),log10(xiy))

            self.hist["Hist_log10Mx"].Fill(log10(Mx))
            self.hist["Hist_log10My"].Fill(log10(My))
            self.hist["Hist_2Dlog10MxMy"].Fill(log10(Mx),log10(My))

            self.hist["Hist_log10Mx"+ Process_ID_Ext].Fill(log10(Mx))
            self.hist["Hist_log10My"+ Process_ID_Ext].Fill(log10(My))
            self.hist["Hist_2Dlog10MxMy"+ Process_ID_Ext].Fill(log10(Mx),log10(My))

            if not self.isData:
                self.hist["Hist_GenLogXiXRecoLogXiX"].Fill(log10(xix),log10(GenXiX))
                self.hist["Hist_GenLogXiYRecoLogXiY"].Fill(log10(xiy),log10(GenXiY))
                self.hist["Hist_GenLogXiXRecoLogXiX"+Process_ID_Ext].Fill(log10(xix),log10(GenXiX))
                self.hist["Hist_GenLogXiYRecoLogXiY"+Process_ID_Ext].Fill(log10(xiy),log10(GenXiY))

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
    # sampleList.append("data_ZeroBias1")
    sampleList.append("MinBias_TuneMBR_13TeV-pythia8_MagnetOff")
    #sampleList.append("MinBias_TuneMonash13_13TeV-pythia8_MagnetOff")
  

    maxFilesMC = None# run through all ffiles found
    maxFilesData =None# same
    nWorkers = 1# Use all cpu cores



    slaveParams = {}
    # slaveParams["maxEta"] = 2.


    # use printTTree.py <sampleName> to see what trees are avaliable inside the skim file
    Diffractive.runAll(treeName="EflowTree",
           slaveParameters=slaveParams,
           sampleList=sampleList,
           maxFilesMC = maxFilesMC,
           maxFilesData = maxFilesData,
           nWorkers=nWorkers,
           # maxNevents = 2000,
           verbosity = 2,
           outFile = "plotsDiffractive_247920_mc.root" )
