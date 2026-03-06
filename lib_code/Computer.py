from datetime import datetime

from lib_code.TimeHelper import TimeHelper
from lib_code.Transform import SeedTransform, TimeTransform, Transform1, Transform2
from lib_code.Uint32 import Uint32
from lib_code.Uint64 import Uint64


class Computer:
    def __init__(self):
        self._seed_transform = SeedTransform()
        self._time_helper = TimeHelper()

    def compute_code(self, dev_id: Uint32, date_time: datetime) -> Uint64:
        seed = self._seed_transform.forward(dev_id)
        ms_time = self._time_helper.get_ms_time(date_time)
        p1_transf = TimeTransform.forward(ms_time)
        p2_transf = Transform2.forward(p1_transf)
        part_1 = Transform1.reward(p1_transf, seed.get_p1())
        part_2 = Transform1.reward(p2_transf, seed.get_p2())
        return Uint64.create(part_1, part_2)
