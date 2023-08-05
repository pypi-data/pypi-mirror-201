
from facts_finder.modifiers import juniper_modifier
from .common import Merged

# ========================================================================================
def add_access_vlan_column(port_mode, vlan):
	if port_mode == 'access':
		return eval(f'{vlan}[0]')
	return ""

# ========================================================================================

class JuniperMerge(Merged):

	def __init__(self, fg, capture_tfsm_file, use_cdp):
		super().__init__(fg, capture_tfsm_file, use_cdp)

	def __call__(self):
		self.get_facts_modifiers()

		self.merged_var_dataframe()			# self.var_df
		self.merged_interfaces_dataframe()	# self.int_df
		# self.merged_vrfs_dataframe()		# self.vrf_df
		self.add_vrf_dataframe()
		self.bgp_dataframe()
		self.ospf_dataframe()

		self.generate_interface_numbers()
		self.split_interface_dataframe()
		self.add_access_vlan_column_on_physical()
		self.add_filters()

	def get_facts_modifiers(self):
		self.pdf_dict = juniper_modifier(self.capture_tfsm_file)

	def add_access_vlan_column_on_physical(self):
		physical_int_df = self.int_dfs['physical']
		physical_int_df['access_vlan'] = physical_int_df.apply(lambda x: add_access_vlan_column(x['port_mode'], x['vlan']), axis=1)

	def add_vrf_dataframe(self):
		fg_df = self.Fg['vrf'].reset_index()										## facts-gen dataframe
		fg_df.drop(fg_df[fg_df["vrf"] == "Mgmt-vrf"].index, axis=0, inplace=True)	## Remove row with management vrfs ( add more description for mgmt vrf )
		self.vrf_df = fg_df
		self['vrf'] = fg_df

