"""common functions for cisco devices """

# ------------------------------------------------------------------------------
from nettoolkit import *
from nettoolkit.gpl import CISCO_IFSH_IDENTIFIERS

# ------------------------------------------------------------------------------


def expand_if(ifname):
	"""get the full length interface string for variable length interface

	Args:
		ifname (str): variable length interface name

	Returns:
		str: updated interface string
	"""    	
	return standardize_if(ifname, True)

def expand_if_dict(d):
	"""returns updated the dictionary with standard expanded interface format in keys.

	Args:
		d (dict): dictionary where keys are interface names

	Returns:
		dict: updated dictionary keys with standard expanded interface format
	"""
	return {standardize_if(k, True):v for k, v in d.items()}

def get_interface_cisco(line):
	"""get the standard interface string from interface config line

	Args:
		ifname (str): line starting with interface [interface name]

	Returns:
		str: standard interface string
	"""    	
	return STR.if_standardize(line[10:])


# ----------------------------------------------------------
def get_vlans_cisco(line):
	"""set of vlan numbers allowed for the interface.

	Args:
		line (str): interface config line containing vlan info

	Returns:
		dict: vlan information dictionary
	"""    	
	vlans = {'trunk': set(), 'access': None, 'voice': None, 'native': None}
	line = line.strip()
	if line.startswith("switchport trunk allowed"):
		vlans['trunk'] = trunk_vlans_cisco(line)
	elif line.startswith("switchport access vlan"):
		vlans['access'] = line.split()[-1]
	elif line.startswith("switchport voice vlan"):
		vlans['voice'] = line.split()[-1]
	elif line.startswith("switchport trunk native"):
		vlans['native'] = line.split()[-1]
	else:
		return None
	return vlans

def trunk_vlans_cisco(line):
	"""supportive to get_vlans_cisco(). derives trunk vlans

	Args:
		line (str): interface config line containing vlan info

	Returns:
		list, set: list or set of trunk vlans
	"""    	
	for i, s in enumerate(line):
		if s.isdigit(): break
	line = line[i:]
	# vlans_str = line.split()[-1]
	# vlans = vlans_str.split(",")
	line = line.replace(" ", "")
	vlans = line.split(",")
	if not line.find("-")>0:
		return vlans
	else:
		newvllist = []
		for vlan in vlans:
			if vlan.find("-")==-1: 
				newvllist.append(vlan)
				continue
			splvl = vlan.split("-")
			for vl in range(int(splvl[0]), int(splvl[1])+1):
				newvllist.append(vl)
		return set(newvllist)
# ---------------------------------------------------------------


def get_inet_address(line):
	"""derive the ipv4 information from provided line

	Args:
		line (str): interface config line

	Returns:
		str: ipv4 address with /mask , None if not found.
	"""    	
	if line.strip().startswith("ip address "):
		spl = line.split()
		ip  = spl[-2]
		mask = to_dec_mask(spl[-1])
		s = ip+"/"+str(mask)
		return s
	return None


def get_inetv6_address(line, link_local):
	"""derive the ipv6 information from provided line

	Args:
		line (str): interface config line

	Returns:
		str: ipv6 address with /mask , None if not found.
	"""    	
	v6idx = -2 if link_local else -1
	if line.strip().startswith("ipv6 address "):
		spl = line.split()
		ip  = spl[v6idx]
		return ip
	return None



# ---------------------------------------------------------------

def get_vrf_cisco(line):
	"""get the standard vrf string from vrf config line

	Args:
		ifname (str): line starting with vrf definition [vrf name]

	Returns:
		str: standard interface string
	"""    	
	vrfname = line.split()[-1]	
	return vrfname



# ---------------------------------------------------------------
