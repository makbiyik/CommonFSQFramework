#!/usr/bin/env python


import CommonFSQFramework.Core.ExampleProofReader
#from rootpy.math.physics.vector import LorentzVector
import sys, os, time
sys.path.append(os.path.dirname(__file__))

import ROOT
ROOT.gROOT.SetBatch(True)
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
from BadChannels2015 import badChannelsSecMod


def comparePFeta(first,second):
    if first[0].eta() > second[0].eta(): return 1
    if first[0].eta() == second[0].eta(): return 0
    if first[0].eta() < second[0].eta(): return -1

class Track(CommonFSQFramework.Core.ExampleProofReader.ExampleProofReader):
    def init(self,maxEvents = None):
        
        self.maxEvents = maxEvents
        self.hist = {}
        self.hist["hNentries"] = ROOT.TH1F("hNentries","hNentries",10, 0, 20)
        self.hist["BunchCrossing"] =  ROOT.TH1F("BunchCrossing", "BunchCrossing",  3600, 0-0.5, 3600-0.5)
        self.hist["Runs"] =  ROOT.TH1F("Runs", "Runs",  2000, 246000-0.5, 278000-0.5)
        self.hist["HFEnergy"] = ROOT.TH1F("HFEnergy","HFEnergy",100, 0, 200)
        
        self.hist["Hist_PixelPiX"] = ROOT.TH1F("Hist_PixelPiX","Hist_PixelPiX",120, -60, 100)
        self.hist["Hist_PixelPiY"] = ROOT.TH1F("Hist_PixelPiY","Hist_PixelPiY",120, -60, 100)
        self.hist["Hist_PixelX"] = ROOT.TH1F("Hist_PixelX","Hist_PixelX",120, -60, 60)
        self.hist["Hist_PixelY"] = ROOT.TH1F("Hist_PixelY","Hist_PixelY",120, -60, 60)
        self.hist["Hist_PixelZ"] = ROOT.TH1F("Hist_PixelZ","Hist_PixelZ",120, -60, 60)
        self.hist["Hist_PixelDeltaZ"] = ROOT.TH1F("Hist_PixelDeltaZ","Hist_PixelDeltaZ",1200,-30, 30)
        self.hist["Hist_Pixelr"] = ROOT.TH1F("Hist_Pixelr","Hist_Pixelr",80, 0, 16)
        self.hist["Hist_2D_Pixelrz"] =  ROOT.TH2D("Hist_2D_Pixelrz", "Hist_2D_Pixelrz", 160, -60, 60,100, 0, 16)
        

        NbrDeltaetaBins = 50
        BinDeltaetaMin = -20
        BinDeltaetaMax = 20

        self.hist["Hist_DeltaEta"] = ROOT.TH1F("Hist_DeltaEta","Hist_DeltaEta",NbrDeltaetaBins,BinDeltaetaMin,BinDeltaetaMax)
        self.hist["Hist_DeltaEta_PixelPreSplitting"] = ROOT.TH1F("Hist_DeltaEta_PixelPreSplitting","Hist_DeltaEta_PixelPreSplitting",NbrDeltaetaBins,BinDeltaetaMin,BinDeltaetaMax)
        self.hist["Hist_DeltaEta_PixelnoPreSplitting"] = ROOT.TH1F("Hist_DeltaEta_PixelnoPreSplitting","Hist_DeltaEta_PixelnoPreSplitting",NbrDeltaetaBins,BinDeltaetaMin,BinDeltaetaMax)



       
        NbrVtxzBins = 50
        BinVtxzMin = -20
        BinVtxzMax = 20

        self.hist["Hist_Vtxz_Strip"] = ROOT.TH1F("Hist_Vtxz_Strip","Hist_Vtxz_Strip",NbrVtxzBins,BinVtxzMin, BinVtxzMax)  
        self.hist["Hist_Vtxz_PixelPreSplitting"] = ROOT.TH1F("Hist_Vtxz_PixelPreSplitting","Hist_Vtxz_PixelPreSplitting",NbrVtxzBins,BinVtxzMin, BinVtxzMax)  
        self.hist["Hist_Vtxz_PixelnoPreSplitting"] = ROOT.TH1F("Hist_Vtxz_PixelnoPreSplitting","Hist_Vtxz_PixelnoPreSplitting",NbrVtxzBins,BinVtxzMin, BinVtxzMax)  

        self.hist["Hist_NrVtx_Strip"] = ROOT.TH1F("Hist_NrVtx_Strip_","Hist_NrVtx_Strip",11,-0.5,10.5)  
        self.hist["Hist_NrVtx_PixelnoPreSplitting"] = ROOT.TH1F("Hist_NrVtx_PixelnoPreSplitting","Hist_NrVtx_PixelnoPreSplitting",11,-0.5,10.5)  



        NbrEtaBins = 50
        BinEtaMin = -6.5
        BinEtaMax = 5.5
        NbrDetaBins = 50
        BinDetaMin = 0
        BinDetaMax = 10


        
       



        NbrSizeBins = 50
        BinSizeEMin = 0
        BinSizeEMax = 50
        self.hist["Histsum_CAS_E"] =  ROOT.TH1F("Histsum_CAS_E", "Histsum_CAS_E" ,100,0.5, 599.5)
        self.hist["Histsum_castor_tag"] =  ROOT.TH1F("Histsum_castor_tag", "Histsum_castor_tag" ,50,0.5, 49.5)
        
        self.hist["Hist_NtrackSize"] = ROOT.TH1F("Hist_NtrackSize","Hist_NtrackSize",NbrSizeBins, BinSizeEMin,BinSizeEMax)
        self.hist["Hist_EtaSize"] = ROOT.TH1F("Hist_EtaSize","Hist_EtaSize",NbrSizeBins, BinSizeEMin,BinSizeEMax)
        self.hist["Hist_PhiSize"] = ROOT.TH1F("Hist_PhiSize","Hist_PhiSize",NbrSizeBins, BinSizeEMin,BinSizeEMax)
        self.hist["Hist_HFCand"] = ROOT.TH1F("Hist_HFCand","Hist_HFCand",NbrSizeBins, BinSizeEMin,100)
        self.hist["Hist_Cand"] = ROOT.TH1F("Hist_Cand","Hist_Cand",NbrSizeBins, BinSizeEMin,100)

        NbrPhiBins = 50
        BinPhiMin = -5
        BinPhiMax = 5

        
        self.hist["Hist_Phi_Strip"] = ROOT.TH1F("Hist_Phi_Strip","Hist_Phi_Strip",NbrPhiBins,  BinPhiMin, BinPhiMax) 
        self.hist["Hist_Phi_PixelPreSplitting"] = ROOT.TH1F("Hist_Phi_PixelPreSplitting","Hist_Phi_PixelPreSplitting",NbrPhiBins,  BinPhiMin, BinPhiMax)      
        self.hist["Hist_Phi_PixelnoPreSplitting"] = ROOT.TH1F("Hist_Phi_PixelnoPreSplitting","Hist_Phi_PixelnoPreSplitting",NbrPhiBins,  BinPhiMin, BinPhiMax)  

        # NbrEtaBins = 50
        # BinEtaMin = -5
        # BinEtaMax = 4
        self.hist["Hist_Theta_Stript"] = ROOT.TH1F("Hist_Theta_Stript","Hist_Theta_Stript",50,0,10)  
        self.hist["Hist_p4Eta"] = ROOT.TH1F("Hist_p4Eta","Hist_p4Eta",NbrEtaBins, BinEtaMin,BinEtaMax)
        self.hist["Hist_Eta_Strip"] = ROOT.TH1F("Hist_Eta_Strip","Hist_Eta_Strip",NbrEtaBins, BinEtaMin,BinEtaMax)  
        self.hist["Hist_HFeta_Strip"] = ROOT.TH1F("Hist_HFeta_Strip","Hist_HFeta_Strip",NbrEtaBins, BinEtaMin,BinEtaMax)
        self.hist["Hist_Eta_PixelPreSplitting"] = ROOT.TH1F("Hist_Eta_PixelPreSplitting","Hist_Eta_PixelPreSplitting",NbrEtaBins, BinEtaMin, BinEtaMax)  
        self.hist["Hist_Eta_PixelnoPreSplitting"] = ROOT.TH1F("Hist_Eta_PixelnoPreSplitting","Hist_Eta_PixelnoPreSplitting",NbrEtaBins, BinEtaMin, BinEtaMax)  
        

        NbrNtrackBins = 50
        BinNtrackMin = 0
        BinNtrackMax = 150
        
        self.hist["Hist_NTracks_Strip"] = ROOT.TH1F("Hist_NTracks_Strip","Hist_NTracks_Strip",NbrNtrackBins, BinNtrackMin, BinNtrackMax)
        self.hist["Hist_NTracks_PixelPreSplitting"] = ROOT.TH1F("Hist_NTracks_PixelPreSplitting","Hist_NTracks_PixelPreSplitting",NbrNtrackBins, BinNtrackMin, BinNtrackMax)
        self.hist["Hist_NTracks_PixelnoPreSplitting"] = ROOT.TH1F("Hist_NTracks_PixelnoPreSplitting","Hist_NTracks_PixelnoPreSplitting",NbrNtrackBins, BinNtrackMin, BinNtrackMax)
  

        self.hist["Hist_2D_PixelEtaPhi"] =  ROOT.TH2D("Hist_2D_PixelEtaPhi", "Hist_2D_PixelEtaPhi",NbrPhiBins,  BinPhiMin, BinPhiMax,NbrEtaBins, BinEtaMin, BinEtaMax)

        for h in self.hist:
            self.hist[h].Sumw2()
            self.GetOutputList().Add(self.hist[h])
        
        
        

    def analyze(self):
        # return 1
        

        # if self.isData:
        #     if not self.fChain.run == 247324: return 1 

        weight = 1
        num = 0
        # genTracks
        #num = self.fChain.genTracks.size()
        num = self.fChain.ZeroTeslaStripVtxNtracks.size()
        Eta = 0
        theta= 0
        Ntrack = 0
        phi = 0
        #print self.maxEta # see slaveParams below
        #self.hist["numGenTracks"].Fill(1)
      
      
        self.hist["hNentries"].Fill("all",1)
        self.hist["BunchCrossing"].Fill(self.fChain.bx)
        self.hist["Runs"].Fill(self.fChain.run)
        self.hist["Hist_NtrackSize"].Fill(num)
        self.hist["Hist_EtaSize"].Fill(self.fChain.ZeroTeslaStripVtxtrktheta.size())
        self.hist["Hist_PhiSize"].Fill(self.fChain.ZeroTeslaStripVtxtrkphi.size())
     

        HFTower = self.fChain.CaloTowersp4.size()
       
       
        TrackHFCandClass = []
        for ihf in xrange(0,HFTower):
            hfp4 = self.fChain.CaloTowersp4[ihf]
            # hfid = self.fChain.PFCandidatesparticleId[ihf] 
            hftowers = self.fChain.CaloTowershasHF[ihf]   
            self.hist["Hist_p4Eta"].Fill(hfp4.eta()) 
            
            if abs(hfp4.eta()) > 3.2 and abs(hfp4.eta()) < 5.2:
                if (hfp4.e()) > 5:
                    TrackHFCandClass.append([hfp4,hftowers])  
    
                
        self.hist["Hist_NrVtx_Strip"].Fill(self.fChain.ZeroTeslaStripVtxz.size())
        self.hist["Hist_NrVtx_PixelnoPreSplitting"].Fill(self.fChain.ZeroTeslaPixelnoPreSplittingVtxz.size())
        self.hist["Hist_HFCand"].Fill(len(TrackHFCandClass))  
        for i in xrange(self.fChain.ZeroTeslaStripVtxtrktheta.size()):
            theta = self.fChain.ZeroTeslaStripVtxtrktheta[i]
            self.hist["Hist_Theta_Stript"].Fill(theta)
            Eta = -np.log(math.tan(theta/2))
            self.hist["Hist_Eta_Strip"].Fill(Eta)
            self.hist["hNentries"].Fill("track eta",1) 
           
            # self.hist["Hist_Vtxz_PixelnoPreSplitting"].Fill(self.fChain.ZeroTeslaPixelnoPreSplittingVtxz[i])
            # self.hist["Hist_DeltaEta_PixelnoPreSplitting"].Fill(self.fChain.ZeroTeslaPixelnoPreSplittingVtxtrkdeltaeta[i])
            
        # //////////////HF CUT////////////////#
        
        Eta = 0
        theta = 0
        if len(TrackHFCandClass) == 0:
                return 0

       
        for i in xrange(self.fChain.ZeroTeslaPixelnoPreSplittingVtxtrktheta.size()):
            theta = self.fChain.ZeroTeslaPixelnoPreSplittingVtxtrktheta[i]
            Eta = -np.log(math.tan(theta/2))
            self.hist["Hist_Eta_PixelnoPreSplitting"].Fill(Eta)
            if self.fChain.ZeroTeslaPixelnoPreSplittingVtxz.size() == 1:
                for iphi in xrange(self.fChain.ZeroTeslaPixelnoPreSplittingVtxtrktheta.size()):
                    phi = self.fChain.ZeroTeslaPixelnoPreSplittingVtxtrkphi[iphi]
                    self.hist["Hist_Phi_PixelnoPreSplitting"].Fill(phi)
                    self.hist["Hist_2D_PixelEtaPhi"].Fill(phi,Eta)
            
                self.hist["hNentries"].Fill("vrtz",1) 
            
        for jtrkno in xrange(self.fChain.ZeroTeslaPixelnoPreSplittingVtxNtracks.size()):
            Ntrack = self.fChain.ZeroTeslaPixelnoPreSplittingVtxNtracks[jtrkno]
            self.hist["Hist_NTracks_PixelnoPreSplitting"].Fill(Ntrack)
       
        for icut in xrange(self.fChain.ZeroTeslaStripVtxtrktheta.size()):

            theta= self.fChain.ZeroTeslaStripVtxtrktheta[icut]
            Eta = -np.log(math.tan(theta/2))
            self.hist["Hist_HFeta_Strip"].Fill(Eta)
            phi = self.fChain.ZeroTeslaStripVtxtrkphi[icut]
            self.hist["Hist_Phi_Strip"].Fill(phi)
            # self.hist["Hist_Vtxz_Strip"].Fill(self.fChain.ZeroTeslaStripVtxz[icut])


        self.hist["hNentries"].Fill("hf cut",1)    
       
        for j in xrange(self.fChain.ZeroTeslaStripVtxNtracks.size()):
            Ntrack = self.fChain.ZeroTeslaStripVtxNtracks[j]
            self.hist["Hist_NTracks_Strip"].Fill(Ntrack)


        x = 0
        y = 0 
        xpi = 0
        ypi = 0 
        z = 0 
        r = 0
        deltaz = 0
        z2vtx = 0
        zSort =[]
        for ivtx in xrange(self.fChain.ZeroTeslaPixelnoPreSplittingVtxtrkX.size()):
            x = self.fChain.ZeroTeslaPixelnoPreSplittingVtxtrkX[ivtx]
            y = self.fChain.ZeroTeslaPixelnoPreSplittingVtxtrkY[ivtx]
            z = self.fChain.ZeroTeslaPixelnoPreSplittingVtxtrkZ[ivtx]
            
            r = sqrt( (x**2) + (y**2))
            self.hist["Hist_PixelX"].Fill(x)
            self.hist["Hist_PixelY"].Fill(y)
            self.hist["Hist_PixelZ"].Fill(z)
           
            self.hist["Hist_Pixelr"].Fill(r)
            self.hist["Hist_2D_Pixelrz"].Fill(z,r)
        
            if self.fChain.ZeroTeslaPixelnoPreSplittingVtxNtracks[ivtx] > 2:
                zSort.append(z)

        zSort.sort()
   
        if len(zSort) > 1:
            for ivtx in xrange(len(zSort)-1):
                deltaz = zSort[ivtx+1]- zSort[ivtx]
                self.hist["Hist_PixelDeltaZ"].Fill(deltaz)
   

        # TrackHFCandClass.sort(cmp=comparePFeta)
        # miny = TrackHFCandClass[0][0].eta()
        # maxy = TrackHFCandClass[len(TrackCandClass)-1][0].eta() #eta()pseduorapidty


        # self.hist["Hist_Y_Min"].Fill(miny)
        # self.hist["Hist_Y_Max"].Fill(maxy)
           
        # DeltaY = maxy - miny
        # self.hist["Hist_Y_Delta"].Fill(DeltaY)  
        # delta_zero = -1
        # delta_zero_pos = -1
        # deltaymax = -1
        # deltaymax_pos = -1
        
        # for itrack in xrange(0,len(TrackCandClass)): #change   GenParticleClass to TrackHFCandClass for testing
        #     trackp4  = TrackHFCandClass[itrack][0]
        #     # trackid  = TrackHFCandClass[itrack][1]


        #     if itrack != len(TrackCandClass)-1:
        #         # deltay = TrackHFCandClass[itrack+1][0].eta() - TrackHFCandClass[itrack][0].eta()
        #         deltay = TrackHFCandClass[itrack+1][0].eta() - TrackHFCandClass[itrack][0].eta() #eta()pseduorapidty

        #         if  (deltay > deltaymax):
        #             deltaymax = deltay
        #             deltaymax_pos = itrack

        #         if TrackHFCandClass[itrack+1][0].eta() > 0 and TrackHFCandClass[itrack][0].eta() < 0:
        #             delta_zero = deltay
        #             delta_zero_pos = itrack


            
        #     self.hist["Hist_Y_DeltaZero"].Fill(delta_zero)
            


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
    Track.runAll(treeName="EflowTree",
           slaveParameters=slaveParams,
           sampleList=sampleList,
           maxFilesMC = maxFilesMC,
           maxFilesData = maxFilesData,
           nWorkers=nWorkers,
           # maxNevents = 200,
           verbosity = 2,
           outFile = "plotsTracks_247934.root" )
