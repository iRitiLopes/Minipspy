from minips import Minips
import cProfile, pstats

if __name__ == "__main__":
    #profiler = cProfile.Profile()
    minips = Minips(mem_mode=2)
    #profiler.enable()
    minips.load('./examples/02.hello')
    minips.execute()
    #profiler.disable()
    #stats = pstats.Stats(profiler).sort_stats('tottime')
    #stats.print_stats()
