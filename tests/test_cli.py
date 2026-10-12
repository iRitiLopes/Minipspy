from pathlib import Path
import subprocess
import sys

import pytest

from minips import Minips


ROOT = Path(__file__).resolve().parents[1]
PROGRAM = str(ROOT / 'examples' / '01.soma')


def cli(arguments):
    return subprocess.run(
        [sys.executable, str(ROOT / 'main.py'), *arguments],
        cwd=ROOT, capture_output=True, text=True, timeout=10)


@pytest.mark.parametrize('mode', ['run', 'trace', 'debug'])
@pytest.mark.parametrize('memory_mode', [[], ['6']])
def test_statistics_are_hidden_by_default(mode, memory_mode):
    result = cli([mode, *memory_mode, PROGRAM])
    assert result.returncode == 0, result.stderr
    assert result.stdout == '7'


@pytest.mark.parametrize('mode', ['run', 'trace', 'debug'])
@pytest.mark.parametrize('arguments', [
    ['--stat', '6', PROGRAM], ['6', '--stat', PROGRAM],
    ['6', PROGRAM, '--stat'], [PROGRAM, '--stat'],
])
def test_stat_flag_enables_report(mode, arguments):
    result = cli([mode, *arguments])
    assert result.returncode == 0, result.stderr
    assert result.stdout.startswith('7\n')
    assert 'Instruction count:' in result.stdout
    assert 'Total: 8' in result.stdout
    assert 'Memory Info:' in result.stdout


def test_stat_flag_can_precede_mode():
    result = cli(['--stat', 'run', PROGRAM])
    assert result.returncode == 0, result.stderr
    assert 'Instruction count:' in result.stdout


@pytest.mark.parametrize('enabled', [False, True])
def test_python_api_controls_report(enabled, capsys):
    emulator = Minips(1, show_statistics=enabled)
    emulator.load(PROGRAM)
    emulator.execute()
    output = capsys.readouterr().out
    assert ('Instruction count:' in output) == enabled
    assert emulator.statistics.statistics['cycles'] > 0
