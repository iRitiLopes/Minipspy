from datetime import datetime
from minips.word import Word

class CacheSet(list):
    def __init__(self, n_vias, blocks):
        self.timestamp = datetime.utcnow().timestamp()
        self.vias = blocks * n_vias


class CacheData:
    def __init__(self, data, tag, address):
        self.data = Word(data=data)
        self.tag = tag
        self.address = address
        self.valid = False
        self.dirty = False
        self.timestamp = datetime.utcnow().timestamp()
    
    def set_time(self):
        self.timestamp = datetime.utcnow().timestamp()
    
    def dirty_this(self):
        self.dirty = True
    
    def is_dirty(self):
        return self.dirty
    
    def clean_this(self):
        self.dirty = False
    
    def valid_this(self):
        self.valid = True
    
    def invalid_this(self):
        self.valid = False
    
    def set_tag(self, tag):
        self.tag = tag
    
    def set_address(self, address):
        self.address = address
    
    def set_data(self, data):
        self.data.data = data
    
    def compare_tag(self, tag):
        return self.tag == tag
    
    def __str__(self) -> str:
        return f"data: {self.data}, tag: {hex(self.tag)}, address: {hex(self.address)}, valid: {self.valid}, dirty: {self.dirty}"