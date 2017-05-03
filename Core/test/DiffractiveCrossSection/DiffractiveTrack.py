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

def comparePFrapidiy(first,second):
    if first[0].Rapidity() > second[0].Rapidity(): return 1
    if first[0].Rapidity() == second[0].Rapidity(): return 0
    if first[0].Rapidity() < second[0].Rapidity(): return -1

class DiffractiveTrack(CommonFSQFramework.Core.ExampleProofReader.ExampleProofReader):
    def init(self,maxEvents = None):
        
        self.maxEvents = maxEvents
        self.hist = {}
        self.hist["hNentries"] = ROOT.TH1F("hNentries","hNentries",10, 0, 20)
        self.hist["BunchCrossing"] =  ROOT.TH1F("BunchCrossing", "BunchCrossing",  3600, 0-0.5, 3600-0.5)
        self.hist["Runs"] =  ROOT.TH1F("Runs", "Runs",  2000, 246000-0.5, 278000-0.5)
       

        NbrSizeBins = 50
        BinSizeEMin = 0
        BinSizeMax = 50
        self.hist["Histsum_CAS_E"] =  ROOT.TH1F("Histsum_CAS_E", "Histsum_CAS_E" ,100,0.5, 599.5)
        self.hist["Histsum_castor_tag"] =  ROOT.TH1F("Histsum_castor_tag", "Histsum_castor_tag" ,50,0.5, 49.5)
        self.hist["NTracksStripVtx"] = ROOT.TH1F("NTracksStripVtx","NTracksStripVtx",10, 0, 140)
        self.hist["NtrackSize"] = ROOT.TH1F("NtrackSize","NtrackSize",NbrSizeBins, BinSizeEMin,BinSizeMax)
        self.hist["EtaSize"] = ROOT.TH1F("EtaSize","EtaSize",NbrSizeBins, BinSizeEMin,BinSizeMax)
        self.hist["PhiSize"] = ROOT.TH1F("PhiSize","PhiSize",NbrSizeBins, BinSizeEMin,BinSizeMax)
        
        NbrPhiBins = 50
        BinPhiMin = -5
        BinPhiMax = 5

        
        self.hist["ZeroTeslaStripPhi"] = ROOT.TH1F("ZeroTeslaStripPhi","ZeroTeslaStripPhi",NbrPhiBins, BinSizeEMin, BinSizeMax) 
        self.hist["ZeroTeslaPixelPreSplittingPhi"] = ROOT.TH1F("ZeroTeslaPixelPreSplittingPhi","ZeroTeslaPixelPreSplittingPhi",NbrPhiBins, BinSizeEMin, BinSizeMax)      
        self.hist["ZeroTeslaPixelnoPreSplittingPhi"] = ROOT.TH1F("ZeroTeslaPixelnoPreSplittingPhi","ZeroTeslaPixelnoPreSplittingPhi",NbrPhiBins, BinSizeEMin, BinSizeMax)  

        NbrEtaBins = 50
        BinEtaMin = -5
        BinEtaMax = 4
        self.hist["ZeroTeslaStripEta"] = ROOT.TH1F("ZeroTeslaStripEta","ZeroTeslaStripEta",NbrEtaBins, BinEtaMin, BinEtaMax)  
        
        self.hist["ZeroTeslaPixelPreSplittingEta"] = ROOT.TH1F("ZeroTeslaPixelPreSplittingEta","ZeroTeslaPixelPreSplittingEta",NbrEtaBins, BinEtaMin, BinEtaMax)  
        
       
        self.hist["ZeroTeslaPixelnoPreSplittingEta"] = ROOT.TH1F("ZeroTeslaPixelnoPreSplittingEta","ZeroTeslaPixelnoPreSplittingEta",NbrEtaBins, BinEtaMin, BinEtaMax)  
        

        NbrNtrackBins = 10
        BinNtrackMin = 0
        BinNtrackMax = 140
        
        self.hist["NTracksPixelPreSplittingVtx"] = ROOT.TH1F("NTracksPixelPreSplittingVtx","NTracksPixelPreSplittingVtx",NbrNtrackBins, BinNtrackMin, BinEtaMax)
        self.hist["NTracksPixelnoPreSplittingVtx"] = ROOT.TH1F("NTracksPixelnoPreSplittingVtx","NTracksPixelnoPreSplittingVtx",NbrNtrackBins, BinNtrackMin, BinEtaMax)
  



        for h in self.hist:
            self.hist[h].Sumw2()
            self.GetOutputList().Add(self.hist[h])
        
        
        self.castor_tower_p4 = []
        for isec in xrange(0,16):
            self.castor_tower_p4.append( ROOT.ROOT.Math.LorentzVector('ROOT::Math::PxPyPzE4D<double>')(0,0,0,0) )

    def analyze(self):
        # return 1
        weight = 1
        num = 0
        # genTracks
        #num = self.fChain.genTracks.size()
        num = self.fChain.ZeroTeslaStripVtxNtracks.size()
        Eta = 0
        eta = 0
        Ntrack = 0
        phi = 0
        #print self.maxEta # see slaveParams below
        #self.hist["numGenTracks"].Fill(1)
       
      
        self.hist["hNentries"].Fill("all",1)
        self.hist["BunchCrossing"].Fill(self.fChain.bx)
        self.hist["Runs"].Fill(self.fChain.run)

        # if self.fChain.ZeroTeslaStripVtxNtracks.size()!= 1:
        #     return 0
         
        


        self.hist["NtrackSize"].Fill(num)
        self.hist["EtaSize"].Fill(self.fChain.ZeroTeslaStripVtxtrketa.size())
        self.hist["PhiSize"].Fill(self.fChain.ZeroTeslaStripVtxtrkphi.size())
       
        for i in xrange(self.fChain.ZeroTeslaStripVtxtrketa.size()):
            eta = self.fChain.ZeroTeslaStripVtxtrketa.at(i)
            Eta = -np.log(math.tan(eta/2))


            self.hist["ZeroTeslaStripEta"].Fill(Eta)
            phi = self.fChain.ZeroTeslaStripVtxtrkphi.at(i)
            self.hist["ZeroTeslaStripPhi"].Fill(phi)

        for j in xrange(self.fChain.ZeroTeslaStripVtxNtracks.size()):
            Ntrack = self.fChain.ZeroTeslaStripVtxNtracks.at(j)
            self.hist["NTracksStripVtx"].Fill(Ntrack)

        
        for ipn in xrange(self.fChain.ZeroTeslaPixelnoPreSplittingVtxtrketa.size()):
            eta = self.fChain.ZeroTeslaPixelnoPreSplittingVtxtrketa.at(ipn)
            Eta = -np.log(math.tan(eta/2))
            self.hist["ZeroTeslaPixelnoPreSplittingEta"].Fill(Eta)
            phi = self.fChain.ZeroTeslaPixelnoPreSplittingVtxtrkphi.at(ipn)
            self.hist["ZeroTeslaPixelnoPreSplittingPhi"].Fill(phi)

        for jpn in xrange(self.fChain.ZeroTeslaPixelnoPreSplittingVtxNtracks.size()):
            Ntrack = self.fChain.ZeroTeslaPixelnoPreSplittingVtxNtracks.at(jpn)
            self.hist["NTracksPixelnoPreSplittingVtx"].Fill(Ntrack)



        if not self.isData:
            for ip in xrange(self.fChain.ZeroTeslaPixelPreSplittingVtxtrketa.size()):
                eta = self.fChain.ZeroTeslaPixelPreSplittingVtxtrketa.at(ip)
                Eta = -np.log(math.tan(eta/2))
               
                self.hist["ZeroTeslaPixelPreSplittingEta"].Fill(Eta)
                phi = self.fChain.ZeroTeslaPixelPreSplittingVtxtrkphi.at(ip)
                self.hist["ZeroTeslaPixelPreSplittingPhi"].Fill(phi)

            for jp in xrange(self.fChain.ZeroTeslaPixelPreSplittingVtxNtracks.size()):
                Ntrack = self.fChain.ZeroTeslaPixelPreSplittingVtxNtracks.at(jp)
                self.hist["NTracksPixelPreSplittingVtx"].Fill(Ntrack)    


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
    nWorkers = 1 # Use all cpu cores
    


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
