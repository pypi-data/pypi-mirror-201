"""generate Network Devices (Switch/Router) facts from its configuration outputs.
"""

# ------------------------------------------------------------------------------

from .generators.merger import device
from .generators.merger import DeviceDB
from .rearrange import rearrange_tables

from .clean import CleanFacts



__all__ = [ 
	'device', 'DeviceDB',
	'CleanFacts',
	'rearrange_tables',
	]

__ver__ = "0.0.14"