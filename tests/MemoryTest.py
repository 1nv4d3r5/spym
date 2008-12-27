import unittest
import testcommon

from spym.vm.Memory import MemoryManager

class TestMemoryManager(unittest.TestCase):
	def setUp(self):
		self.memory = MemoryManager(None, 32)
		
	def testInnerConsistency(self):
		for i in xrange(0, 128, 4):
			self.memory[i] = 0xFF000000
		
		self.assertEqual(len(self.memory.memory), 4)
		
		self.memory[128] = 0x0
		self.assertEqual(len(self.memory.memory), 5)
		
		print str(self.memory)
		
	def testSimpleAllocation(self):
		self.memory[0x00000004] = 0x2
		self.assertEqual(self.memory[0x4], 0x2)
		
		self.memory[0x0008, 2] = 0xFFFF
		self.memory[0x000A, 2] = 0xAAAA
		self.assertEqual(self.memory[0x0008, 4], 0xAAAAFFFF)
		
		self.memory[0x0010, 1] = 0xAAFF
		self.memory[0x0011, 1] = 0xEEEE
		self.assertEqual(self.memory[0x0010, 4], 0x0000EEFF)
		
		self.memory[0x0002] = 0xABCD0A0A
		self.assertEqual(self.memory[0x0002], 0x0A0A)
		
	def testMemoryBounds(self):
		self.assertRaises(MemoryManager.InvalidMemoryAddress, self.memory.__getitem__, 0xFFFFFFFF0)
		self.assertEqual(self.memory[0xFFFFFFFF], 0)
		
	def testAlignmentChecks(self):
		self.assertRaises(MemoryManager.UnalignedMemoryAccess, self.memory.getWord, 0x0003)
		self.assertRaises(MemoryManager.UnalignedMemoryAccess, self.memory.getWord, 0x0002)
		self.assertRaises(MemoryManager.UnalignedMemoryAccess, self.memory.getHalf, 0x0003)
		self.assertRaises(MemoryManager.UnalignedMemoryAccess, self.memory.getWord, 0x0001)
		
		self.assertRaises(MemoryManager.UnalignedMemoryAccess, self.memory.setWord, 0x0003, 0xFFFF)
		self.assertRaises(MemoryManager.UnalignedMemoryAccess, self.memory.setWord, 0x0002, 0xFFFF)
		self.assertRaises(MemoryManager.UnalignedMemoryAccess, self.memory.setHalf, 0x0003, 0xFFFF)
		self.assertRaises(MemoryManager.UnalignedMemoryAccess, self.memory.setWord, 0x0001, 0xFFFF)
		
		self.assertEqual(self.memory.getWord(0x0000), 0)
		self.assertEqual(self.memory.getHalf(0x0002), 0)
		self.assertEqual(self.memory.getByte(0x0003), 0)
		
		
if __name__ == '__main__':
	unittest.main()