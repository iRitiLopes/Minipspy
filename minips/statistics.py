from time import time


class Mipstatics:
    def __init__(self) -> None:
        self.statistics = {
            'I': 0,
            'R': 0,
            'J': 0,
            'FR': 0,
            'FI': 0,
            'timelapse_0': 0,
            'timelapse_f': 0
        }

    def start(self):
        self.__set_statistic('timelapse_0', time())

    def finish(self):
        self.__set_statistic('timelapse_f', time())

    def __set_statistic(self, key, value):
        self.statistics[key] = value

    def increase_statistic(self, instruction):
        instruction_mapper = {
            0: 'I',
            1: 'R',
            2: 'J',
            3: 'FI',
            4: 'FR'
        }
        self.statistics[instruction_mapper[instruction.instruction_type]] += 1

    def show_statistics(self):
        print("\n------------------------------------------")
        print("Instruction count:")
        total = 0
        elapsed_time = self.statistics['timelapse_f'] - \
            self.statistics['timelapse_0']
        for instruction_type in ['R', 'I', 'J', 'FR', 'FI']:
            v = self.statistics[instruction_type]
            total += v
            print(f"{instruction_type}: {v}", end=' ')
        print(f"\nTotal: {total}")
        print(f"Simulation time: {elapsed_time} sec")
        print(f"Average IPS: {total/elapsed_time}")
        print("------------------------------------------")
