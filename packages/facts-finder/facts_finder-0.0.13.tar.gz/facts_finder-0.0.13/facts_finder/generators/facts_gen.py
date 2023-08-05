"""Boiler plate code for the facts generation.
fg_dict: attribute will provide the output dictionary with pandas dataframe as values to be readily available to write it to excel.
dev_type: attribute returns the device type of configuraton provided
"""

from .merger import device, DeviceDB
from .cisco_parser import Cisco
from .juniper_parser import Juniper
# ==============================================================================


class FactsGen:

	def __init__(self, capture_file):
		self.capture_file = capture_file

	def __call__(self):
		self.model = device(self.capture_file)           # select the model based on input file
		device_database = DeviceDB()    				 # create a new device database object
		df_dict = device_database.evaluate(self.model)   # evaluate object by providing necessary model, and return dictionary	
		df_dict['system'] = df_dict['system'].reset_index().rename(columns={'system':'var', 0:'default'})
		self.df_dict = df_dict
		return df_dict

	def __iter__(self):
		for k, v in self.fg_dict.items():
			yield (k, v)

	def __getitem__(self, key):
		return self.fg_dict[key]

	@property
	def dev_type(self):
		"""detected device type for the given configuration capture"""
		try:
			if isinstance(self.model, Cisco):
				return 'cisco'
			elif isinstance(self.model, Juniper):
				return 'juniper'
			else:
				raise Exception(f'Invalid device type ``{type(self.model)}``. verify config')
		except Exception as e:
			raise Exception(f"FactsGen needs to be called in order to get the device type."
				f"\n\tEither it is not called or invalid config present in device capture."
				f"\n\t{e}")

	@property
	def fg_dict(self):
		"""facts generator dictionary"""
		return self.df_dict

# ==============================================================================
