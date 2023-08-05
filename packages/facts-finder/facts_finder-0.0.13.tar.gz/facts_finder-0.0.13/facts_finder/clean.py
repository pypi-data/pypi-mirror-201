
import os
from nettoolkit import *
from pathlib import *

from .generators import FactsGen
from .generators.cisco_parser import get_op_cisco
from .mergers import CiscoMerge, JuniperMerge

# ========================================================================================

class CleanFacts:
	"""cleans the captured parsed file and writes out the modified facts in new clean file
	using additional information provided from capture log file.
	Also can get a few additional properties to process futher. A new clean file will be 
	generated upon instance calling."""

	def __init__(self,
		capture_log_file, 
		capture_parsed_file,
		new_suffix='-clean',
		use_cdp=False,
		debug=False,
		):
		self.capture_log_file = capture_log_file
		self.capture_parsed_file = capture_parsed_file
		self.new_suffix = new_suffix
		self.use_cdp = use_cdp
		self.debug = debug
		self._clean_file = get_clean_filename(self.capture_parsed_file, self.new_suffix)
		if debug:
			self._fg_data_file = get_clean_filename(self.capture_parsed_file, "-fg")
			self._fm_data_file = get_clean_filename(self.capture_parsed_file, "-fm")

	def __call__(self):
		self.get_facts_gen()
		self.call(self.merge_class())
		remove_file(self.clean_file)
		write_to_xl(self.clean_file, self.Mc.merged_dict, overwrite=True)
		if self.debug:
			write_to_xl(self._fg_data_file, self.Mc.fg_merged_dict, overwrite=True)
			write_to_xl(self._fm_data_file, self.Mc.pdf_dict, overwrite=True)

	def get_facts_gen(self):
		"""gets Facts from generators """
		self.Fg = FactsGen(self.capture_log_file)
		self.Fg()

	def merge_class(self):
		""" returns Modifier Merge Class from the generated Facts """
		if self.Fg.dev_type == 'cisco':
			MergeClass = CiscoMerge
			self._config = cisco_config(self.capture_log_file)
		elif self.Fg.dev_type == 'juniper':
			MergeClass = JuniperMerge
			self._config = juniper_config(self.capture_log_file)
		else:
			raise Exception(f"undetected device type {self.Fg.dev_type}, cannot proceed")
		return MergeClass

	def call(self, MergeClass):
		""" calls the modifier merge class """
		self.Mc = MergeClass(self.Fg, self.capture_parsed_file, self.use_cdp)
		self.Mc()

	@property
	def clean_file(self):
		"""new output clean filename """
		return self._clean_file

	@property
	def hostname(self):
		"""device hostname"""
		return self.Mc.hostname

	@property
	def config(self):
		"""device configuration.  for cisco show running, for juniper show configuration - set output"""
		return self._config

	@property
	def dev_type(self):
		"""device type string either(cisco/juniper)"""
		return self.Fg.dev_type		

# ========================================================================================

def get_clean_filename(file, suffix):
	"""get a new clened filename appended with suffix string"""
	p = Path(file)
	filename_wo_ext = str(p.stem)
	file_ext = str(p.suffix)
	cur_folder = str(p.resolve().parents[0])
	return cur_folder+"/"+filename_wo_ext+suffix+file_ext


def remove_file(xl):
	"""try to remove file if available, skip else"""
	try: os.remove(xl)			# remove old file if any
	except: pass


def cisco_config(capture_log_file):
	"""returns cisco running configuration """
	config = get_op_cisco(capture_log_file, 'show running-config')
	return config


def juniper_config(capture_log_file):
	"""returns juniper configuration in set commnand output """
	cmd_op = get_op(capture_log_file, 'show configuration')
	JS = JSet(input_list=cmd_op)
	JS.to_set
	config = verifid_output(JS.output)
	return config

# ========================================================================================
