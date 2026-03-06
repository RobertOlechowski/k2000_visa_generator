from datetime import datetime
from lib_code.PhilipsGenerator import PhilipsGenerator


def main():
    generator = PhilipsGenerator()

    dev_id = "AB76-0871"
    days = 60
    current_time = datetime.now()

    result = generator.generate(dev_id=dev_id, days=days, current_time=current_time)

    print("=" * 60)
    print("Philips Device Activation Code")
    print("=" * 60)
    print(f"Device ID:     {dev_id}")
    print(f"Valid days:    {days}")
    print(f"Current date:  {current_time}")
    print(f"Code:          {result['code']}")
    print(f"Valid until:   {result['valid_until']}")
    print("=" * 60)


if __name__ == "__main__":
    main()
