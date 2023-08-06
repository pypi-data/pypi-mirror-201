import struct


class BinaryStreamRead:
	def __init__(self, data):
		self.buffer = data
		self.pos = 0
	
	def seek(self, pos):
		self.pos = pos
	
	def read(self, lenght=-1):
		if lenght < 0:
			lenght = len(self.buffer)-self.pos
		data = self.buffer[self.pos:self.pos+lenght]
		self.pos += lenght
		return data
	
	def int8(self):
		return struct.unpack("!b", self.read(1))[0]
	
	def uint8(self):
		return struct.unpack("!B", self.read(1))[0]
	
	def int16(self):
		return struct.unpack("!h", self.read(2))[0]
	
	def uint16(self):
		return struct.unpack("!H", self.read(2))[0]
	
	def int24(self):
		data = self.read(3)
		return struct.unpack("!i", (b"\x00" if data[2] < 0x80 else b"\xff") + data)[0]
	
	def uint24(self):
		return struct.unpack("!I", b"\x00"+self.read(3))[0]
	
	def int32(self):
		return struct.unpack("!i", self.read(4))[0]
	
	def uint32(self):
		return struct.unpack("!I", self.read(4))[0]
	
	def int64(self):
		return struct.unpack("!q", self.read(8))[0]
	
	def uint64(self):
		return struct.unpack("!Q", self.read(8))[0]
	
	def float16(self):
		return struct.unpack("!e", self.read(2))[0]
	
	def float32(self):
		return struct.unpack("!f", self.read(4))[0]
	
	def float64(self):
		return struct.unpack("!d", self.read(8))[0]
	
	def bool(self):
		return struct.unpack("!?", self.read(1))[0]


class BinaryStreamWrite:
	def __init__(self):
		self.buffer = bytes()
	
	def write(self, data):
		self.buffer += data
	
	def read(self):
		return self.buffer
	
	def int8(self, val):
		self.write(struct.pack("!b", val))
	
	def uint8(self, val):
		self.write(struct.pack("!B", val))
	
	def int16(self, val):
		self.write(struct.pack("!h", val))
	
	def uint16(self, val):
		self.write(struct.pack("!H", val))
	
	def int24(self, val):
		self.write(struct.pack("!i", val)[1:])
	
	def uint24(self, val):
		self.write(struct.pack("!I", val)[1:])
	
	def int32(self, val):
		self.write(struct.pack("!i", val))
	
	def uint32(self, val):
		self.write(struct.pack("!I", val))
	
	def int64(self, val):
		self.write(struct.pack("!q", val))
	
	def uint64(self, val):
		self.write(struct.pack("!Q", val))
	
	def float16(self, val):
		self.write(struct.pack("!e", val))
	
	def float32(self, val):
		self.write(struct.pack("!f", val))
	
	def float64(self, val):
		self.write(struct.pack("!d", val))
	
	def bool(self, val):
		self.write(struct.pack("!?", val))