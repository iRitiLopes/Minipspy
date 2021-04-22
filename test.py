from minips import Minips
import cProfile, pstats

if __name__ == "__main__":
    profiler = cProfile.Profile()
    minips = Minips()
    minips.load('./examples/example')
    profiler.enable()
    minips.execute()
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('tottime')
    stats.print_stats()
