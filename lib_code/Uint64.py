from lib_code.Uint32 import Uint32


class Uint64:
    def __init__(self, value: int):
        self._data = value & 0xFFFFFFFFFFFFFFFF

    @staticmethod
    def create(p1, p2=None) -> 'Uint64':
        if p2 is None:
            if isinstance(p1, Uint32):
                return Uint64(p1.get_long())
            return Uint64(p1)
        return Uint64.create(p1).shift_L(32).or_(Uint64.create(p2))

    def get_long(self) -> int:
        return self._data

    def get_p1(self) -> Uint32:
        return Uint32.create(int(self.clone().shift_R(32).and_(0xFFFFFFFF).get_long()))

    def get_p2(self) -> Uint32:
        return Uint32.create(int(self.clone().and_(0xFFFFFFFF).get_long()))

    def clone(self) -> 'Uint64':
        return Uint64(self._data)

    def add(self, value: int) -> 'Uint64':
        self._data = (self._data + value) & 0xFFFFFFFFFFFFFFFF
        return self

    def and_(self, value: int) -> 'Uint64':
        self._data = self._data & value
        return self

    def or_(self, value) -> 'Uint64':
        if isinstance(value, Uint64):
            value = value._data
        self._data = self._data | value
        return self

    def shift_L(self, bits: int) -> 'Uint64':
        if bits >= 64:
            self._data = 0
        else:
            self._data = (self._data << bits) & 0xFFFFFFFFFFFFFFFF
        return self

    def shift_R(self, bits: int) -> 'Uint64':
        if bits >= 64:
            self._data = 0
        else:
            self._data = self._data >> bits
        return self
