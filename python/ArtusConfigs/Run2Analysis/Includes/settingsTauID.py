# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import json
import Artus.Utility.jsonTools as jsonTools
import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz
import copy

class Tau_ID(dict):
	def __init__(self, nickname):
		#doppelgemoppel allready in the config class
		self.datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz("Kappa/Skimming/data/datasets.json") 
		self["TauID_documentation"] = []

		self["TauDiscriminatorIsolationName"] = "byIsolationMVArun2v1DBoldDMwLTraw"

		self["TauElectronLowerDeltaRCut"] = -1.0
		self["TauMuonLowerDeltaRCut"] = -1.0
