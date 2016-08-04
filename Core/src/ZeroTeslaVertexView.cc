#include "CommonFSQFramework/Core/interface/ZeroTeslaVertexView.h"
#include <cmath>

#include "../interface/LineTrackingProducer.h"

#include "Geometry/TrackerGeometryBuilder/interface/TrackerGeometry.h"
#include "Geometry/Records/interface/TrackerDigiGeometryRecord.h"
#include "Geometry/CommonDetUnit/interface/GeomDet.h"

#include "DataFormats/TrackerRecHit2D/interface/SiPixelRecHitCollection.h"
#include "DataFormats/TrackerRecHit2D/interface/SiStripMatchedRecHit2DCollection.h"
#include "DataFormats/TrackerRecHit2D/interface/SiStripRecHit2DCollection.h"

#include "Geometry/TrackerGeometryBuilder/interface/StripGeomDetUnit.h"

#include "FWCore/Framework/interface/ESHandle.h"

#include <vector>

#include "DataFormats/BeamSpot/interface/BeamSpot.h"

using namespace std;

struct RawPixelRecHit;
struct RawStripRecHit;

ZeroTeslaVertexView::ZeroTeslaVertexView(const edm::ParameterSet& iConfig, TTree * tree, edm::ConsumesCollector && iC):
EventViewBase(iConfig,  tree)
{
    m_usePixels = iConfig.getParameter<bool>("usePixel");
    m_src = iConfig.getParameter<edm::InputTag>("src");

    iC.consumes<reco::BeamSpot >(edm::InputTag("offlineBeamSpot"));    
    if(m_usePixels) iC.consumes<SiPixelRecHitCollection >(m_src);
    else iC.consumesMany<SiStripMatchedRecHit2DCollection >();

    registerVecFloat("_vrtxX",tree);
    registerVecFloat("_vrtxY",tree);
    registerVecFloat("_vrtxZ",tree);
    registerVecFloat("_HitX",tree);
    registerVecFloat("_HitY",tree);
    registerVecFloat("_HitZ",tree);
    // registerVecFloat("_PiX", tree);
    // registerVecFloat("_PiY",tree);
    registerVecFloat("_trkVertex",tree);
    // registerVecFloat("PiZ",tree );
           
    registerVecFloat("_trktheta",tree);
    registerVecFloat("_trkphi",tree);
    registerVecFloat("_rkdelta",tree);
    registerVecInt("_Ntracks", tree);    
}


