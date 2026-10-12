from minips import Minips
import argparse


def run(arguments=None):
    parser = argparse.ArgumentParser(description='Mini MIPS emulator')
    parser.add_argument('mode', choices=['decode', 'run', 'trace', 'debug'])
    parser.add_argument('mem_mode', nargs='?', type=int, choices=range(1, 7), default=1)
    parser.add_argument('filepath', help='Program prefix without .text')
    parser.add_argument('--stat', action='store_true', help='Print execution statistics')
    args = parser.parse_intermixed_args(arguments)
    mode, mem_mode, filepath = args.mode, args.mem_mode, args.filepath

    if mode == 'decode':
        minips = Minips(mem_mode=1)
        minips.load(filepath)
        minips.decode()
    elif mode == 'run':
        minips = Minips(mem_mode=mem_mode, show_statistics=args.stat)
        minips.load(filepath)
        minips.execute()
    elif mode == 'trace':
        minips = Minips(mem_mode=mem_mode, show_statistics=args.stat)
        minips.load(filepath)
        minips.trace_mode()
    elif mode == 'debug':
        minips = Minips(mem_mode=mem_mode, show_statistics=args.stat)
        minips.load(filepath)
        minips.debug_mode()
    else:
        raise Exception("Invalid mode: Valid modes -> decode | run")


if __name__ == "__main__":
    run()
