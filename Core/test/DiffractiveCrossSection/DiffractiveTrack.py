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




class DiffractiveTrack(CommonFSQFramework.Core.ExampleProofReader.ExampleProofReader):
    def init(self,maxEvents = None):
        
        self.maxEvents = maxEvents
        self.hist = {}
        self.hist["hNentries"] = ROOT.TH1F("hNentries","hNentries",10, 0, 20)
        self.hist["BunchCrossing"] =  ROOT.TH1F("BunchCrossing", "BunchCrossing",  3600, 0-0.5, 3600-0.5)
        self.hist["Runs"] =  ROOT.TH1F("Runs", "Runs",  2000, 246000-0.5, 278000-0.5)
        self.hist["HFEnergy"] = ROOT.TH1F("HFEnergy","HFEnergy",100, 0, 200)

        NbrSizeBins = 50
        BinSizeEMin = 0
        BinSizeMax = 50
        self.hist["Histsum_CAS_E"] =  ROOT.TH1F("Histsum_CAS_E", "Histsum_CAS_E" ,100,0.5, 599.5)
        self.hist["Histsum_castor_tag"] =  ROOT.TH1F("Histsum_castor_tag", "Histsum_castor_tag" ,50,0.5, 49.5)
        
        self.hist["NtrackSize"] = ROOT.TH1F("NtrackSize","NtrackSize",NbrSizeBins, BinSizeEMin,BinSizeMax)
        self.hist["EtaSize"] = ROOT.TH1F("EtaSize","EtaSize",NbrSizeBins, BinSizeEMin,BinSizeMax)
        self.hist["PhiSize"] = ROOT.TH1F("PhiSize","PhiSize",NbrSizeBins, BinSizeEMin,BinSizeMax)
        self.hist["HistoHFCand"] = ROOT.TH1F("HistoHFCand","HistoHFCand",NbrSizeBins, BinSizeEMin,100)
        NbrPhiBins = 50
        BinPhiMin = -5
        BinPhiMax = 5

        
        self.hist["ZeroTeslaStripPhi"] = ROOT.TH1F("ZeroTeslaStripPhi","ZeroTeslaStripPhi",NbrPhiBins, BinSizeEMin, BinSizeMax) 
        self.hist["ZeroTeslaPixelPreSplittingPhi"] = ROOT.TH1F("ZeroTeslaPixelPreSplittingPhi","ZeroTeslaPixelPreSplittingPhi",NbrPhiBins, BinSizeEMin, BinSizeMax)      
        self.hist["ZeroTeslaPixelnoPreSplittingPhi"] = ROOT.TH1F("ZeroTeslaPixelnoPreSplittingPhi","ZeroTeslaPixelnoPreSplittingPhi",NbrPhiBins, BinSizeEMin, BinSizeMax)  

        NbrEtaBins = 50
        BinEtaMin = -5
        BinEtaMax = 4
        self.hist["ZeroTeslaStriptheta"] = ROOT.TH1F("ZeroTeslaStriptheta","ZeroTeslaStriptheta",50,0,10)  
        self.hist["hfeta"] = ROOT.TH1F("hfeta","hfeta",NbrEtaBins, BinEtaMin,BinEtaMax)
        self.hist["ZeroTeslaStripEta"] = ROOT.TH1F("ZeroTeslaStripEta","ZeroTeslaStripEta",NbrEtaBins, BinEtaMin,BinEtaMax)  
        self.hist["ZeroTeslaStripHFEta"] = ROOT.TH1F("ZeroTeslaStripHFEta","ZeroTeslaStripHFEta",NbrEtaBins, BinEtaMin,BinEtaMax)
        self.hist["ZeroTeslaStripHFEta1"] = ROOT.TH1F("ZeroTeslaStripHFEta1","ZeroTeslaStripHFEta1",NbrEtaBins, BinEtaMin,BinEtaMax)
        self.hist["ZeroTeslaPixelPreSplittingEta"] = ROOT.TH1F("ZeroTeslaPixelPreSplittingEta","ZeroTeslaPixelPreSplittingEta",NbrEtaBins, BinEtaMin, BinEtaMax)  
        
       
        self.hist["ZeroTeslaPixelnoPreSplittingEta"] = ROOT.TH1F("ZeroTeslaPixelnoPreSplittingEta","ZeroTeslaPixelnoPreSplittingEta",NbrEtaBins, BinEtaMin, BinEtaMax)  
        

        NbrNtrackBins = 50
        BinNtrackMin = 0
        BinNtrackMax = 150
        
        self.hist["NTracksStripVtx"] = ROOT.TH1F("NTracksStripVtx","NTracksStripVtx",NbrNtrackBins, BinNtrackMin, BinNtrackMax)
        self.hist["NTracksPixelPreSplittingVtx"] = ROOT.TH1F("NTracksPixelPreSplittingVtx","NTracksPixelPreSplittingVtx",NbrNtrackBins, BinNtrackMin, BinNtrackMax)
        self.hist["NTracksPixelnoPreSplittingVtx"] = ROOT.TH1F("NTracksPixelnoPreSplittingVtx","NTracksPixelnoPreSplittingVtx",NbrNtrackBins, BinNtrackMin, BinNtrackMax)
  



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
        self.hist["NtrackSize"].Fill(num)
        self.hist["EtaSize"].Fill(self.fChain.ZeroTeslaStripVtxtrktheta.size())
        self.hist["PhiSize"].Fill(self.fChain.ZeroTeslaStripVtxtrkphi.size())
        
       

         # if self.fChain.CaloTowersp4.size() > 0:
        for j in xrange(self.fChain.ZeroTeslaStripVtxNtracks.size()):
            Ntrack = self.fChain.ZeroTeslaStripVtxNtracks.at(j)
            self.hist["NTracksStripVtx"].Fill(Ntrack)


        HFTower = self.fChain.CaloTowersp4.size()
        HFCandClass = []
        
        for ihf in xrange(0,HFTower):
            hfp4 = self.fChain.CaloTowersp4[ihf]
            # hfid = self.fChain.PFCandidatesparticleId[ihf] 
            hftowers = self.fChain.CaloTowershasHF[ihf]   
            self.hist["hfeta"].Fill(hfp4.eta()) 
            
            if abs(hfp4.eta()) > 3.2 and abs(hfp4.eta()) < 5.2:
                if (hfp4.e()) > 5:
                    HFCandClass.append([hfp4,hftowers])
                      
        # print ("HFCand", len(HFCandClass) )
        self.hist["HistoHFCand"].Fill(len(HFCandClass)) 
       
        for itrack in xrange(self.fChain.ZeroTeslaStripVtxtrktheta.size()):
            theta= self.fChain.ZeroTeslaStripVtxtrktheta[itrack]
            self.hist["ZeroTeslaStriptheta"].Fill(theta)
            Eta = -np.log(math.tan(theta/2))
            phi = self.fChain.ZeroTeslaStripVtxtrkphi[itrack]
            self.hist["ZeroTeslaStripPhi"].Fill(phi)
            self.hist["ZeroTeslaStripEta"].Fill(Eta)
            self.hist["hNentries"].Fill("track eta",1) 
        
        # //////////////HF CUT////////////////
        Eta = 0
        theta= 0
        
        if len(HFCandClass)== 0:
                return 0
           
        # print ("HFCut", len(HFCandClass) )  
     
        for icut in xrange(self.fChain.ZeroTeslaStripVtxtrktheta.size()):

            theta= self.fChain.ZeroTeslaStripVtxtrktheta[icut]
            Eta = -np.log(math.tan(theta/2))
            self.hist["ZeroTeslaStripHFEta"].Fill(Eta)
            self.hist["hNentries"].Fill("hf cut",1) 
       
 
     
        #     hfp4 = HFCandClass[ipf][0]

            
        # for ipn in xrange(self.fChain.ZeroTeslaPixelnoPreSplittingVtxtrketa.size()):
        #     theta= self.fChain.ZeroTeslaPixelnoPreSplittingVtxtrketa.at(ipn)
        #     Eta = -np.log(math.tan(theta/2))
        #     self.hist["ZeroTeslaPixelnoPreSplittingEta"].Fill(Eta)
        #     phi = self.fChain.ZeroTeslaPixelnoPreSplittingVtxtrkphi.at(ipn)
        #     self.hist["ZeroTeslaPixelnoPreSplittingPhi"].Fill(phi)

        # for jpn in xrange(self.fChain.ZeroTeslaPixelnoPreSplittingVtxNtracks.size()):
        #     Ntrack = self.fChain.ZeroTeslaPixelnoPreSplittingVtxNtracks.at(jpn)
        #     self.hist["NTracksPixelnoPreSplittingVtx"].Fill(Ntrack)

        
       


        # if not self.isData:
        #     for ip in xrange(self.fChain.ZeroTeslaPixelPreSplittingVtxtrketa.size()):
        #         theta= self.fChain.ZeroTeslaPixelPreSplittingVtxtrketa.at(ip)
        #         Eta = -np.log(math.tan(theta/2))
               
        #         self.hist["ZeroTeslaPixelPreSplittingEta"].Fill(Eta)
        #         phi = self.fChain.ZeroTeslaPixelPreSplittingVtxtrkphi.at(ip)
        #         self.hist["ZeroTeslaPixelPreSplittingPhi"].Fill(phi)

        #     for jp in xrange(self.fChain.ZeroTeslaPixelPreSplittingVtxNtracks.size()):
        #         Ntrack = self.fChain.ZeroTeslaPixelPreSplittingVtxNtracks.at(jp)
        #         self.hist["NTracksPixelPreSplittingVtx"].Fill(Ntrack)    


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
    sampleList.append("data_ZeroBias1_MagnetOff_CASTORmeasured")
    sampleList.append("MinBias_CUETP8M1_13TeV-pythia8_MagnetOff_CASTORmeasured")
    maxFilesMC =  None# run through all ffiles found
    maxFilesData = None# same
    nWorkers = 8 # Use all cpu cores
    


    slaveParams = {}
    # slaveParams["maxEta"] = 2.


    # use printTTree.py <sampleName> to see what trees are avaliable inside the skim file
    DiffractiveTrack.runAll(treeName="EflowTree",
           slaveParameters=slaveParams,
           sampleList=sampleList,
           maxFilesMC = maxFilesMC,
           maxFilesData = maxFilesData,
           nWorkers=nWorkers,
           # maxNevents = 200,
           verbosity = 2,
           outFile = "plotsTracks.root" )
