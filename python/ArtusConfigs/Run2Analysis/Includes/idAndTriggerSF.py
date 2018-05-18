# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import json
import Artus.Utility.jsonTools as jsonTools
import copy

class IdAndTriggerSF(dict):
	def __init__(self, nickname, channel, dcach=False):

		if dcach:
			if channel == "ET":
				if re.search("(Fall15MiniAODv2|Run2015D|Embedding2015)", nickname):
					self["TriggerEfficiencyData"] = [ "0:root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/ohlushch/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2015_Electron_Ele23_fall15.root" ]
					self["TriggerEfficiencyMc"] = [ "0:root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/ohlushch/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Electron_Ele23_fall15.root"]

					self["IdentificationEfficiencyData"] = ["0:root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/ohlushch/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2015_Electron_IdIso0p1_fall15.root"]
					self["IdentificationEfficiencyMc"] = ["0:root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/ohlushch/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC_Electron_IdIso0p1_fall15.root"]

				elif re.search("Run2017|Summer17|Fall17", nickname):
					self["TriggerEfficiencyData"] = ["0:root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/ohlushch/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2017_Electron_Ele32orEle35.root"]
					self["TriggerEfficiencyMc"] = ["0:root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/ohlushch/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MCFall2017_Electron_Ele32orEle35.root"]

					self["IdentificationEfficiencyData"] = ["0:root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/ohlushch/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2017_Electron_IdIso_IsoLt0.10_eff_RerecoFall17.root"]
					self["IdentificationEfficiencyMc"] = ["0:root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/ohlushch/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MCFall2017_Electron_IdIso_IsoLt0.10_eff_RerecoFall17.root"]

				else:
					self["TriggerEfficiencyData"] = ["0:root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/ohlushch/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2016_Electron_Ele25WPTight_eff.root" ]
					self["TriggerEfficiencyMc"] = ["0:root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/ohlushch/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Electron_Ele25WPTight_eff.root" ]

					self["IdentificationEfficiencyData"] = ["0:root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/ohlushch/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2016_Electron_IdIso_IsoLt0p1_eff.root"]
					self["IdentificationEfficiencyMc"] = ["0:root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/ohlushch/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC_Electron_IdIso_IsoLt0p1_eff.root"]
		else:
			if channel == "ET":
				if re.search("(Fall15MiniAODv2|Run2015D|Embedding2015)", nickname):
					self["TriggerEfficiencyData"] = [ "0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2015_Electron_Ele23_fall15.root" ]
					self["TriggerEfficiencyMc"] = [ "0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Electron_Ele23_fall15.root"]

					self["IdentificationEfficiencyData"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2015_Electron_IdIso0p1_fall15.root"]
					self["IdentificationEfficiencyMc"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC_Electron_IdIso0p1_fall15.root"]

				elif re.search("Run2017|Summer17|Fall17", nickname):
					self["TriggerEfficiencyData"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2017_Electron_Ele32orEle35.root"]
					self["TriggerEfficiencyMc"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MCFall2017_Electron_Ele32orEle35.root"]

					self["IdentificationEfficiencyData"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2017_Electron_IdIso_IsoLt0.10_eff_RerecoFall17.root"]
					self["IdentificationEfficiencyMc"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MCFall2017_Electron_IdIso_IsoLt0.10_eff_RerecoFall17.root"]

				else:
					self["TriggerEfficiencyData"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2016_Electron_Ele25WPTight_eff.root" ]
					self["TriggerEfficiencyMc"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Electron_Ele25WPTight_eff.root" ]

					self["IdentificationEfficiencyData"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2016_Electron_IdIso_IsoLt0p1_eff.root"]
					self["IdentificationEfficiencyMc"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC_Electron_IdIso_IsoLt0p1_eff.root"]

				if re.search("Spring16", nickname):
					self["TriggerEfficiencyMc"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_dummy.root" ]

			if channel == "MT":
				self["TriggerEfficiencyData"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2016_Muon_Mu22OR_eta2p1_eff.root"]
				self["TriggerEfficiencyMc"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Muon_Mu22OR_eta2p1_eff.root"]
				self["IdentificationEfficiencyData"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2016_Muon_IdIso_IsoLt0p15_2016BtoH_eff.root"]
				self["IdentificationEfficiencyMc"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC_Muon_IdIso_IsoLt0p15_2016BtoH_eff.root"]

				if re.search("(Fall15MiniAODv2|Run2015D|Embedding2015)", nickname):
					self["TriggerEfficiencyData"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2015_Muon_IsoMu18_fall15.root"]
					self["TriggerEfficiencyMc"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Muon_IsoMu18_fall15.root"]
					self["IdentificationEfficiencyData"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2015_Muon_IdIso0p1_fall15.root"]
					self["IdentificationEfficiencyMc"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC_Muon_IdIso0p1_fall15.root"]

				elif re.search("Run2017|Summer17|Fall17", nickname):
					# triggerEfficiency_Run2017_Muon_IsoMu24orIsoMu27.root
					# triggerEfficiency_MCFall2017_Muon_IsoMu24orIsoMu27.root
					# triggerEfficiency_Run2017_Muon_IsoMu27.root
					# triggerEfficiency_MCFall2017_Muon_IsoMu27.root
					self["TriggerEfficiencyData"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2017_Muon_IsoMu24orIsoMu27.root"]
					self["TriggerEfficiencyMc"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MCFall2017_Muon_IsoMu24orIsoMu27.root"]

					# identificationEfficiency_Run2017_Muon_IdIso_IsoLt0p15_2017B_eff.root
					# identificationEfficiency_MCFall2017_Muon_IdIso_IsoLt0p15_2017B_eff.root
					self["IdentificationEfficiencyData"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2017_Muon_IdIso_IsoLt0p15_2017B_eff.root"]
					self["IdentificationEfficiencyMc"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MCFall2017_Muon_IdIso_IsoLt0p15_2017B_eff.root"]

				elif re.search("Spring16", nickname):
					self["TriggerEfficiencyMc"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_dummy.root"]

				elif re.search("Run2017|Summer17|Fall17", nickname):
					pass

			if channel == "TT":
				pass

			if channel == "EM":
				if re.search("(Fall15MiniAODv2|Run2015D|Embedding2015)", nickname):
					self["TriggerEfficiencyData"] = [
						"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2015_Electron_Ele12_fall15.root",         	 #2 times 0:... and 1:...
						"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2015_Electron_Ele17_fall15.root",
						"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2015_Muon_Mu8_fall15.root",
						"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2015_Muon_Mu17_fall15.root"
					]

					self["TriggerEfficiencyMc"] = [
						"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Electron_Ele12_fall15.root",
						"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Electron_Ele17_fall15.root",
						"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Muon_Mu8_fall15.root",
						"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Muon_Mu17_fall15.root"
					]

					self["IdentificationEfficiencyData"] = [
						"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2016_Electron_IdIso_IsoLt0p15_eff.root",
						"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2016_Muon_IdIso_IsoLt0p2_2016BtoH_eff.root"
					]
					self["IdentificationEfficiencyMc"] = [
						"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC_Electron_IdIso0p15_fall15.root",
						"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC_Muon_IdIso0p15_fall15.root"
					]

				else:
					self["TriggerEfficiencyData"] = [
						"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2016_Electron_Ele12leg_eff.root",      		 #2 times 0:... and 1:...
						"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2016_Electron_Ele23leg_eff.root",
						"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2016_Muon_Mu8leg_2016BtoH_eff.root",
						"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2016_Muon_Mu23leg_2016BtoH_eff.root"
					]
					self["TriggerEfficiencyMc"] = [
						"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Electron_Ele12leg_eff.root",
						"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Electron_Ele23leg_eff.root",
						"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Muon_Mu8leg_2016BtoH_eff.root",
						"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Muon_Mu23leg_2016BtoH_eff.root"
					]

					self["IdentificationEfficiencyData"] = [
						"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2016_Electron_IdIso_IsoLt0p15_eff.root",
						"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2016_Muon_IdIso_IsoLt0p2_2016BtoH_eff.root"
					]
					self["IdentificationEfficiencyMc"] = [
						"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC_Electron_IdIso_IsoLt0p15_eff.root",
						"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC_Muon_IdIso_IsoLt0p2_2016BtoH_eff.root"
					]

			if channel == "MM":
				if re.search("(Fall15MiniAODv2|Run2015D|Embedding2015)", nickname):
					self["TriggerEfficiencyData"] = [
						"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2015_Muon_Mu8_fall15.root",
						"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2015_Muon_Mu17_fall15.root",
						"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2015_Muon_Mu8_fall15.root",
						"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2015_Muon_Mu17_fall15.root"
					]
					self["TriggerEfficiencyMc"] = [
						"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Muon_Mu8_fall15.root",
						"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Muon_Mu17_fall15.root",
						"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Muon_Mu8_fall15.root",
						"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Muon_Mu17_fall15.root"
					]

					self["IdentificationEfficiencyData"] = [
						"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2015_Muon_IdIso0p15_fall15.root",
						"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2015_Muon_IdIso0p15_fall15.root"
					]
					self["IdentificationEfficiencyMc"] = [
						"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC_Muon_IdIso0p15_fall15.root",
						"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC_Muon_IdIso0p15_fall15.root"
					]

				else:
					#self["TriggerEfficiencyData"] = not given

					self["TriggerEfficiencyMc"] = [
						"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_dummy.root",
						"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_dummy.root",
						"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_dummy.root",
						"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_dummy.root"
					]

					self["IdentificationEfficiencyData"] = [
						"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2016_Muon_IdIso_IsoLt0p15_2016BtoH_eff.root",
						"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2016_Muon_IdIso_IsoLt0p15_2016BtoH_eff.root"
					]
					self["IdentificationEfficiencyMc"] = [
						"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC_Muon_IdIso_IsoLt0p15_2016BtoH_eff.root",
						"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC_Muon_IdIso_IsoLt0p15_2016BtoH_eff.root"
					]

		# return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/ZZTo4L_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext1.root"
		# log.warning("COULD NOT FIND THE SVFIT CACHE FILE")