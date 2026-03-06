from lib_code.Uint32 import Uint32
from lib_code.Uint64 import Uint64


class SeedTransform:
    def forward(self, dev_id: Uint32) -> Uint64:
        value = self._init_seed(dev_id.clone())
        seed_1 = value.clone().xor(dev_id)
        seed_2 = value.rot_L(1).xor(dev_id)
        return Uint64.create(seed_1, seed_2)

    def _init_seed(self, dev_id: Uint32) -> Uint32:
        eax = Uint32.create(0)
        for _ in range(0x20):
            eax.shift_L(1)
            bit = dev_id.clone().and_(0x1).get_int()
            eax.or_(bit)
            dev_id.shift_R(1)
        return eax


class TimeTransform:
    @staticmethod
    def forward(arg: Uint64) -> Uint32:
        DIVIDER = 0x989680

        data = arg.clone().add(0xfe624e212ac18000)
        edx = data.get_p1().get_long() % DIVIDER
        value = (edx << 32) + data.get_p2().get_long()
        value = value // DIVIDER
        return Uint64.create(value).get_p2()


class Transform1:
    @staticmethod
    def forward(arg_1: Uint32, arg_2: Uint32) -> Uint32:
        return arg_1.clone().sub(1).rot_L(1).xor(arg_2)

    @staticmethod
    def reward(arg_1: Uint32, arg_2: Uint32) -> Uint32:
        return arg_1.clone().xor(arg_2).rot_R(1).add(1)


class Transform2:
    @staticmethod
    def forward(arg: Uint32) -> Uint32:
        val_1 = arg.clone().shift_R(0x10).and_(0xFF)
        val_2 = arg.clone().shift_R(0x8).and_(0xFF)
        val_3 = arg.clone().and_(0xFF)
        val_4 = arg.clone().shift_R(0x18).and_(0xFF)
        return val_1.add(val_2.get_long()).add(val_3.get_long()).add(val_4.get_long()).or_(0x2000000)
