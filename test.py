from minips import Minips

if __name__ == "__main__":

    minips = Minips()
    minips.load('./examples/example')
    print(minips.memory.load(8388628))
