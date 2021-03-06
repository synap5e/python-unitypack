import struct
from os import SEEK_CUR


class BinaryReader:
	def __init__(self, buf, endian="<"):
		self.buf = buf
		self.endian = endian

	def align(self):
		old = self.tell()
		new = (old + 3) & -4
		if new > old:
			self.seek(new - old, SEEK_CUR)

	def read(self, *args):
		return self.buf.read(*args)

	def seek(self, *args):
		return self.buf.seek(*args)

	def tell(self):
		return self.buf.tell()

	def read_string(self, size=None, encoding="utf-8"):
		if size is None:
			ret = self.read_cstring()
		else:
			ret = struct.unpack(self.endian + "%is" % (size), self.read(size))[0]
		return ret.decode(encoding)

	def read_cstring(self):
		ret = []
		c = b""
		while c != b"\0":
			ret.append(c)
			c = self.read(1)
			if not c:
				raise ValueError("Unterminated string: %r" % (ret))
		return b"".join(ret)

	def read_boolean(self):
		return struct.unpack(self.endian + "b", self.read(1))[0]

	def read_byte(self):
		return struct.unpack(self.endian + "b", self.read(1))[0]

	def read_int16(self):
		return struct.unpack(self.endian + "h", self.read(2))[0]

	def read_int(self):
		return struct.unpack(self.endian + "i", self.read(4))[0]

	def read_uint(self):
		return struct.unpack(self.endian + "I", self.read(4))[0]

	def read_float(self):
		return struct.unpack(self.endian + "f", self.read(4))[0]

	def read_int64(self):
		return struct.unpack(self.endian + "q", self.read(8))[0]
