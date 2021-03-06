#include "CommonFSQFramework/Core/interface/CastorTowerView.h"



CastorTowerView::CastorTowerView(const edm::ParameterSet& iConfig, TTree * tree, edm::ConsumesCollector && iC):
EventViewBase(iConfig,  tree)
{
    m_inputCol = iConfig.getParameter<edm::InputTag>("inputcoll");
    iC.consumes< reco::CastorTowerCollection >(edm::InputTag(m_inputCol)); 
    registerVecP4("p4", tree);
    registerVecFloat("emEnergy",tree);
    registerVecFloat("hadEnergy",tree);
    registerVecInt("Nrechits", tree);    

}


void CastorTowerView::fillSpecific(const edm::Event& iEvent, const edm::EventSetup& iSetup){

    edm::Handle<reco::CastorTowerCollection> CastorTowers;
    iEvent.getByLabel(m_inputCol,CastorTowers);
    
    for (reco::CastorTowerCollection::const_iterator i = CastorTowers->begin(); i != CastorTowers->end(); ++i) {
        
        addToP4Vec("p4", reco::Candidate::LorentzVector(i->px(),i->py(),i->pz(),i->energy()));
	addToFVec("emEnergy",i->emEnergy());
	addToFVec("hadEnergy",i->hadEnergy());
	addToIVec("Nrechits",i->rechitsSize());
	

    }

}
