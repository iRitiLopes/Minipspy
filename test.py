from minips import Minips

if __name__ == "__main__":

    minips = Minips(mem_mode=2)
    minips.load('./examples/09.contador')
    minips.execute()
    print("a")