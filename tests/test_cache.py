import random

import pytest

from helpers.log import Log
from minips.cache.l1 import L1Cache
from minips.cache.mapping.nvias import NVias
from minips.cache.policy.lru import LRUAccess
from minips.memory import Memory, MemoryException


@pytest.mark.parametrize("mode", range(1, 7))
def test_memory_is_isolated_and_unmapped_reads_stay_empty(mode):
    first = Memory(mode, Log())
    second = Memory(mode, Log())
    first.store(0x10011000, 42)
    assert second.load(0x10011000).is_empty()
    assert first.load(0x10011000).data == 42
    assert first.load(0x10011004).is_empty()
    assert first.load(0x10011004).is_empty()
    first.clean()
    assert first.load(0x10011000).is_empty()


@pytest.mark.parametrize("mode", range(2, 7))
def test_conflicts_and_writebacks_match_ram(mode):
    memory = Memory(mode, Log())
    rng = random.Random(17)
    addresses = [0x10010000 + i * 4096 + j * 4
                 for i in range(20) for j in range(16)]
    expected = {address: i for i, address in enumerate(addresses)}
    for address, value in expected.items():
        memory.init_store(address, value)
    for _ in range(1200):
        address = rng.choice(addresses)
        if rng.randrange(2):
            value = rng.randrange(2 ** 32)
            memory.store(address, value)
            expected[address] = value
        else:
            assert memory.load(address).data == expected[address]
    for address, value in expected.items():
        assert memory.load(address).data == value
    memory.flush()
    assert all(memory.mem_blocks[a].data == v for a, v in expected.items())
    counts = dict(memory.access_count)
    memory.flush()
    assert memory.access_count == counts


def test_lru_updates_on_load_and_store_and_prefers_invalid_ways():
    cache = L1Cache(size=64, line_size=16, mode=NVias(4), policy=LRUAccess())
    for via in range(4):
        assert cache.need_writeback(via * 16) == (False, via)
        cache.store_line(via * 16, [via] * 4, via)
    cache.load(0, 0)
    cache.store(16, 99)
    assert cache.need_writeback(64) == (False, 2)
    cache.store_line(64, [4] * 4, 2)
    assert cache.hit(32) == (False, -1)
    assert cache.load(16, 1).data == 99
    assert cache.cache[0][0][0] is not cache.cache[0][0][1]
    assert cache.cache[0][0] is not cache.cache[0][1]


def test_dirty_writeback_returns_victim_address():
    cache = L1Cache(size=32, line_size=32)
    cache.store_line(0x10010000, list(range(8)), 0)
    assert cache.need_writeback(0x10011000) == (False, 0)
    cache.store(0x10010004, 99)
    assert cache.need_writeback(0x10011000) == (True, 0)
    line, address = cache.writeback(0x10011000, 0)
    assert address == 0x10010000
    assert line[1].address == 0x10010004
    assert line[1].data.data == 99


def test_l2_serves_l1_conflict_without_ram_read():
    memory = Memory(6, Log())
    # Five lines in the same four-way L1 set, all fitting in L2.
    addresses = [0x10010000 + 128 * i for i in range(5)]
    for i, address in enumerate(addresses):
        memory.init_store(address, i + 1)
        assert memory.load(address).data == i + 1
    count = memory.access_count[3]
    for _ in range(5):
        for i, address in enumerate(addresses):
            assert memory.load(address).data == i + 1
    assert memory.access_count[3] == count
    assert memory.access_count[2] > 5


@pytest.mark.parametrize("mode", range(1, 7))
@pytest.mark.parametrize("address", [-4, 1, 2 ** 32])
def test_invalid_addresses(mode, address):
    memory = Memory(mode, Log())
    with pytest.raises(MemoryException):
        memory.load(address)
    with pytest.raises(MemoryException):
        memory.store(address, 1)


@pytest.mark.parametrize('mode', range(1, 7))
def test_compatibility_controller_uses_working_memory(mode):
    from minips.memory_controller import MemoryController

    controller = MemoryController(mode)
    controller.store(0x10012000, 42)
    assert controller.load(0x10012000).data == 42
    controller.flush()
    assert controller.memory.mem_blocks[0x10012000].data == 42


def test_statistics_include_both_cache_levels():
    from minips.statistics import Mipstatics

    memory = Memory(6, Log())
    memory.init_store(memory.TEXT_SECTION_START, 1)
    memory.init_store(memory.DATA_SECTION_START, 2)
    memory.load(memory.TEXT_SECTION_START)
    memory.load(memory.DATA_SECTION_START)
    memory.store(memory.DATA_SECTION_START, 3)
    stats = Mipstatics()
    stats.memory_statistics(memory)
    assert stats.statistics['memory_access'] == 2
    assert stats.statistics['l2_access'] == 2
    assert stats.statistics['l1i_access'] == 1
    assert stats.statistics['l1d_access'] == 2
    assert stats.statistics['cycles'] == 223


def test_mode_four_lru_replaces_least_recent_line():
    memory = Memory(4, Log())
    base = memory.DATA_SECTION_START
    for i in range(16):
        memory.init_store(base + i * 32, i)
        memory.load(base + i * 32)
    memory.load(base)  # Preserve the oldest inserted line by touching it.
    memory.init_store(base + 16 * 32, 16)
    memory.load(base + 16 * 32)
    assert memory.cache.hit(base)[0]
    assert not memory.cache.hit(base + 32)[0]
