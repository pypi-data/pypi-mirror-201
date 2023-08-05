# ------------------------------------------------------------------------------
from nettoolkit import *

# ------------------------------------------------------------------------------


def get_vlans_juniper(spl, how="s"):
	"""get the list of vlans on the interface

	Args:
		spl (list): splitted line

	Returns:
		list: list of vlans
	"""    	
	memberlist_identifiers = ('vlan-id-list', 'members')
	is_any_members = False
	for memid in memberlist_identifiers:
		is_any_members = memid in spl
		if is_any_members: break
	if not is_any_members: return None
	int_vl_list = [int(vl) for vl in spl[spl.index(memid)+1:] if vl.isdigit()]
	str_vl_list = [vl for vl in spl[spl.index(memid)+1:] if vl.isdigit()]
	if how == 's':
		return str_vl_list
	else:
		return int_vl_list

def get_juniper_pw_string(spl, key_index):
	pw = " ".join(spl[key_index:]).strip().split("##")[0].strip()
	if pw[0] == '"': pw = pw[1:]
	if pw[-1] == '"': pw = pw[:-1]
	try:
		pw = juniper_decrypt(pw)
	except: pass
	return pw


# ------------------------------------------------------------------------------
