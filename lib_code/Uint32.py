class Uint32:
    def __init__(self, value: int):
        self._data = value & 0xFFFFFFFF

    @staticmethod
    def create(value: int) -> 'Uint32':
        return Uint32(value)

    def get_int(self) -> int:
        if self._data & 0x80000000:
            return self._data - 0x100000000
        return self._data

    def get_long(self) -> int:
        return self._data

    def clone(self) -> 'Uint32':
        return Uint32(self._data)

    def add(self, value: int) -> 'Uint32':
        self._data = (self._data + value) & 0xFFFFFFFF
        return self

    def sub(self, value: int) -> 'Uint32':
        self._data = (self._data - value) & 0xFFFFFFFF
        return self

    def and_(self, value: int) -> 'Uint32':
        self._data = self._data & value
        return self

    def or_(self, value: int) -> 'Uint32':
        self._data = self._data | value
        return self

    def xor(self, value) -> 'Uint32':
        if isinstance(value, Uint32):
            value = value._data
        self._data = self._data ^ value
        return self

    def shift_L(self, bits: int) -> 'Uint32':
        if bits >= 32:
            self._data = 0
        else:
            self._data = (self._data << bits) & 0xFFFFFFFF
        return self

    def shift_R(self, bits: int) -> 'Uint32':
        if bits >= 32:
            self._data = 0
        else:
            self._data = self._data >> bits
        return self

    def rot_L(self, bits: int) -> 'Uint32':
        bits = bits % 32
        for _ in range(bits):
            bit = 1 if (self._data & 0x80000000) else 0
            self.shift_L(1)
            self.add(bit)
        return self

    def rot_R(self, bits: int) -> 'Uint32':
        bits = bits % 32
        for _ in range(bits):
            bit = 0x80000000 if (self._data & 0x1) else 0
            self.shift_R(1)
            self.add(bit)
        return self
