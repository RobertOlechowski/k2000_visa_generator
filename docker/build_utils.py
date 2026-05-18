import argparse
import datetime
from pathlib import Path


def load_version(file_path: Path) -> list[int]:
    try:
        if not file_path.exists():
            return [1, 0, 0, 0]
        contents = file_path.read_text().strip().split(".")
        version = [int(a) for a in contents]
        return version if len(version) == 4 else [1, 0, 0, 0]
    except Exception:
        return [1, 0, 0, 0]


def save_version(file_path: Path, version: list[int]) -> None:
    file_path.write_text(".".join(map(str, version)))


def main() -> None:
    parser = argparse.ArgumentParser(description="Docker Build Utilities")
    parser.add_argument("command", choices=["get_build_time", "get_version", "inc_version"])
    parser.add_argument("--file", type=str, default="docker/_ver.txt")

    args = parser.parse_args()
    ver_file = Path(args.file).absolute()

    if args.command == "get_build_time":
        print(datetime.datetime.now(datetime.timezone.utc).isoformat())
    elif args.command == "get_version":
        version = load_version(ver_file)
        print(f"v{'.'.join(map(str, version))}")
    elif args.command == "inc_version":
        version = load_version(ver_file)
        version[-1] += 1
        save_version(ver_file, version)
        print(f"v{'.'.join(map(str, version))}")


if __name__ == "__main__":
    main()