void ZeroTeslaVertexView::fillSpecific(const edm::Event& iEvent, const edm::EventSetup& iSetup){

    // get the beamspot
    reco::BeamSpot beamSpot;
    edm::Handle<reco::BeamSpot> beamSpotHandle;
    iEvent.getByLabel("offlineBeamSpot", beamSpotHandle);
    if ( beamSpotHandle.isValid() )
    {
        beamSpot = *beamSpotHandle;
    }

    // Get tracker geometry
    edm::ESHandle<TrackerGeometry> trackerHandle;
    iSetup.get<TrackerDigiGeometryRecord>().get(trackerHandle);
    const TrackerGeometry* theTracker = trackerHandle.product();

    std::vector<RawPixelRecHit> RawPixelRecHits;
    std::vector<RawStripRecHit> RawStripRecHits;

    // get Pixel RecHits and save them in a format that the LineTrackingProducer can deal with
    if (m_usePixels) {
        edm::Handle<SiPixelRecHitCollection> pixelColl;
        iEvent.getByLabel(m_src, pixelColl);
        const SiPixelRecHitCollection* thePixelHits = pixelColl.product();

        for(SiPixelRecHitCollection::DataContainer::const_iterator recHit = thePixelHits->data().begin(); recHit!= thePixelHits->data().end(); recHit++) {
            if(recHit->isValid()){
                DetId id = recHit->geographicalId();
                LocalPoint lpos = recHit->localPosition();
                GlobalPoint p = theTracker->idToDet(id)->toGlobal(lpos);
                SiPixelRecHit::ClusterRef const & cluster = recHit->cluster();
                vector<SiPixelCluster::Pixel> pixels = cluster->pixels();
                
                
                bool isFirst = true;
                unsigned int xmin=0, xmax=0, ymin=0, ymax=0;
                for(vector<SiPixelCluster::Pixel>::const_iterator pixel = pixels.begin(); pixel!= pixels.end(); pixel++) {
                    if(pixel->x > xmax || isFirst) xmax = pixel->x;
                    if(pixel->x < xmin || isFirst) xmin = pixel->x;
                    if(pixel->y > ymax || isFirst) ymax = pixel->y;
                    if(pixel->y < ymin || isFirst) ymin = pixel->y;
                    isFirst = false;
                    // addToFVec("PiX", pixel->x);
                    // addToFVec("PiY", pixel->y);
                    // // addToFVec("PiZ", pixel->z);
               

                }
    
                RawPixelRecHit tmp;
                tmp.x = p.x();
                tmp.y = p.y();
                tmp.z = p.z();
                tmp.nx = int(xmax-xmin)+1;
                tmp.ny = int(ymax-ymin)+1;
                tmp.id = id;

                RawPixelRecHits.push_back(tmp);
            }
        }
    }

    // get Strip RecHits and save them in a format that the LineTrackingProducer can deal with
  
    if (!m_usePixels) {
        vector<edm::Handle<SiStripMatchedRecHit2DCollection> > stripColls;
        iEvent.getManyByType(stripColls);
    
        for(vector<edm::Handle<SiStripMatchedRecHit2DCollection> >::const_iterator stripColl = stripColls.begin(); stripColl!= stripColls.end(); stripColl++){
            const SiStripMatchedRecHit2DCollection* theStripHits = (*stripColl).product();
            for(SiStripMatchedRecHit2DCollection::DataContainer::const_iterator recHit = theStripHits->data().begin(); recHit!= theStripHits->data().end(); recHit++){
                DetId id = recHit->geographicalId();
                LocalPoint lpos = recHit->localPosition();
                GlobalPoint p = theTracker->idToDet(id)->toGlobal(lpos);
    
                RawStripRecHit tmp;
                tmp.x = p.x();
                tmp.y = p.y();
                tmp.z = p.z();
                tmp.monoSize = recHit->monoHit().cluster()->amplitudes().size();
                tmp.stereoSize = recHit->stereoHit().cluster()->amplitudes().size();
                tmp.monoId = recHit->monoHit().geographicalId();
                tmp.stereoId = recHit->stereoHit().geographicalId();

                RawStripRecHits.push_back(tmp);
            }
        }
    }

    // C
    for(std::vector<RawPixelRecHit>::iterator RecHit = RawPixelRecHits.begin(); RecHit != RawPixelRecHits.end(); ++RecHit){
        addToFVec("_HitX",RecHit->x);
        addToFVec("_HitY",RecHit->y);
        addToFVec("_HitZ",RecHit->z);
    }
    
    // Calculate vertices
    LineTrackingProducer theProducer(m_usePixels, beamSpot.x0(), beamSpot.y0());
    if (m_usePixels) theProducer.run(RawPixelRecHits);
    if (!m_usePixels) theProducer.run(RawStripRecHits);
    // Get result
    std::vector<double> VerticesX, VerticesY, VerticesZ;
    std::vector<int> nTracks;
    int nVertices = theProducer.getVertices(VerticesX, VerticesY, VerticesZ, nTracks);

    // fill trees
    for ( int i=0; i<nVertices; i++){
        addToFVec("_vrtxX",VerticesX[i]);
        addToFVec("_vrtxY",VerticesY[i]);
        addToFVec("_vrtxZ",VerticesZ[i]);
        addToIVec("_Ntracks",nTracks[i]);
    }
    std::vector<double> TracksPhi,Trackstheta,TracksDelta;
    std:: vector<int> TracksVertex;
    int ntrk = theProducer.getTracks(Trackstheta, TracksPhi,TracksDelta,TracksVertex);
    
    for ( int i=0; i<ntrk; i++){
        addToFVec("_trktheta",Trackstheta[i]);
        addToFVec("_trkphi",TracksPhi[i]);
        addToFVec("_trkdelta",TracksDelta[i]);
        addToFVec("_trkVertex",TracksVertex[i]);

    }
    
    


    // std::vector<double> PixelRecHitX, PixelRecHitY, PixelRecHitZ;
  

    
}
