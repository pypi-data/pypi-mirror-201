
from facts_finder.modifiers import cisco_modifier
from .common import Merged

# ========================================================================================

class CiscoMerge(Merged):

	def __init__(self, fg, capture_tfsm_file, use_cdp):
		super().__init__(fg, capture_tfsm_file, use_cdp)

	def __call__(self):
		self.get_facts_modifiers()

		self.merged_var_dataframe()			# self.var_df
		self.merged_interfaces_dataframe()	# self.int_df
		self.merged_vrfs_dataframe()		# self.vrf_df
		self.bgp_dataframe()
		self.ospf_dataframe()

		self.generate_interface_numbers()
		self.split_interface_dataframe()
		self.add_filters()

		self.add_fg_dfs()

	def get_facts_modifiers(self):
		self.pdf_dict = cisco_modifier(self.capture_tfsm_file, use_cdp=self.use_cdp)


	def add_fg_dfs(self):
		self.fg_merged_dict = {
			'var': self.fg_var_df,
			'interface': self.fg_int_df,
			'vrf': self.fg_vrf_df,
			'bgp': self.fg_bgp_df,
		}