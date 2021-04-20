from minips.word import Word

class CacheController:
    def __init__(self) -> None:
        self.dirty = 0
        self.valid = 0

    def dirty_this(self):
        self.dirty = 1
    
    def clean_this(self):
        self.dirty = 0
    
    def valid_this(self):
        self.valid = 1
    
    def invalid_this(self):
        self.valid = 0
    

class Cache:
    def __init__(self, size=1024) -> None:
        self.size = size
        self.cache = {x: Word("".zfill(32)) for x in range(0, size, 4)}
        self.cache_control = {x: CacheController() for x in range(0, size, 4)}
    
    def store(self, address, data) -> None:
        pass

    def load(self, address) -> Word:
        pass

    def __is_valid_address(self, address):
        return address in self.mem_blocks or address % 4 == 0

    def __str__(self) -> str:
        return str({str(k): str(v) for k, v in self.cache.items()})


class CacheException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
