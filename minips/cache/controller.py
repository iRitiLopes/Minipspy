class CacheController:
    def __init__(self) -> None:
        self.dirty = 0
        self.valid = 0
        self.tag = None

    def dirty_this(self):
        self.dirty = 1
    
    def clean_this(self):
        self.dirty = 0
    
    def valid_this(self):
        self.valid = 1
    
    def invalid_this(self):
        self.valid = 0
    
    def set_tag(self, tag):
        self.tag = tag
    
    def compare_tag(self, tag):
        return self.tag == tag