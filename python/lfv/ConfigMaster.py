import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2016 as samples
import Artus.Utility.jsonTools as jsonTools

### Enumeration class for possible plotting/analysis modules

class Plotmodule():
	control_plot = 0
	sum_of_hists = 1
	efficiency_plot = 2
	shape_plot = 3
	datacard = 4

### Class to create harry plotter configs for your special desire. All configs are safed as dictionaries and can be combined to the final config which is needed	

class ConfigMaster(object):

	##Constructor for loading sample information from samples_run2_2016.py

	def __init__(self, base_values, sample_values):

		###Config which is initiliazed with information for each sample from samples_run2_201X.py if wished
		if sample_values != None:
			sample_settings = samples.Samples()	
			sample_list, channel, category, estimationMethod, cut_type, nick_suffix, no_plot, weight = sample_values

		self._config = 0
		sample_settings = samples.Samples()
	
		sample_list, channel, category, no_plot, nick_suffix, weight = sample_values
		self._config = sample_settings.get_config(samples=[getattr(samples.Samples, sample) for sample in sample_list], channel = channel, category = category, no_plot = no_plot, nick_suffix = nick_suffix, weight = weight)

		###Fill config with basic information

		for (key, value) in self.__base__(*base_values).iteritems():
			self._config[key] = value


		###Dictionary with all possible plotting/analysis modules

		self._modules_dict = {
					Plotmodule.control_plot:		self.__controlplot__,
					Plotmodule.sum_of_hists:		self.__sumofhists__,
					Plotmodule.efficiency_plot:		self.__efficiencyplot__,
					Plotmodule.shape_plot:			self.__shapeplot__,
					Plotmodule.datacard:			self.__datacard__
		}

	
	###Dictionaries for information for each plotting/analysis modules

	def __base__(self, input_dir, output_dir, formats, www_nodate, www, x_expressions, x_bins, output_file, title, cms, text):

	
		self._base = {
					"directories":			input_dir,
					"output_dir":			output_dir,
					"filename":			output_file,
					"formats":			formats,
					"www":				www,
					"www_nodate":			www_nodate,
					
					"x_expressions":		x_expressions,
					"x_bins":			x_bins,


					"filename":			output_file,
					"title":			title,
					"cms":				cms,
					"extra_text":			text,	

		}

		return self._base

		
	def __controlplot__(self, x_label, legend, lumis, energies, year, www):
		
		self._controlplot = {
					"x_label":			x_label,
					"legend":			legend,
					"lumis"	:			lumis,
					"energies":			energies,
					"year":				year,
					"www":				www
		}

		return self._controlplot


	def __sumofhists__(self, analysis_mod, sum_nicks, result_nicks):
	
		self._sumofhists = {
					"analysis_modules":		analysis_mod,
					"sum_nicks":			sum_nicks,
					"sum_result_nicks":		result_nicks
		}

		return self._sumofhists

	def __efficiencyplot__(self, analysis_mod, bkg_nicks, markers, y_label, cut_modes, sig_nicks, cut_nicks, whitelist, lower_cut):
		
		self._efficiencyplot = {
					"analysis_modules":		analysis_mod,
					"output_dir":			output_dir,
					"cut_efficiency_bkg_nicks":	bkg_nicks,
					"cut_efficiency_sig_nicks":	sig_nicks,
					"cut_efficiency_nicks":		cut_nicks,
					"cut_efficiency_modes":		cut_modes,
					"nicks_whitelist":		whitelist,
					"markers":			markers,
					"y_label":			y_label,
					"select_lower_values":		lower_cut,
		}

		return self._efficiencyplot

	def __shapeplot__(self, y_label, analysis_mod):
		
		self._shapeplot = {
					"y_label":			y_label,
					"analysis_modules":		analysis_mod					
		}

		return self._shapeplot

	def __datacard__(self, labels, plot_modules, file_mode):

		self._datacard = {
					"labels":			labels,
					"plot_modules":			plot_modules,
					"file_mode":			file_mode
		}

		return self._datacard

	###Function for adding information to the config

	def add_config_info(self, module_values, module):
		
		###Fill config will all module information checking if values are already avaible as list or string
		for (key, value) in self._modules_dict[module](*module_values).iteritems():
			try:
				self._config[key].append(value)

			except AttributeError:
				self._config[key] += value

			except KeyError:
				self._config[key] = value

	###Returns build config
			
	def return_config(self):
		return self._config

