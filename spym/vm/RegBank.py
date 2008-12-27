class RegisterBank(object):
	REGISTER_NAMES = {
		"$zero" : 0, "$at" : 1, 
		"$v0" : 2, "$v1" : 3, 
		"$a0" : 4, "$a1" : 5, 
		"$a2" : 6, "$a3" : 7, 
		"$t0" : 8, "$t1" : 9, 
		"$t2" : 10, "$t3" : 11, 
		"$t4" : 12, "$t5" : 13, 
		"$t6" : 14, "$t7" : 15, 
		"$t8" : 24, "$t9" : 25, 
		"$s0" : 16, "$s1" : 17, 
		"$s2" : 18, "$s3" : 19, 
		"$s4" : 20, "$s5" : 21, 
		"$s6" : 22, "$s7" : 23, 
		"$k0" : 26, "$k1" : 27, 
		"$gp" : 28, "$sp" : 29, 
		"$fp" : 30, "$ra" : 31
	}
	
	class RegisterAccessFault(Exception):
		pass
		
	class CoprocessorZero(object):
		STATUS_USER_MASK = 0x0002
		REGISTER_NAMES = {
			8	: 'BadVAddr',
			9	: 'Count',
			11	: 'Compare',
			12	: 'Status',   
			13	: 'Cause',
			14	: 'EPC',
			16	: 'Config',
		}
		
		def __init__(self):			
			self.BadVAddr 	= 0x0
			self.Count		= 0x0
			self.Compare	= 0x0
			self.Status		= 0x0
			self.Cause		= 0x0
			self.EPC		= 0x0
			self.Config		= 0x0
					
		def getUserBit(self):
			return self.Status & self.STATUS_USER_MASK
			
		def __getitem__(self, item):
			if self.getUserBit():
				raise RegisterBank.RegisterAccessFault("Cannot access Coprocessor 0 registers while in usermode.")
				
			if item in self.REGISTER_NAMES:
				return getattr(self, self.REGISTER_NAMES[item])
			
			elif hasattr(self, item):
				return getattr(self, item)
				
			return 0x0
		
		def __setitem__(self, item, data):
			if self.getUserBit():
				raise RegisterBank.RegisterAccessFault("Cannot access Coprocessor 0 registers while in usermode.")
				
			data = data & 0xFFFFFFFF
				
			if item in self.REGISTER_NAMES:
				setattr(self, self.REGISTER_NAMES[item], data)
			elif hasattr(self, item):
				setattr(self, item, data)
	
	def __init__(self, vm_memory):
		self.std_registers = 32 * [0, ]
		self.HI = 0x0
		self.LO = 0x0
		self.PC = 0x0
		
		self.CP0 = self.CoprocessorZero()
		self.memory = vm_memory
		
	def __getitem__(self, item):
		return self.std_registers[item] if item else 0
			
	def __setitem__(self, item, value):
		if item: self.std_registers[item] = value & 0xFFFFFFFF