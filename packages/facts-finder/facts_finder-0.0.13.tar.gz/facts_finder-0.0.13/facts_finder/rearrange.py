
import pandas as pd
from nettoolkit import *

# =====================================================================================================

IF_PROPS = {
	1: ["filter", "interface", "int_number",  ],
	2: [ "link_status", "protocol_status", "speed", "duplex", "media_type", ],
	3: ["nbr_dev_type", "nbr_hostname", "nbr_ip", "nbr_platform", "nbr_serial", "nbr_vlan", "nbr_interface",],
	4: ["switchport", "admin_mode", "switchport_negotiation", "interface_mode", "access_vlan", "voice_vlan", 
		"native_vlan", "vlan_members",],
	5: ["subnet", "h4block", "v4_helpers", "v6_helpers", ],
	6: ["ospf_auth", "ospf_auth_type",],
	7: ["intvrf", "channel_group_interface", "channel_grp", "channel_group_mode"],
	8: ["description",  "int_filter", ],
	9:["int_udld",],
	10: [],
}

BGP_PROPS = [ 
	"filter", "bgp neighbor", "bgp_vrf", "address-family", "bgp_peergrp", "bgp_peer_description", "bgp_peer_password", 
	"bgp_peer_ip", "bgp_peer_as", "local-as", "update-source", "route-map in", "route-map out", "unsuppress-map",
]

VRF_PROPS = [
	"filter", "vrf", "protocols", "default_rd", "vrf_route_target", 
	"vrf_summaries", 
	"vrf_static_default_nexthops", 
	"vrf_description", "interfaces",
]






# =====================================================================================================
def _get_all_int_columns():
	"""get all columns from all Interface Properties defined globally """
	all_if_cols = []
	for _k, v in IF_PROPS.items():
		all_if_cols.extend(v)
	return all_if_cols

def _df_columns_rearrange(pdf_dict, all_cols):
	"""rearrange columns of the dataframe as per interface properties grouping defined globally """
	for sht, df in pdf_dict.items():
		if sht in ('var',): continue
		if sht in ('bgp', 'vrf',):
			cols = all_cols[sht]
		elif sht in ('aggregated', 'vlan', 'physical', 'loopback', 'management', 'tunnel', ):
			cols = all_cols['interfaces']
		else:
			cols = df.columns
		pdf_dict[sht] = df[[ col for col in cols if col in df.columns ]]
	return pdf_dict


# =====================================================================================================

def rearrange_tables(clean_file, foreign_keys=None):
	"""rearrange Excel file columns as per interface properties grouping defined globally 
	provide foreign_keys dictionary with list of columns to be extended.
	"""
	pdf_dict = pd.read_excel(clean_file, sheet_name=None)
	#
	all_if_cols = _get_all_int_columns()
	all_bgp_cols = BGP_PROPS
	all_vrf_cols = VRF_PROPS
	#
	# -- add foreign keys
	if foreign_keys is not None:
		if "bgp" in foreign_keys:
			all_bgp_cols.extend(foreign_keys['bgp'])
		if "vrf" in foreign_keys:
			all_vrf_cols.extend(foreign_keys['vrf'])
		if "interfaces" in foreign_keys:
			all_if_cols.extend(foreign_keys['interfaces'])
		if "ifs" in foreign_keys:
			all_if_cols.extend(foreign_keys['ifs'])
	#
	all_cols = {
		'bgp': all_bgp_cols, 
		'vrf': all_vrf_cols,
		'interfaces': all_if_cols,
	}
	pdf_dict = _df_columns_rearrange(pdf_dict, all_cols)
	write_to_xl(clean_file, pdf_dict, overwrite=True)


# =====================================================================================================
__all__ = ['rearrange_tables', ]








