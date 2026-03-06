from datetime import datetime, timedelta

from lib_code.Computer import Computer
from lib_code.DeviceIdParser import DeviceIdParser
from lib_code.Uint64 import Uint64


class PhilipsGenerator:
    def __init__(self):
        self._dev_id_parser = DeviceIdParser()
        self._computer = Computer()

    def generate(self, dev_id: str, days: int, current_time: datetime = None) -> dict:
        try:
            if current_time is None:
                current_time = datetime.utcnow()
            current_time = current_time.replace(microsecond=0)
            dev_id_uint = self._dev_id_parser.parse(dev_id)
            valid_until = current_time + timedelta(days=days, hours=6)
            valid_until = valid_until.replace(hour=0, minute=0, second=0, microsecond=0)
            code = self._computer.compute_code(dev_id_uint, valid_until)
            code_str = self._format_code(code)
            return {'code': code_str, 'valid_until': valid_until}
        except Exception as e:
            raise Exception(f"Error generating code: {str(e)}")

    def _format_code(self, code: Uint64) -> str:
        p1 = code.clone().shift_R(0x30).and_(0xFFFF).get_long()
        p2 = code.clone().shift_R(0x20).and_(0xFFFF).get_long()
        p3 = code.clone().shift_R(0x10).and_(0xFFFF).get_long()
        p4 = code.clone().shift_R(0x00).and_(0xFFFF).get_long()
        return f"{p1:04X}-{p2:04X}-{p3:04X}-{p4:04X}"
