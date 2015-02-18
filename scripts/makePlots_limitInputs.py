#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import os
import shlex

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gErrorIgnoreLevel = ROOT.kError
from HiggsAnalysis.HiggsToTauTau.utils import parseArgs

import Artus.Utility.jsonTools as jsonTools
import Artus.Utility.tools as tools

import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.mt as mt
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.quantities as quantities
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.systematics as systematics
import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot



if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Make Data-MC control plots.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-i", "--input-dir", required=True,
	                    help="Input directory.")
	parser.add_argument("-o", "--root-output", default="htt.inputs-sm-8TeV.root",
	                    help="Merged ROOT output. [Default: %(default)s]")
	parser.add_argument("--channels", nargs="*",
	                    default=["mt"], choices=["mt"],
	                    #default=["tt", "mt", "et", "em", "mm", "ee"], # other channels currently not supported
	                    help="Channels. [Default: %(default)s]")
	parser.add_argument("--categories", nargs="*",
	                    default=["0JetMedium", "0JetHigh", "1JetMedium", "1JetHigh", "1JetHighBoost", "2JetVbfLoose", "2JetVbfTight"],
	                    help="Categories. [Default: %(default)s]")
	parser.add_argument("--quantities", nargs="*",
	                    default=["inclusive", "m_ll", "svitMass"],
	                    help="Quantities. [Default: %(default)s]")
	parser.add_argument("-m", "--higgs-masses", nargs="+", default=["110_145:5"],
	                    help="Higgs masses. [Default: %(default)s]")
	parser.add_argument("--tau-es-shifts", nargs="+", type=float, default=[1.0, -1.0],
	                    help="Tau ES shifts. [Default: %(default)s]")
	parser.add_argument("--svfit-mass-shifts", nargs="+", type=float, default=[1.0, -1.0],
	                    help="Svfit mass shifts. [Default: %(default)s]")
	parser.add_argument("-a", "--args", default="--plot-modules ExportRoot PlotRootHtt",
	                    help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
	                    help="Number of (parallel) processes. [Default: %(default)s]")

	args = vars(parser.parse_args())
	logger.initLogger(args)
	args["higgs_masses"] = parseArgs(args["higgs_masses"])
	
	channel_renamings = {
		#"mt" : "muTau",
	}
	category_renamings = {
		"0Jet" : "0jet",
		"0JetLow" : "0jet_low",
		"0JetMedium" : "0jet_medium",
		"0JetHigh" : "0jet_high",
		"1Jet" : "1jet",
		"1JetLow" : "1jet_low",
		"1JetMedium" : "1jet_medium",
		"1JetHigh" : "1jet_high_lowhiggs",
		"1JetHighBoost" : "1jet_high_mediumhiggs",
		"1JetHighLargeBoost" : "1jet_high_highhiggs",
		"2Jet" : "vbf",
		"2JetVbfLoose" : "vbf_loose",
		"2JetVbfTight" : "vbf_tight",
	}
	label_renamings = {
		"Data" : "data_obs",
		"WJets" : "W",
		"TTJ" : "TT",
		"VBF90" : "qqH90",
		"VBF95" : "qqH95",
		"VBF100" : "qqH100",
		"VBF105" : "qqH105",
		"VBF110" : "qqH110",
		"VBF115" : "qqH115",
		"VBF120" : "qqH120",
		"VBF125" : "qqH125",
		"VBF130" : "qqH130",
		"VBF135" : "qqH135",
		"VBF140" : "qqH140",
		"VBF145" : "qqH145",
		"VBF150" : "qqH150",
		"VBF155" : "qqH155",
		"VBF160" : "qqH160",
	}
	
	harry_configs = []
	harry_args = []
	
	systematic_shifts = [(systematics.Nominal, "", 0.0)]
	systematic_shifts += [(systematics.TauEsSystematic, "CMS_scale_t_%s_8TeV", shift) for shift in args["tau_es_shifts"] if shift != 0.0]
	systematic_shifts += [(systematics.SvfitMassSystematic, "CMS_htt_ZLScale_%s_8TeV", shift) for shift in args["svfit_mass_shifts"] if shift != 0.0]
	
	for uncertainty, name, shift in systematic_shifts:
		
		for channel in args["channels"]:
			if "%s" in name:
				name = name % channel_renamings.get(channel, channel)
		
			channel_settings = mt.MT(add_data=uncertainty.add_data(),
			                         add_ztt=uncertainty.add_ztt(),
			                         add_zl=uncertainty.add_zl(),
			                         add_zj=uncertainty.add_zj(),
			                         add_ttj=uncertainty.add_ttj(),
			                         add_diboson=uncertainty.add_vv(),
			                         add_wjets=uncertainty.add_wjets(),
			                         add_qcd=uncertainty.add_qcd(),
			                         add_ggh_signal=args["higgs_masses"] if uncertainty.add_ggh() else [],
			                         add_vbf_signal=args["higgs_masses"] if uncertainty.add_qqh() else [],
			                         add_vh_signal=args["higgs_masses"] if uncertainty.add_vh() else [],
			                         normalise_signal_one_pb=True) if channel == "mt" else None
			
			for category in args["categories"]:
				if category == "None":
					category = None
			
				config = channel_settings.get_config(category=category) if channel == "mt" else jsonTools.JsonDict()
			
				for quantity in args["quantities"]:
					json_exists = True
					json_configs = [
						os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/control_plots/%s_%s.json" % (channel, quantity)),
						os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/samples/complete/%s.json" % (channel))
					] if channel != "mt" else [os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/control_plots/%s_%s.json" % (channel, quantity))]
					if not os.path.exists(json_configs[0]):
						json_exists = False
						json_configs[0] = os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/sync_exercise/%s_default.json" % (channel))
					json_defaults = jsonTools.JsonDict([os.path.expandvars(json_file) for json_file in json_configs]).doIncludes().doComments()
					if channel == "mt":
						json_defaults += config
				
					if not category is None:
						json_defaults["output_dir"] = os.path.join(json_defaults.setdefault("output_dir", "plots"), category)
			
					for index, label in enumerate(json_defaults.setdefault("labels", [])):
						json_defaults["labels"][index] = os.path.join("%s_%s" % (channel_renamings.get(channel, channel),
							                                                     category_renamings.get(category, category)),
							                                          label_renamings.get(label, label))
					
					json_defaults = uncertainty(json_defaults, name).get_config(shift)
					
					if quantity == "m_ll":
						json_defaults = quantities.VisibleMass(json_defaults).get_config(channel, category)
					if quantity == "svitMass":
						json_defaults = quantities.VisibleMass(json_defaults).get_config(channel, category)
					
					if "PrintInfos" in json_defaults.get("analysis_modules", []):
						json_defaults.get("analysis_modules", []).remove("PrintInfos")
					
					harry_configs.append(json_defaults)
					harry_args.append("-d %s %s --formats png pdf %s" % (args["input_dir"], ("" if json_exists else ("-x %s" % quantity)), args["args"]))
			
	higgs_plotter = higgsplot.HiggsPlotter(list_of_config_dicts=harry_configs, list_of_args_strings=harry_args, n_processes=args["n_processes"])
	
	root_outputs = list(set([output for output in tools.flattenList(higgs_plotter.output_filenames) if output.endswith(".root")]))
	logger.subprocessCall(shlex.split("hadd -f %s %s" % (args["root_output"], " ".join(root_outputs))))
	log.info("Merged ROOT output is saved to \"%s\"." % args["root_output"])

