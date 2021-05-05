from random import randint
class RandomAccess:
    def run(self, from_n, to_n, *args, **kwargs):
        return randint(from_n, to_n)