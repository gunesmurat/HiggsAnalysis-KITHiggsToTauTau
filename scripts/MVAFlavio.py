#! /usr/bin/env python

import ROOT
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.cutstrings as cuts 

from multiprocessing import Pool,  cpu_count
import argparse
import array
from math import cos, sin, acos, fabs

##Define constants
version = 2
sample_dir = "/net/scratch_cms3b/brunner/artus/AllSamples/merged/"
tree_name = "{channel}_nominal/ntuple"
input_file = "$CMSSW_BASE/src/plots/FlavioOutput/MVA_trees_{sample_type}{cut_label}_{channel}.root"
output_root = "$CMSSW_BASE/src/plots/FlavioOutput/output" + str(version) + "{cut_label}_{channel}.root"

sig_list = ["zem"]
bkg_list = ["ztt", "zll", "ttj", "vv", "wj"]
parameter = ["deltaPhi_ll:= acos(cos(phi_1)*cos(phi_2) + sin(phi_1)*sin(phi_2))", "deltaPhi_l1met:= acos(cos(metphi)*cos(phi_1) + sin(metphi)*sin(phi_1))", "deltaPhi_l2met:= acos(cos(metphi)*cos(phi_2) + sin(metphi)*sin(phi_2))", "abs(d0_1)", "abs(d0_2)", "pt_1", "pt_2", "ptvis", "met", "mt_2"] #,"m_vis"]
#parameter = ["deltaPhi_ll:= acos(cos(phi_1)*cos(phi_2) + sin(phi_1)*sin(phi_2))", "pt_1", "pt_2", "ptvis", "m_vis", "met"]

user_def_parameter = {
			0:	[lambda phi_1, phi_2: acos(cos(phi_1)*cos(phi_2) + sin(phi_1)*sin(phi_2)), ["phi_1", "phi_2"]],
			1:	[lambda phi_1, phi_2: acos(cos(phi_1)*cos(phi_2) + sin(phi_1)*sin(phi_2)), ["metphi", "phi_1"]],
			2:	[lambda phi_1, phi_2: acos(cos(phi_1)*cos(phi_2) + sin(phi_1)*sin(phi_2)), ["metphi", "phi_2"]],
			3:	[lambda d0_1: abs(d0_1), ["d0_1"]],
			4:	[lambda d0_2: abs(d0_2), ["d0_2"]],
}
	

##Argument parser
def parser():
	parser = argparse.ArgumentParser(description = "Script for using TMVA method in LFV analysis", formatter_class=argparse.RawTextHelpFormatter)

	parser.add_argument("--create-input-trees", action = "store_true", default = False, help = "Do the splitting of background and signal samples into even and odd event number sample")
	parser.add_argument("--training", action = "store_true", default = False, help = "Do the training on the background/signal samples")
	parser.add_argument("--application", action = "store_true", default = False, help = "Use the trained BDT3 to apply on background/data and append it in the ROOT files")
	parser.add_argument("--file-attach", action = "store", help = "Attach BDT score in ROOT File. Calling --application call this option for all files and submit it to the batch system.")
	parser.add_argument("--results", action = "store", help = "Give .xml or .root output from TMVA to show results with the TMVA GUI")

	return parser.parse_args()
	

##Create input trees for BDT method, splitting signal and background events for each channel in even and odd event numbered
def create_input_trees():
	import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2016 as samples
	import glob
	
	sample_settings = samples.Samples()
	mc_list = []

	##Get file names using samples_run2_2016
	for sample_list in [sig_list, bkg_list]:
		mc_set = set()
		config = sample_settings.get_config(samples=[getattr(samples.Samples, sample) for sample in sample_list], channel = "em", category = None, cut_type = "lfv")
		mc_set.update([glob.glob(sample_dir + mc_name)[0] for mc_name in [file_name for file_list in [config_string.split(" ") for config_string in config["files"]] for file_name in file_list]])
		mc_list.append(list(mc_set))

	for channel in ["em", "et", "mt"]:
		##Create signal/background chain and read in all files
		sig_chain = ROOT.TChain(tree_name.format(channel = channel))
		bkg_chain = ROOT.TChain(tree_name.format(channel = channel))

		for sig_file in mc_list[0]:
			sig_chain.Add(sig_file)

		for bkg_file in mc_list[1]:
			bkg_chain.Add(bkg_file)

		##Deactivate branches, which are not avaiable in all files
		invalid_branch = ["genBosonLV", "genBosonLep1LV", "genBosonLep2LV", "genBosonTau1LV", "genBosonTau2LV", "genBosonTau1VisibleLV", "genBosonTau2VisibleLV"]
	
		for branch in invalid_branch:
			sig_chain.SetBranchStatus(branch, 0)
			bkg_chain.SetBranchStatus(branch, 0)
	
		##Create input root files in paralell
		pool = Pool(4)
		pool.map(write_root_file, [[sig_chain, "event%2==0", "sig", channel], [sig_chain, "event%2==1", "sig", channel], [bkg_chain, "event%2==0", "bkg", channel], [bkg_chain, "event%2==1", "bkg", channel]])


