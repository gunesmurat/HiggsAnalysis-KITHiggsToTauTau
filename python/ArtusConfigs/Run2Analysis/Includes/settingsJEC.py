# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re


class JEC(dict):
	def __init__(self, nickname):
		if re.search("(Summer17)",nickname):
			self["JetEnergyCorrectionUncertaintyParameters"] = ""
		elif re.search("(Fall17|Run2017)", nickname): #this is recomended in https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2017#%20Jet/MET%20uncertainty%20treatment
			self["JetEnergyCorrectionUncertaintyParameters"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/Fall17_17Nov2017F_V6_DATA_UncertaintySources_AK4PFchs.txt"

			"""
			#from https://twiki.cern.ch/twiki/bin/viewauth/CMS/JECDataMC
		elif re.search("(Fall17)", nickname):
			self["JetEnergyCorrectionUncertaintyParameters"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/Fall17_17Nov2017_V6_MC_UncertaintySources_AK4PFchs.txt"
		elif re.search("(Run2017B)", nickname):
			self["JetEnergyCorrectionUncertaintyParameters"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/Fall17_17Nov2017B_V6_DATA_UncertaintySources_AK4PFchs.txt"
		elif re.search("(Run2017C)", nickname):
			self["JetEnergyCorrectionUncertaintyParameters"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/Fall17_17Nov2017C_V6_DATA_UncertaintySources_AK4PFchs.txt"
		elif re.search("(Run2017D)", nickname):
			self["JetEnergyCorrectionUncertaintyParameters"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/Fall17_17Nov2017D_V6_DATA_UncertaintySources_AK4PFchs.txt"
		elif re.search("(Run2017E)", nickname):
			self["JetEnergyCorrectionUncertaintyParameters"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/Fall17_17Nov2017E_V6_DATA_UncertaintySources_AK4PFchs.txt"
		elif re.search("(Run2017F)", nickname):
			self["JetEnergyCorrectionUncertaintyParameters"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/Fall17_17Nov2017F_V6_DATA_UncertaintySources_AK4PFchs.txt"
			"""
		elif re.search("(Run2016|Spring16|Summer16)", nickname):
			self["JetEnergyCorrectionUncertaintyParameters"] =  "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Summer16/Summer16_23Sep2016V4_DATA_UncertaintySources_AK4PFchs.txt"
		#elif re.search("Run2016|Embedding2016", nickname):
		#	self["JetEnergyCorrectionUncertaintyParameters"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Summer16/Summer16_23Sep2016V4_DATA_Uncertainty_AK4PFchs.txt"
		elif re.search("(Fall15MiniAODv2)", nickname):
			self["JetEnergyCorrectionUncertaintyParameters"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall15/Fall15_25nsV2_MC_Uncertainty_AK4PFchs.txt"
		elif re.search("(Run2015|Embedding2015)", nickname):
			self["JetEnergyCorrectionUncertaintyParameters"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall15/Fall15_25nsV2_DATA_Uncertainty_AK4PFchs.txt"
		
		self["JetEnergyCorrectionUncertaintySource"] = "Total"
		#self["JetEnergyCorrectionUncertaintyShift"] = 0.0
		
		#All commented out
		"""
		if re.search("Run2015|Embedding2016", nickname):
			self["JetEnergyCorrectionParameters"] = [
				"#$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall15/Fall15_25nsV2_DATA_L1FastJet_AK4PFchs.txt",
				"#$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall15/Fall15_25nsV2_DATA_L2Relative_AK4PFchs.txt",
				"#$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall15/Fall15_25nsV2_DATA_L3Absolute_AK4PFchs.txt",
				"#$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall15/Fall15_25nsV2_DATA_L2L3Residual_AK4PFchs.txt"
			]

		else:
			self["JetEnergyCorrectionParameters"] = [
				"#$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall15/Fall15_25nsV2_MC_L1FastJet_AK4PFchs.txt",
				"#$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall15/Fall15_25nsV2_MC_L2Relative_AK4PFchs.txt",
				"#$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall15/Fall15_25nsV2_MC_L3Absolute_AK4PFchs.txt"
			]
		"""

