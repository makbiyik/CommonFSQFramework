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
        self.hist["Hist_Vrtx_Z"] = ROOT.TH1F("Hist_Vrtx_Z","Hist_Vrtx_Z",120, -60, 60)
        self.hist["Hist_Vrtx_DeltaZ"] = ROOT.TH1F("Hist_Vrtx_DeltaZ","Hist_Vrtx_DeltaZ",120,-30, 30)#1200
        self.hist["Hist_Pixelr"] = ROOT.TH1F("Hist_Pixelr","Hist_Pixelr",80, 0, 16)
        self.hist["Hist_2D_Pixelrz"] =  ROOT.TH2D("Hist_2D_Pixelrz", "Hist_2D_Pixelrz", 160, -60, 60,100, 0, 16)
        self.hist["Hist_2D_Vrtz_Z1Z2"] =  ROOT.TH2D("Hist_2D_Vrtz_Z1Z2", "Hist_2D_Vrtz_Z1Z2", 160, -60, 60,160, -60, 60)

        NbrDeltaetaBins = 50
        BinDeltaetaMin = -20
        BinDeltaetaMax = 20
      
        NbrVtxzBins = 50
        BinVtxzMin = -20
        BinVtxzMax = 20
    
        self.hist["Hist_Vtxz_PixelnoPreSplitting"] = ROOT.TH1F("Hist_Vtxz_PixelnoPreSplitting","Hist_Vtxz_PixelnoPreSplitting",NbrVtxzBins,BinVtxzMin, BinVtxzMax)  
        self.hist["Hist_NrVtx"] = ROOT.TH1F("Hist_NrVtx","Hist_NrVtx",11,-0.5,10.5)  
        self.hist["Hist_VrtxId"] = ROOT.TH1F("Hist_VrtxId","Hist_VrtxId",11,-0.5,20.5)  
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
        self.hist["Hist_trkPhi"] = ROOT.TH1F("Hist_trkPhi","Hist_trkPhi",NbrPhiBins,  BinPhiMin, BinPhiMax)  

        # NbrEtaBins = 50
        # BinEtaMin = -5
        # BinEtaMax = 4
        self.hist["Hist_trkEta"] = ROOT.TH1F("Hist_trkEta","Hist_trkEta",NbrEtaBins, BinEtaMin, BinEtaMax)  
        
        NbrNtrackBins = 50
        BinNtrackMin = 0
        BinNtrackMax = 150
        
      
        self.hist["Hist_NbrTracks_vrtx"] = ROOT.TH1F("Hist_NbrTracks_vrtx","Hist_NbrTracks_vrtx",NbrNtrackBins, BinNtrackMin, BinNtrackMax)
        
        self.hist["Hist_2D_trkEtaPhi"] =  ROOT.TH2D("Hist_2D_trkEtaPhi", "Hist_2D_trkEtaPhi",NbrPhiBins,  BinPhiMin, BinPhiMax,NbrEtaBins, BinEtaMin, BinEtaMax)

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
        num = self.fChain.ZeroTeslaStripVtx_Ntracks.size()
        Eta = 0
        theta= 0
        Ntrack = 0
        phi = 0
        trk_vrtx= 0
        #print self.maxEta # see slaveParams below
        #self.hist["numGenTracks"].Fill(1)
      
      
        self.hist["hNentries"].Fill("all",1)
        self.hist["BunchCrossing"].Fill(self.fChain.bx)
        self.hist["Runs"].Fill(self.fChain.run)
        self.hist["Hist_NtrackSize"].Fill(num)
        
        # if self.isData:
        #     if not self.fChain.run == 247324 :return 1 
        #     if not self.fChain.bx == 208 : return 0 

        HFTower = self.fChain.CaloTowersp4.size()
       
       
        TrackHFCandClass = []
        for ihf in xrange(0,HFTower):
            hfp4 = self.fChain.CaloTowersp4[ihf]
            # hfid = self.fChain.PFCandidatesparticleId[ihf] 
            hftowers = self.fChain.CaloTowershasHF[ihf]   
           
            if abs(hfp4.eta()) > 3.2 and abs(hfp4.eta()) < 5.2:
                if (hfp4.e()) > 5:
                    TrackHFCandClass.append([hfp4,hftowers])  
    
            
        self.hist["Hist_NrVtx"].Fill(self.fChain.ZeroTeslaStripVtx_vrtxZ.size())
        self.hist["Hist_HFCand"].Fill(len(TrackHFCandClass))  
       
        self.hist["hNentries"].Fill("track eta",1) 
           
            # self.hist["Hist_Vtxz_PixelnoPreSplitting"].Fill(self.fChain.ZeroTeslaPixelnoPreSplittingVtx_z[i])
            # self.hist["Hist_DeltaEta_PixelnoPreSplitting"].Fill(self.fChain.ZeroTeslaPixelnoPreSplittingVtx_trkdeltaeta[i])
            
        # //////////////HF CUT////////////////#
        
        Eta = 0
        theta = 0
        trk_vrtx =0 
        if len(TrackHFCandClass) == 0:
                return 

        self.hist["hNentries"].Fill("hf cut",1)    


        if self.fChain.ZeroTeslaPixelnoPreSplittingVtx_vrtxX.size() > 0: 
            self.hist["hNentries"].Fill("vrtz",1) 

        if self.fChain.ZeroTeslaPixelnoPreSplittingVtx_vrtxX.size() == 1: 
            for i in xrange(self.fChain.ZeroTeslaPixelnoPreSplittingVtx_trktheta.size()):
                theta = self.fChain.ZeroTeslaPixelnoPreSplittingVtx_trktheta[i]
                Eta = -np.log(math.tan(theta/2))
                self.hist["Hist_trkEta"].Fill(Eta)
                phi = self.fChain.ZeroTeslaPixelnoPreSplittingVtx_trkphi[i]    
                self.hist["Hist_trkPhi"].Fill(phi)
                self.hist["Hist_2D_trkEtaPhi"].Fill(phi,Eta)
        
        for i in xrange(self.fChain.ZeroTeslaPixelnoPreSplittingVtx_trktheta.size()):
            vrtxId = self.fChain.ZeroTeslaPixelnoPreSplittingVtx_trkVertex[i]
            self.hist["Hist_VrtxId"].Fill(vrtxId)   
           
            
        for jtrkno in xrange(self.fChain.ZeroTeslaPixelnoPreSplittingVtx_Ntracks.size()):
            Ntrack = self.fChain.ZeroTeslaPixelnoPreSplittingVtx_Ntracks[jtrkno]
            self.hist["Hist_NbrTracks_vrtx"].Fill(Ntrack)
       
        
       
    
        x = 0
        y = 0 
        xpi = 0
        ypi = 0 
        z = 0 
        r = 0
        deltaz = 0
        z2vtx = 0
        xhit=0
        yhit=0
        zhit=0
        zSort =[]
       

        for ihit in xrange(self.fChain.ZeroTeslaPixelnoPreSplittingVtx_HitX.size()):
            xhit = self.fChain.ZeroTeslaPixelnoPreSplittingVtx_HitX[ihit]
            yhit = self.fChain.ZeroTeslaPixelnoPreSplittingVtx_HitY[ihit]
            zhit = self.fChain.ZeroTeslaPixelnoPreSplittingVtx_HitZ[ihit]
            
            r = sqrt((xhit**2) + (yhit**2))
        
            self.hist["Hist_2D_Pixelrz"].Fill(zhit,r)


        for ivtx in xrange(self.fChain.ZeroTeslaPixelnoPreSplittingVtx_vrtxX.size()):
            x = self.fChain.ZeroTeslaPixelnoPreSplittingVtx_vrtxX[ivtx]
            y = self.fChain.ZeroTeslaPixelnoPreSplittingVtx_vrtxY[ivtx]
            z = self.fChain.ZeroTeslaPixelnoPreSplittingVtx_vrtxZ[ivtx]
            self.hist["Hist_Vrtx_Z"].Fill(z)  

            # if self.fChain.ZeroTeslaPixelnoPreSplittingVtx_Ntracks[ivtx] > 2:
            zSort.append(z)

        zSort.sort()
   
        if len(zSort) == 2:
            for ivtx in xrange(len(zSort)-1):
                deltaz = zSort[ivtx+1]- zSort[ivtx]
                self.hist["Hist_Vrtx_DeltaZ"].Fill(deltaz)
                self.hist["Hist_2D_Vrtz_Z1Z2"].Fill(zSort[ivtx+1],zSort[ivtx])
                
    


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
    # sampleList.append("data_ZeroBias1_CASTOR")
    sampleList.append("data_ZeroBias1_CASTOR")
    sampleList.append("MinBias_CUETP8M1_13TeV-pythia8_MagnetOff_CASTORmeasured_newNoise")
    maxFilesMC = None# run through all ffiles 247934found
    maxFilesData = None# same
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
           outFile = "plotsTracks_247324.root" )