##Function writing root files in paralell
def write_root_file(args):
	chain, cut, sample_type, channel = args

	new_file = ROOT.TFile(input_file.format(sample_type = sample_type, cut_label = "A" if cut == "event%2==0" else "B", channel=channel), "RECREATE")
	splitted_tree = chain.CopyTree(cut)
	splitted_tree.SetName(channel)
	splitted_tree.Write()
	new_file.Close()

	print "The input file " + input_file.format(sample_type = sample_type, cut_label = "A" if cut == "event%2==0" else "B", channel=channel) + " is written."


##Do the training/evaluaton for the splitted samples for each channel
def training():
	##Config arguments for do_training function
	pool = Pool(cpu_count())
		
	for channel in ["em", "et", "mt"]:
		config_A = [channel, "A"]
		config_B = [channel, "B"]
		sub_config = []

		for sample_type, cut_label in zip(["sig", "sig", "bkg", "bkg"], ["A", "B", "A", "B"]):
			sub_config.append(input_file.format(sample_type = sample_type, cut_label = cut_label, channel=channel))
			
		pool.apply_async(do_training, args = (config_A + sub_config,))

		for i, j in [[0,1], [2, 3]]:
			sub_config[i], sub_config[j] = sub_config[j], sub_config[i] 
		
		pool.apply_async(do_training, args = (config_B + sub_config,))

	pool.close()
	pool.join()
					

##Function for doing the training in parelell
def do_training(args):
	##Retrieve arguments
	channel, cut_label, sig_train, sig_test, bkg_train, bkg_test = args

	##Get the input trees
	file_sig_train = ROOT.TFile(sig_train, "READ")
	tree_sig_train = ROOT.TTree()
	file_sig_train.GetObject(channel, tree_sig_train)

	file_sig_test = ROOT.TFile(sig_test, "READ")
	tree_sig_test = ROOT.TTree()
	file_sig_test.GetObject(channel, tree_sig_test)

	file_bkg_train = ROOT.TFile(bkg_train, "READ")
	tree_bkg_train = ROOT.TTree()
	file_bkg_train.GetObject(channel, tree_bkg_train)

	file_bkg_test = ROOT.TFile(bkg_test, "READ")
	tree_bkg_test = ROOT.TTree()
	file_bkg_test.GetObject(channel, tree_bkg_test)

	##Create output file
	output = ROOT.TFile(output_root.format(channel=channel, cut_label = cut_label), "RECREATE")
	factory = ROOT.TMVA.Factory("BDT{version}_".format(version=version) + channel + "_" + cut_label, output)

	##Add signal/background trees
	factory.AddSignalTree(tree_sig_train, 1., "Training")
	factory.AddSignalTree(tree_sig_test, 1., "Testing")
	factory.AddBackgroundTree(tree_bkg_train, 1., "Training")
	factory.AddBackgroundTree(tree_bkg_test, 1., "Testing")

	##Get baseline selection	
	weights = ""
	
	for index, weight in enumerate(cuts.CutStringsDict().baseline(channel, "").values()[1:]):
		weights = weights + "*" if index != 0 else weights
		weights += weight

	##Set signal/background event weights
	factory.SetSignalWeightExpression("jetCorrectionWeight")
	factory.SetBackgroundWeightExpression(weights)

	##Add parameter for training
	for param in parameter:
		factory.AddVariable(param)

	##Configure everything
	sig_cut = ROOT.TCut("")
	bkg_cut = ROOT.TCut("")
	n_option =  ROOT.TString("") #ROOT.TString("nTrain_Signal=100000:nTest_Signal=100000:nTrain_Background=100000:nTest_Background=100000:SplitMode=Random",)
 
	factory.PrepareTrainingAndTestTree(sig_cut, bkg_cut, n_option)
	factory.BookMethod(ROOT.TMVA.Types.kBDT, "BDT", "!H:!V:NTrees=500:MinNodeSize=2.5%:MaxDepth=10:BoostType=AdaBoost:AdaBoostBeta=0.5:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20")
	#factory.BookMethod(ROOT.TMVA.Types.kMLP, "MLP", "H:!V:NeuronType=tanh:VarTransform=N:NCycles=500:HiddenLayers=N+10,N+2,N+2:TestRate=5:!UseRegulator:LearningRate=0.05:EstimatorType=CE")

	##Run the training/evulation
	factory.TrainAllMethods()
	factory.TestAllMethods()
	factory.EvaluateAllMethods()
	output.Close()


