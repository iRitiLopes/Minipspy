from minips import Minips
import cProfile, pstats

if __name__ == "__main__":
<<<<<<< HEAD

    minips = Minips(mem_mode=2)
    minips.load('./examples/09.contador')
    minips.execute()
    print("a")
=======
    profiler = cProfile.Profile()
    minips = Minips(mem_mode=1)
    minips.load('./examples/example')
    profiler.enable()
    minips.execute()
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('tottime')
    stats.print_stats()
>>>>>>> feature/profile
