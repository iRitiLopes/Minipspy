"""Compare program output across cache modes, with bounded subprocesses."""
import argparse
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
SLOW = {'18.naive_dgemm', '19.regular_dgemm', '20.blocking_dgemm', '21.mandelbrot'}
INPUTS = {
    '03.input': '10\n',
    '05.fibo': '10\n',
    '06.collatz': '10\n3\n0\n',
    '14.flutuantes': '3\n3\n',
    '15.pi': '10\n',
    '16.automato': '30\n3\n',
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('programs', nargs='*', help='Program prefixes without .text')
    parser.add_argument('--all', action='store_true', help='Include slow matrix/fractal programs')
    parser.add_argument('--timeout', type=float, default=60, help='Seconds per program/mode')
    args = parser.parse_args()
    if args.programs:
        programs = [Path(p).resolve() for p in args.programs]
    else:
        programs = [p.with_suffix('') for p in sorted((ROOT / 'examples').glob('[0-9][0-9].*.text'))
                    if args.all or p.stem not in SLOW]
    failures = 0
    for program in programs:
        reference = None
        ok = True
        for mode in range(1, 7):
            try:
                result = subprocess.run(
                    [sys.executable, str(ROOT / 'main.py'), 'run', str(mode), str(program)],
                    input=INPUTS.get(program.name, ''), capture_output=True,
                    text=True, cwd=ROOT, timeout=args.timeout)
                if result.returncode:
                    raise RuntimeError(result.stderr.strip())
                # Timing/statistics differ; compare only guest program output.
                output = result.stdout.split('\n------------------------------------------', 1)[0]
                if mode == 1:
                    reference = output
                elif output != reference:
                    raise RuntimeError('Output differs from uncached mode')
            except (subprocess.TimeoutExpired, RuntimeError) as error:
                print(f'FAIL {program.name} mode {mode}: {error}', flush=True)
                failures += 1
                ok = False
                break
        if ok:
            print(f'PASS {program.name}: modes 1-6 agree', flush=True)
    return int(failures != 0)


if __name__ == '__main__':
    sys.exit(main())
