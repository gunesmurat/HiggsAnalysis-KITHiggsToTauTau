# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import json
import Artus.Utility.jsonTools as jsonTools
import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz
import copy

class Jet_ID(dict):
	def __init__(self, nickname):
		self["JetID"] = "loose"
		self["JetIDVersion"] = "2015"

		self["PuJetIDs"] = []
		self["PuJetIDFullDiscrName"] = "pileupJetIdfullDiscriminant"
		self["JetTaggerLowerCuts"] = []
		self["JetTaggerUpperCuts"] = []
	
		self["JetLowerPtCuts"] = ["20.0"]
		self["JetUpperAbsEtaCuts"] = ["4.7"]
	
		self["JetLeptonLowerDeltaRCut"] = 0.5
