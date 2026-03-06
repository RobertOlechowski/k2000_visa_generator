from datetime import datetime

from lib_code.Uint64 import Uint64


class TimeHelper:
    EPOCH_AS_FILETIME = 116444736000000000
    HUNDREDS_OF_NANOSECONDS = 10000000

    def get_ms_time(self, date_time: datetime) -> Uint64:
        from calendar import timegm
        unix_time = timegm(date_time.timetuple())
        return self._unixtime_to_mstime(Uint64.create(unix_time))

    def _unixtime_to_mstime(self, unix_time: Uint64) -> Uint64:
        timestamp = unix_time.get_long()
        timestamp *= self.HUNDREDS_OF_NANOSECONDS
        timestamp += self.EPOCH_AS_FILETIME
        return Uint64.create(timestamp)
