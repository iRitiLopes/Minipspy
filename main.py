from minips import Minips
from sys import argv

def run():
    if len(argv) < 3 or len(argv) > 4:
        raise Exception(
            "Invalid arguments: main.py <mode[decode, run]> <Memorymode[1,2,3,4], optional> <filepath>")
    mode = argv[1]
    mem_mode = 1
    if len(argv) == 3:
        filepath = argv[2]
    else:
        mem_mode = int(argv[2])
        filepath = argv[3]

    if mode == 'decode':
        minips = Minips(mem_mode=1)
        minips.load(filepath)
        minips.decode()
    elif mode == 'run':
        minips = Minips(mem_mode=mem_mode)
        minips.load(filepath)
        minips.execute()
    elif mode == 'trace':
        minips = Minips(mem_mode=mem_mode)
        minips.load(filepath)
        minips.trace_mode()
    elif mode == 'debug':
        minips = Minips(mem_mode=mem_mode)
        minips.load(filepath)
        minips.debug_mode()
    else:
        raise Exception("Invalid mode: Valid modes -> decode | run")


if __name__ == "__main__":
    run()