##Function for creating grid control for the application of the BDT score
def application():
	import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2016 as samples
	import glob
	import ConfigParser
	import os
	from random import uniform
	
	sample_settings = samples.Samples()
	mc_list = []
	mc_set = set()

	##Get file names using samples_run2_2016
	for sample_list in [["data"], bkg_list, sig_list]:
		for channel in ["em", "et", "mt"]:
			config = sample_settings.get_config(samples=[getattr(samples.Samples, sample) for sample in sample_list], channel = channel, category = None, cut_type = "lfv")
			mc_set.update([glob.glob(sample_dir + mc_name)[0] for mc_name in [file_name for file_list in [config_string.split(" ") for config_string in config["files"]] for file_name in file_list]])
			
	for file_name in list(mc_set):			
		mc_list.append(file_name)

	##Write bash script for grid control

	##Write config for grid control

	local = True

	if not local:
		#Send jobs to the batch system
		os.system("go.py {config_name}".format(config_name = config_name))
		os.system("rm config*.cfg")
		seed = str(int(uniform(1, 10000)))
	
		Config = ConfigParser.ConfigParser()
		Config.optionxform = str
		config_name = "config" + seed + ".cfg"
		config = open(config_name, "w")

		sections = ["global", "jobs", "UserTask", "parameters"]
		entries = [
				[("task", "UserTask"), ("backend", "condor"), ("cmdargs", "-c -G"), ("workdir create", True), ("workdir", "/tmp/Flavio_work" + seed)],
				[("wall time", "1:00"), ("max retry", 5)],
				[("executable", "kappa.sh")],
				[("parameters", "FILE_NAME"), ("FILE_NAME", " ".join(mc_list))]
		]
	
		for section in sections: 	
			Config.add_section(section)

		for section, entry in zip(sections, entries):
			for key, value in entry:
				Config.set(section, key, value)

		Config.write(config)
		config.close()
	
	else:
		pool = Pool(cpu_count())

		for filename in mc_list:
			pool.apply_async(attach, args = (filename,))

		pool.close()
		pool.join()

##Function for attaching BDT score on root file
def attach(file_name):
	print "File which is processed: " + file_name

	##Prepare input variables and BDT_score variable
	variables = [array.array("f", [0]) for param in parameter]
	BDT_score = array.array("f", [0])

	root_file = ROOT.TFile(file_name, "UPDATE")
	list_of_keys = [key.GetName() for key in root_file.GetListOfKeys()]
	root_file.Close()

	
	##Set up TMVA reader method
	reader = ROOT.TMVA.Reader()		
	for param, variable in zip(parameter, variables):
		reader.AddVariable(param, variable)

	for channel in ["em", "et", "mt"]:
		method_A = "BDT{version}_A_{channel}".format(channel=channel, version=version)
		method_B = "BDT{version}_B_{channel}".format(channel=channel, version=version)
		
		reader.BookMVA(method_A, "/.automount/home/home__home2/institut_3b/brunner/analysis/master/CMSSW_8_1_0/src/weights/BDT{version}_{channel}_A_BDT.weights.xml".format(channel = channel, version=version))
		reader.BookMVA(method_B, "/.automount/home/home__home2/institut_3b/brunner/analysis/master/CMSSW_8_1_0/src/weights/BDT{version}_{channel}_B_BDT.weights.xml".format(channel = channel, version=version))
		
		for key in list_of_keys:
			if channel in key[:2]:
				root_file = ROOT.TFile(file_name, "UPDATE")
				tree = root_file.Get(key + "/ntuple")
				print "Channel which is evaluated: {key}".format(key = key)
	
				##Delete branch with BDT_score if already there
				if tree.GetLeaf("BDT{version}_score".format(version=version)):	
					tree.GetListOfLeaves().Remove(tree.GetLeaf("BDT{version}_score".format(version=version)))
					tree.GetListOfBranches().Remove(tree.GetBranch("BDT{version}_score".format(version=version)))

				##Create (new) branch for BDT_score and fill it
				branch = tree.Branch("BDT{version}_score".format(version=version), BDT_score, "BDT{version}_score/F".format(version=version))
				index = 0

				for index, event in enumerate(tree):
					for index2, (param, variable) in enumerate(zip(parameter, variables)):
						##Try to get value for variable from tree, if it is user defined, the function in the constant section will be used
						try:
							variable[0] = getattr(event, param)
		
						except AttributeError:
							user_func, params = user_def_parameter[index2]

							try:
								variable[0] = user_func(*[getattr(event, param_string) for param_string in params]) 
							
							except:
								variable[0] = -999

					##Get score for event/odd event and fill the branch
					if event.event % 2 == 0:
						BDT_score[0] = reader.EvaluateMVA(method_B)
	
					if event.event % 2 == 1:
						BDT_score[0] = reader.EvaluateMVA(method_A)

					if index % 10000 == 0:
						print "Number of events evaluated: {index}".format(index = index)
 
					branch.Fill()
	
				##Overwrite old tree and close file
				root_file.cd(key)
				tree.Write("", ROOT.TObject.kOverwrite)
				root_file.Close()
				print "Number of events evaluated in total: {index}".format(index = index)
				print "BDT score was sucessfully applied in tree: " + key + "/ntuple"



##Use TMVA Gui to show trainings results
def show_results(file_name):
	ROOT.TMVA.TMVAGui(file_name)
	raw_input("Press Enter to exit")
			

def main():
	args = parser()

	if(args.create_input_trees):
		create_input_trees()

	if(args.training):	
		training()

	if(args.application):
		application()

	if(args.file_attach):
		attach(args.file_attach)

	if(args.results):
		show_results(args.results)


if __name__ == "__main__":		
	main()