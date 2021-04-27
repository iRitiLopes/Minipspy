from minips import Minips
import cProfile, pstats

if __name__ == "__main__":
    profiler = cProfile.Profile()
    minips = Minips(mem_mode=1)
    minips.load('./examples/21.mandelbrot')
    profiler.enable()
    minips.execute()
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('tottime')
    stats.print_stats()
