"""generate Network Devices (Switch/Router) facts from its configuration outputs.
"""

from .merger import device
from .merger import DeviceDB
from .facts_gen import FactsGen

__all__ = [ 
	'device', 'DeviceDB', 'FactsGen',
]

__ver__ = "0.0.7"