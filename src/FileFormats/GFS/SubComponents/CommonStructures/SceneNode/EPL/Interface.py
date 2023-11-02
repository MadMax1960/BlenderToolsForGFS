class EPLInterface:
    def __init__(self):
        self.node = None
        self.binary = None
        
    @classmethod
    def from_binary(cls, node_idx, binary):
        instance = cls()
        
        instance.node = node_idx
        instance.binary = binary
        
        return instance
    
    def to_binary(self):
        return self.binary
