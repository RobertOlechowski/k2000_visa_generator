from lib_code.Uint32 import Uint32


class DeviceIdParser:
    def parse(self, dev_id: str) -> Uint32:
        s = dev_id.replace(" ", "").replace("-", "").upper()
        if not all(c in "0123456789ABCDEF" for c in s) or len(s) != 8:
            raise ValueError("Invalid device ID format")
        return Uint32.create(int(s, 16))
