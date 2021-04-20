from minips import Minips
from sys import argv

def run():
    if len(argv) != 3:
        raise Exception(
            "Invalid arguments: main.py <mode[decode, run]> <filepath>")
    mode = argv[1]
    filepath = argv[2]
    minips = Minips()
    minips.load(filepath)

    if mode == 'decode':
        minips.decode()
    elif mode == 'run':
        minips.execute()
    elif mode == 'trace':
        minips.trace_mode()
    else:
        raise Exception("Invalid mode: Valid modes -> decode | run")


if __name__ == "__main__":
    run()
