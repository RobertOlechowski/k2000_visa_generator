import datetime
import sys

if len(sys.argv) != 2:
    raise Exception("Arguments count")


def _load_version():
    try:
        with open("_ver.txt", "r") as file:
            contents = file.read().split(".")
            contents = [int(a) for a in contents]
            if len(contents) != 4:
                contents = [1, 0, 0, 0]
            return contents
    except:
        return [1, 0, 0, 0]


def _inc_version(version):
    version[-1] += 1
    return version


def _save_version(version):
    with open("_ver.txt", "w") as file:
        file.write(".".join([str(a) for a in version]))
    return version


command = sys.argv[1]
if command == "get_build_time":
    time = datetime.datetime.now(datetime.timezone.utc)
    print(time.isoformat())
    sys.exit()

if command == "get_version":
    ver = _load_version()
    ver_text = ".".join([str(a) for a in ver])
    print(f"v{ver_text}")
    sys.exit()

if command == "inc_version":
    ver = _load_version()
    _inc_version(ver)
    _save_version(ver)
    ver_text = ".".join([str(a) for a in ver])
    print(f"v{ver_text}")
    sys.exit()

raise Exception(f"Unknown command {command}")
